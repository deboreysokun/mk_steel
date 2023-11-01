# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _


class AccountingReport(models.TransientModel):
    _inherit = "accounting.report"

    def _print_report(self, data):
        data['form'].update(self.read(['date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp', 'account_report_id', 'enable_filter', 'label_filter', 'target_move'])[0])
        context = self._context
        if context.get('xls_export'):
            return self.env.ref('accounting_excel_reports.profitloss_xlsx').report_action(self, data=data, config=False)
        else:
            return self.env.ref('accounting_pdf_reports.action_report_financial').report_action(self, data=data, config=False)
