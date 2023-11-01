# -*- coding: utf-8 -*-

from odoo import fields, models, _


class AccountReportGeneralLedger(models.TransientModel):
    _inherit = "account.report.general.ledger"

    def _print_report(self, data):
        res = super(AccountReportGeneralLedger, self)._print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        context = self._context
        if context.get("xls_export"):
            return self.env.ref('accounting_excel_reports.general_ledger_xlsx').report_action(records, data=data)
        else:
            return res