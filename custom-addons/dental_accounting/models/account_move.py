# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import get_lang, email_split
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    dental_treatment_id = fields.Many2one(
        'dental.treatment',
        string='Điều trị liên quan',
        help='Điều trị liên quan đến invoice này'
    )
    
    treatment_total_cost = fields.Float(
        'Tổng chi phí điều trị',
        related='dental_treatment_id.total_cost',
        readonly=True,
        help='Tổng chi phí của điều trị'
    )
    
    treatment_paid_amount = fields.Float(
        'Đã thanh toán',
        compute='_compute_treatment_paid',
        store=True,
        help='Tổng số tiền đã thanh toán cho điều trị này'
    )
    
    treatment_remaining = fields.Float(
        'Số tiền còn lại',
        compute='_compute_treatment_remaining',
        store=True,
        help='Số tiền còn lại cần thanh toán = Tổng chi phí - Đã thanh toán'
    )
    
    @api.depends('dental_treatment_id', 'dental_treatment_id.revenue')
    def _compute_treatment_paid(self):
        """Tính tổng số tiền đã thanh toán cho treatment"""
        for invoice in self:
            if invoice.dental_treatment_id:
                invoice.treatment_paid_amount = invoice.dental_treatment_id.revenue
            else:
                invoice.treatment_paid_amount = 0.0
    
    @api.depends('treatment_total_cost', 'treatment_paid_amount')
    def _compute_treatment_remaining(self):
        """Tính số tiền còn lại"""
        for invoice in self:
            invoice.treatment_remaining = invoice.treatment_total_cost - invoice.treatment_paid_amount
    
    @api.onchange('partner_id')
    def _onchange_partner_id_dental(self):
        """Filter treatments theo partner khi chọn partner"""
        if self.partner_id:
            # Tìm dental patient từ partner
            dental_patient = self.env['dental.patient'].search([
                ('phone', '=', self.partner_id.phone)
            ], limit=1)
            
            if dental_patient:
                # Domain để chỉ hiển thị treatments của patient này
                return {
                    'domain': {
                        'dental_treatment_id': [('patient_id', '=', dental_patient.id)]
                    }
                }
    
    def action_print_invoice(self):
        """Mở PDF preview của invoice trong tab mới (không tải file)"""
        self.ensure_one()
        
        # Tìm report action cho invoice
        report = self.env['ir.actions.report']._get_report_from_name('account.report_invoice')
        if not report:
            # Fallback: tìm report mặc định cho account.move
            report = self.env['ir.actions.report'].search([
                ('model', '=', 'account.move'),
                ('report_type', '=', 'qweb-pdf')
            ], limit=1)
        
        if report:
            # Sử dụng report_action() để mở PDF preview
            # Thêm target='new' vào context để mở trong tab mới
            action = report.report_action(self, config=False)
            if isinstance(action, dict):
                # Đảm bảo target là 'new' để mở trong tab mới
                action['target'] = 'new'
            return action
        else:
            # Fallback: sử dụng URL trực tiếp
            return {
                'type': 'ir.actions.act_url',
                'url': f'/report/pdf/account.report_invoice/{self.id}',
                'target': 'new',
            }


class AccountMoveSend(models.TransientModel):
    """Override account.move.send wizard để fix lỗi mail template render_model = False"""
    _inherit = 'account.move.send'
    
    def _get_default_mail_lang(self, move=None, mail_template=None):
        """Override để xử lý trường hợp mail_template có render_model = False
        
        Signature: _get_default_mail_lang(move, mail_template=None)
        """
        if not mail_template:
            return get_lang(self.env).code
        
        # Kiểm tra nếu mail_template tồn tại
        if not mail_template.exists():
            return get_lang(self.env).code
        
        # Thử gọi method gốc, nếu có lỗi thì trả về language mặc định
        try:
            return super()._get_default_mail_lang(move, mail_template)
        except (KeyError, ValueError, AttributeError, TypeError) as e:
            # Nếu có lỗi (có thể do render_model = False), trả về language mặc định
            _logger.warning(f"Error getting mail lang from template {mail_template.id}: {e}. Using default language.")
            return get_lang(self.env).code
        except Exception as e:
            # Catch all other exceptions
            _logger.warning(f"Unexpected error getting mail lang: {e}. Using default language.")
            return get_lang(self.env).code
    
    @api.depends('mail_template_id')
    def _compute_mail_lang(self):
        """Override để xử lý lỗi khi compute mail_lang"""
        for wizard in self:
            if wizard.mode == 'invoice_single':
                try:
                    # Lấy move đầu tiên và mail_template
                    move = wizard.move_ids[0] if wizard.move_ids else None
                    mail_template = wizard.mail_template_id
                    
                    if move and mail_template:
                        wizard.mail_lang = self._get_default_mail_lang(move, mail_template)
                    else:
                        wizard.mail_lang = get_lang(self.env).code
                except Exception as e:
                    _logger.warning(f"Error computing mail_lang: {e}. Using default language.")
                    wizard.mail_lang = get_lang(self.env).code
            else:
                wizard.mail_lang = get_lang(self.env).code
    
    def _get_mail_default_field_value_from_template(self, mail_template, lang, move, field, **kwargs):
        """Override để xử lý trường hợp mail_template có render_model = False"""
        if not mail_template:
            return
        
        # Kiểm tra nếu render_model không hợp lệ
        try:
            render_model = mail_template.render_model
            if not render_model or render_model == 'False' or render_model is False:
                # Nếu render_model không hợp lệ, trả về None hoặc giá trị mặc định
                _logger.warning(f"Mail template {mail_template.id} has invalid render_model: {render_model}. Skipping template rendering.")
                return None
        except Exception as e:
            _logger.warning(f"Error checking render_model for template {mail_template.id}: {e}. Skipping template rendering.")
            return None
        
        # Gọi method gốc nếu render_model hợp lệ
        try:
            return super()._get_mail_default_field_value_from_template(mail_template, lang, move, field, **kwargs)
        except (KeyError, ValueError, AttributeError, TypeError) as e:
            _logger.warning(f"Error rendering field {field} from template {mail_template.id}: {e}.")
            return None
        except Exception as e:
            _logger.warning(f"Unexpected error rendering field {field} from template {mail_template.id}: {e}.")
            return None
    
    def _get_default_mail_partner_ids(self, move, mail_template, mail_lang):
        """Override để xử lý trường hợp mail_template có render_model = False"""
        partners = self.env['res.partner'].with_company(move.company_id)
        
        if not mail_template:
            return partners
        
        # Kiểm tra render_model trước khi render
        try:
            render_model = mail_template.render_model
            if not render_model or render_model == 'False' or render_model is False:
                _logger.warning(f"Mail template {mail_template.id} has invalid render_model: {render_model}. Returning empty partners.")
                return partners
        except Exception as e:
            _logger.warning(f"Error checking render_model for template {mail_template.id}: {e}. Returning empty partners.")
            return partners
        
        # Gọi method gốc nếu render_model hợp lệ, nhưng xử lý lỗi
        try:
            return super()._get_default_mail_partner_ids(move, mail_template, mail_lang)
        except (KeyError, ValueError, AttributeError, TypeError) as e:
            _logger.warning(f"Error getting mail partner ids from template {mail_template.id}: {e}. Returning empty partners.")
            return partners
        except Exception as e:
            _logger.warning(f"Unexpected error getting mail partner ids: {e}. Returning empty partners.")
            return partners
    
    @api.depends('mail_template_id', 'mail_lang')
    def _compute_mail_partner_ids(self):
        """Override để xử lý lỗi khi compute mail_partner_ids"""
        for wizard in self:
            if wizard.mode == 'invoice_single' and wizard.mail_template_id:
                try:
                    # Lấy move đầu tiên từ move_ids
                    move = wizard.move_ids[0] if wizard.move_ids else None
                    mail_template = wizard.mail_template_id
                    mail_lang = wizard.mail_lang
                    
                    if move and mail_template:
                        wizard.mail_partner_ids = self._get_default_mail_partner_ids(move, mail_template, mail_lang)
                    else:
                        wizard.mail_partner_ids = None
                except Exception as e:
                    _logger.warning(f"Error computing mail_partner_ids: {e}. Using None.")
                    wizard.mail_partner_ids = None
            else:
                wizard.mail_partner_ids = None
    
    @api.model
    def _hook_invoice_document_after_pdf_report_render(self, invoice, invoice_data):
        """Override để xử lý lỗi PyPDF2 DeprecationError khi generate PDF invoice
        
        Lỗi xảy ra do PyPDF2 3.0.0 đã deprecated method cloneReaderDocumentRoot.
        Method này được gọi từ account_edi_ubl_cii module khi generate PDF với EDI.
        
        Giải pháp: Catch exception và bỏ qua phần EDI processing, PDF vẫn được generate bình thường.
        """
        try:
            # Thử gọi method gốc (có thể từ account_edi_ubl_cii hoặc account module)
            return super()._hook_invoice_document_after_pdf_report_render(invoice, invoice_data)
        except Exception as e:
            # Nếu có lỗi PyPDF2 hoặc bất kỳ lỗi nào khác, log và bỏ qua
            # PDF đã được generate, chỉ là không thể thêm EDI attachment vào PDF
            error_type = type(e).__name__
            if 'DeprecationError' in error_type or 'PyPDF2' in str(e):
                _logger.warning(f"PyPDF2 compatibility issue when processing EDI for invoice {invoice.id}: {e}. PDF generation will continue without EDI attachment.")
            else:
                _logger.warning(f"Error in _hook_invoice_document_after_pdf_report_render for invoice {invoice.id}: {e}. PDF generation will continue.")
            # Trả về None để không làm gián đoạn quá trình generate PDF
            return None

