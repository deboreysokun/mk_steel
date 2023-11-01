# -*- coding: utf-8 -*-

from odoo import models


class AccountTaxReport(models.TransientModel):
    _inherit = "account.tax.report"

    def _print_report(self, data):
        res = super(AccountTaxReport, self)._print_report(data)
        context = self._context
        if context.get("xls_export"):
            return self.env.ref('accounting_excel_reports.tax_report_xlsx').report_action(self, data=data)
        else:
            return res
