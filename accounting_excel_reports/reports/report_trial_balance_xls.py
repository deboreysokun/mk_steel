# -*- coding: utf-8 -*-

import time
from odoo import api, models, _


class ReportTrialBalanceXls(models.AbstractModel):
    _name = 'report.accounting_excel_report.trial_balance.xlsx'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_trialbalance']

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Trial Balance")
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'border': True})
        format11 = workbook.add_format({
            'font_size': 12, 'align': 'center', 'bold': True,
            'border': True, 'bg_color': '#FFFFCC'})
        font_size_12_l = workbook.add_format({'font_size': 12, 'align': 'left','bold': False, 'text_wrap': True})
        format12 = workbook.add_format({'font_size': 12,'align': 'center'})
        sheet.set_column(0, 0, 20)
        sheet.set_column(1, 1 , 40)
        sheet.set_column(2, 6, 20)
        sheet.merge_range(1, 0, 0, 2, str(lines.company_id.name)+ ":" + " General Ledger", format0)

        sheet.write(4,0, 'Display Account:', format11)
        sheet.write(5, 0, _('All accounts') if lines.display_account == 'all' else _(_('With movements') if lines.display_account == 'movement' else _("With balance not equal to zero")), format11)
        sheet.write(4, 1, ('Target Move:'), format11)
        sheet.write(5, 1,_('All Entries') if lines.target_move == 'all' else _('All Posted Entries'),format11)
        sheet.write(4, 2, _('Date From: ' + str(lines.date_from.strftime("%Y-%m-%d"))) if lines.date_from else _(''),format11 if lines.date_from else font_size_12_l)
        sheet.write(5, 2, _('Date To: '+ str(lines.date_to.strftime("%Y-%m-%d"))) if lines.date_to else _(''),format11 if lines.date_to else font_size_12_l)

        row = 9
        sheet.write(row, 0, "Code", format11)
        sheet.write(row, 1, "Account", format11)
        sheet.write(row, 2, "Debit", format11)
        sheet.write(row, 3, "Credit", format11)
        sheet.write(row, 4, "Balance", format11)

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        display_account = data['form'].get('display_account')
        accounts = docs if self.model == 'account.account' else self.env['account.account'].search([])
        account_res = self.with_context(data['form'].get('used_context'))._get_accounts(accounts, display_account)
        row +=1
        for account in account_res:
            sheet.write(row, 0, account["code"], format12)
            sheet.write(row, 1, account["name"], font_size_12_l)
            sheet.write(row, 2, account["debit"], format12)
            sheet.write(row, 3, account["credit"], format12)
            sheet.write(row, 4, account["balance"], format12)
            row +=1


