# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountPrintJournal(models.TransientModel):
    _inherit = "account.print.journal"

    def _print_report(self, data):
        res = super(AccountPrintJournal, self)._print_report(data)
        context = self._context
        if context.get('xls_export'):
            return self.env.ref('accounting_excel_reports.journals_audit_xlsx').report_action(self, data=data)
        else:
            return res
