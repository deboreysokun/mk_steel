# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo 13 Accounting Daily Cash book Reports',
    'version': '13.0.1.0.0',
    'category': 'Invoicing Management',
    'summary': '',
    'sequence': '10',
    'author': 'A2A Digital, Odoo SA,Cybrosys Techno Solutions',
    'website': 'https://a2a-digital.com/',
    'depends': [
        'account',
    ],
    'data': [
        'report/account_cash_book_view.xml',
        'wizard/account_cash_book_wizard_view.xml',

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
