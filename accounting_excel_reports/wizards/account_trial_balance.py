# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountBalanceReport(models.TransientModel):
    _inherit = "account.balance.report"

    def _print_report(self, data):
        res = super(AccountBalanceReport, self)._print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        context = self._context
        if context.get('xls_export'):
            return self.env.ref('accounting_excel_reports.trial_balance_xlsx').report_action(records, data=data)
        else:
            return res
