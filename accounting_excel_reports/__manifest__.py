# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo 13 Accounting Excel Reports',
    'version': '13.0.1.0.0',
    'category': 'Invoicing Management',
    'summary': 'Able to export Accountig PDF Reports in Excel',
    'sequence': '10',
    'author': 'Sokream Phan - A2A Digital, Odoo Mates, Odoo SA',
    'company': 'A2A Digital',
    'website': 'https://a2a-digital.com/',
    'depends': [
        'accounting_pdf_reports',
        'report_xlsx',
    ],
    'data': [
        'wizards/account_report_common_view.xml',
        'reports/reports.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
