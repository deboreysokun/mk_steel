# -*- coding: utf-8 -*-

from odoo import fields, models, _


class AccountPartnerLedger(models.TransientModel):
    _inherit = "account.report.partner.ledger"

    def _print_report(self, data):
        res = super(AccountPartnerLedger, self)._print_report(data)
        context = self._context
        if context.get('xls_export'):
            return self.env.ref('accounting_excel_reports.partner_ledger_xlsx').report_action(self, data=data)
        else:
            return res

