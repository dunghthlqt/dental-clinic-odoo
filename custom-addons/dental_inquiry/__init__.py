# -*- coding: utf-8 -*-
from . import models
from . import wizard

import re
import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """
    Fix external IDs in views that may have unqualified group references
    This runs after module installation/upgrade to fix any views in database
    
    Note: In Odoo 17, post_init_hook receives 'env' directly (not cr, registry)
    """
    View = env['ir.ui.view']
    
    # Find all views with unqualified external IDs
    views = View.search([
        '|', '|',
        ('arch_db', 'ilike', '%groups="group_dental_inquiry_receptionist%'),
        ('arch_db', 'ilike', '%groups="group_dental_inquiry_dentist%'),
        ('arch_db', 'ilike', '%groups="group_dental_inquiry_manager%'),
    ])
    
    if not views:
        _logger.info("No views found with unqualified external IDs")
        return
    
    _logger.info(f"Found {len(views)} views to fix")
    
    for view in views:
        arch_db = view.arch_db
        if not arch_db:
            continue
        
        arch_str = arch_db
        original_arch = arch_str
        
        # Replace external IDs in groups attribute
        arch_str = re.sub(
            r'groups="group_dental_inquiry_receptionist([,"])',
            r'groups="dental_inquiry.group_dental_inquiry_receptionist\1',
            arch_str
        )
        arch_str = re.sub(
            r'groups="group_dental_inquiry_dentist([,"])',
            r'groups="dental_inquiry.group_dental_inquiry_dentist\1',
            arch_str
        )
        arch_str = re.sub(
            r'groups="group_dental_inquiry_manager([,"])',
            r'groups="dental_inquiry.group_dental_inquiry_manager\1',
            arch_str
        )
        
        # Replace in comma-separated lists
        arch_str = re.sub(
            r',group_dental_inquiry_receptionist([,"])',
            r',dental_inquiry.group_dental_inquiry_receptionist\1',
            arch_str
        )
        arch_str = re.sub(
            r',group_dental_inquiry_dentist([,"])',
            r',dental_inquiry.group_dental_inquiry_dentist\1',
            arch_str
        )
        arch_str = re.sub(
            r',group_dental_inquiry_manager([,"])',
            r',dental_inquiry.group_dental_inquiry_manager\1',
            arch_str
        )
        
        if arch_str != original_arch:
            view.arch_db = arch_str
            _logger.info(f"Fixed view: {view.name} (ID: {view.id})")
    
    _logger.info("Completed fixing views with unqualified external IDs")
