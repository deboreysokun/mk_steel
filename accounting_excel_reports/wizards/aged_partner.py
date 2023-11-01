
from odoo import api, fields, models, _

class AccountAgedTrialBalance(models.TransientModel):
    _inherit = 'account.aged.trial.balance'

    def _print_report(self, data):
        res = super(AccountAgedTrialBalance, self)._print_report(data)
        context = self._context
        if context.get('xls_export'):
            return self.env.ref('accounting_excel_reports.aged_partner_balance_xlsx').report_action(self, data=data)
        else:
            return res

