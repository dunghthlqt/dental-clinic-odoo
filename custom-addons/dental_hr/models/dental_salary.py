# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class DentalSalary(models.Model):
    _name = 'dental.salary'
    _description = 'Dental Salary'
    _order = 'month desc, id desc'
    
    name = fields.Char('Tên', required=True, default=lambda self: _('Lương tháng %s/%s') % (
        fields.Date.today().month, fields.Date.today().year))
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Nhân viên',
        required=True,
        ondelete='cascade'
    )
    
    month = fields.Date('Tháng/Năm', required=True, default=lambda self: fields.Date.today().replace(day=1))
    
    # Lương cơ bản
    base_salary = fields.Float(
        'Lương cơ bản',
        compute='_compute_base_salary',
        store=True,
        help='Lương cơ bản từ hợp đồng'
    )
    
    # Thưởng
    bonus_ids = fields.Many2many(
        'dental.bonus',
        'salary_bonus_rel',
        'salary_id',
        'bonus_id',
        string='Thưởng',
        domain=[('state', '=', 'confirmed')],
        help='Các khoản thưởng trong tháng'
    )
    
    bonus_amount = fields.Float(
        'Tổng thưởng',
        compute='_compute_bonus_amount',
        store=True
    )
    
    # Tổng lương
    total_salary = fields.Float(
        'Tổng lương',
        compute='_compute_total_salary',
        store=True,
        help='Tổng lương = Lương cơ bản + Tổng thưởng'
    )
    
    # Trạng thái
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('submitted', 'Đã gửi'),
        ('approved', 'Đã duyệt'),
        ('posted', 'Đã đăng'),
    ], string='Trạng thái', default='draft', readonly=True)
    
    # Kế toán
    account_move_id = fields.Many2one(
        'account.move',
        string='Bút toán kế toán',
        readonly=True,
        help='Bút toán kế toán được tạo tự động'
    )
    
    # Workflow
    submitted_by = fields.Many2one('res.users', string='Người gửi', readonly=True)
    submitted_date = fields.Datetime('Ngày gửi', readonly=True)
    approved_by = fields.Many2one('res.users', string='Người duyệt', readonly=True)
    approved_date = fields.Datetime('Ngày duyệt', readonly=True)
    
    @api.depends('employee_id', 'month')
    def _compute_base_salary(self):
        """Tính lương cơ bản từ hợp đồng"""
        for salary in self:
            if salary.employee_id and salary.month:
                # Tính ngày đầu và cuối tháng
                from datetime import datetime
                month_start = salary.month.replace(day=1)
                # Tính ngày cuối tháng
                if month_start.month == 12:
                    month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
                else:
                    month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)
                
                # Tìm hợp đồng có hiệu lực trong tháng
                # Hợp đồng có hiệu lực nếu: date_start <= ngày cuối tháng VÀ (date_end >= ngày đầu tháng HOẶC date_end = False)
                contract = self.env['hr.contract'].search([
                    ('employee_id', '=', salary.employee_id.id),
                    ('state', '=', 'open'),
                    ('date_start', '<=', month_end),
                    '|',
                    ('date_end', '=', False),
                    ('date_end', '>=', month_start),
                ], limit=1, order='date_start desc')
                salary.base_salary = contract.wage if contract else 0.0
            else:
                salary.base_salary = 0.0
    
    @api.depends('bonus_ids', 'bonus_ids.amount', 'bonus_ids.employee_ids')
    def _compute_bonus_amount(self):
        """Tính tổng thưởng"""
        for salary in self:
            total = 0.0
            # Thưởng cá nhân
            individual_bonuses = salary.bonus_ids.filtered(
                lambda b: b.bonus_type == 'individual' and salary.employee_id in b.employee_ids
            )
            total += sum(individual_bonuses.mapped('amount'))
            
            # Thưởng tập thể
            team_bonuses = salary.bonus_ids.filtered(
                lambda b: b.bonus_type == 'team'
            )
            total += sum(team_bonuses.mapped('amount'))
            
            # Thưởng khác (lễ, tháng 13, ...)
            other_bonuses = salary.bonus_ids.filtered(
                lambda b: b.bonus_type in ['holiday', 'month_13', 'other']
            )
            total += sum(other_bonuses.mapped('amount'))
            
            salary.bonus_amount = total
    
    @api.depends('base_salary', 'bonus_amount')
    def _compute_total_salary(self):
        """Tính tổng lương"""
        for salary in self:
            salary.total_salary = salary.base_salary + salary.bonus_amount
    
    def action_submit(self):
        """Gửi để duyệt (Accountant)"""
        self.write({
            'state': 'submitted',
            'submitted_by': self.env.user.id,
            'submitted_date': fields.Datetime.now(),
        })
    
    def action_approve(self):
        """Duyệt (Manager)"""
        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id,
            'approved_date': fields.Datetime.now(),
        })
    
    def action_post(self):
        """Đăng bút toán kế toán"""
        # Kiểm tra tổng lương > 0 trước khi tạo bút toán
        if self.total_salary <= 0:
            raise UserError(_('Tổng lương phải lớn hơn 0 để tạo bút toán! Vui lòng kiểm tra lương cơ bản và thưởng.'))
        
        if not self.account_move_id:
            # Tạo bút toán
            move = self._create_accounting_entry()
            self.write({
                'state': 'posted',
                'account_move_id': move.id,
            })
        else:
            raise UserError(_('Bút toán đã được tạo rồi!'))
    
    def action_reset_to_draft(self):
        """Quay lại nháp"""
        if self.state == 'posted':
            raise UserError(_('Không thể quay lại nháp khi đã đăng bút toán!'))
        self.write({
            'state': 'draft',
            'submitted_by': False,
            'submitted_date': False,
            'approved_by': False,
            'approved_date': False,
        })
    
    def _create_accounting_entry(self):
        """Tạo bút toán kế toán cho lương"""
        # Tìm journal cho lương
        journal = self.env['account.journal'].search([
            ('code', '=', 'SAL'),
            ('type', '=', 'general'),
        ], limit=1)
        
        if not journal:
            raise UserError(_('Chưa tạo journal cho lương!'))
        
        # Tìm tài khoản "Chi phí nhân viên" (6411) - Tài khoản Nợ
        expense_account = self.env['account.account'].search([
            ('code', '=', '6411'),
        ], limit=1)
        
        if not expense_account:
            raise UserError(_('Chưa tạo tài khoản "Chi phí nhân viên" (6411)!'))
        
        # Tìm tài khoản "Phải trả công nhân viên" (3341) - Tài khoản Có
        payable_account = self.env['account.account'].search([
            ('code', '=', '3341'),
        ], limit=1)
        
        if not payable_account:
            raise UserError(_('Chưa tạo tài khoản "Phải trả công nhân viên" (3341)!'))
        
        # Tạo bút toán với line_ids
        # Lấy currency từ journal hoặc company
        currency = journal.currency_id or self.env.company.currency_id
        
        move_vals = {
            'move_type': 'entry',
            'date': self.month,
            'journal_id': journal.id,
            'company_id': self.env.company.id,
            'currency_id': currency.id,
            'ref': _('Lương %s - %s') % (self.employee_id.name, self.month.strftime('%m/%Y')),
            'line_ids': [
                (0, 0, {
                    'account_id': expense_account.id,
                    'debit': self.total_salary,
                    'credit': 0.0,
                    'name': _('Chi phí lương %s') % self.employee_id.name,
                    'currency_id': currency.id,
                }),
                (0, 0, {
                    'account_id': payable_account.id,
                    'debit': 0.0,
                    'credit': self.total_salary,
                    'name': _('Phải trả lương %s') % self.employee_id.name,
                    'currency_id': currency.id,
                }),
            ],
        }
        
        _logger.info(f'Tạo bút toán lương: journal={journal.code}, expense_account={expense_account.code}, payable_account={payable_account.code}, amount={self.total_salary}')
        
        move = self.env['account.move'].create(move_vals)
        
        # Đảm bảo các dòng được tạo đúng
        _logger.info(f'Bút toán {move.name} đã được tạo với {len(move.line_ids)} dòng kế toán')
        for line in move.line_ids:
            _logger.info(f'  - Dòng: {line.account_id.code} | Nợ: {line.debit} | Có: {line.credit} | {line.name}')
        
        if not move.line_ids:
            raise UserError(_('Không thể tạo các dòng kế toán! Vui lòng kiểm tra lại cấu hình tài khoản.'))
        
        if len(move.line_ids) != 2:
            raise UserError(_('Bút toán phải có đúng 2 dòng kế toán (1 Nợ, 1 Có)!'))
        
        # Post bút toán để có tên sequence và chuyển sang trạng thái "Đã vào sổ"
        if move.state == 'draft':
            try:
                move._post(soft=False)
                _logger.info(f'Bút toán {move.name} đã được đăng (posted), state={move.state}')
            except Exception as e:
                _logger.error(f'Lỗi khi đăng bút toán: {str(e)}')
                raise UserError(_('Không thể đăng bút toán: %s') % str(e))
        
        return move
    
    def action_view_account_move(self):
        """Mở bút toán kế toán"""
        self.ensure_one()
        if not self.account_move_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thông báo',
                    'message': 'Chưa có bút toán kế toán. Vui lòng đăng bút toán trước.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        return {
            'name': 'Bút toán kế toán',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': self.account_move_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

