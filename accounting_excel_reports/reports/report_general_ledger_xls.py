# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportGeneralLedgerXls(models.AbstractModel):
    _name = 'report.accounting_excel_report.general_ledger.xlsx'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_general_ledger']

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Genreal ledger")
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'border': True})
        format11 = workbook.add_format({
            'font_size': 12, 'align': 'center', 'bold': True,
            'border': True, 'bg_color': '#FFFFCC'})
        font_size_12_l_bold = workbook.add_format({'font_size': 12, 'align': 'left','bold': True, 'text_wrap': True})
        font_size_12_l = workbook.add_format({'font_size': 12, 'align': 'left','bold': False, 'text_wrap': True})
        format12 = workbook.add_format({'font_size': 12,'align': 'center'})
        format12_bold = workbook.add_format({'font_size': 12,'align': 'center', 'bold': True, 'text_wrap': True})
        sheet.set_column(3, 3, 40)
        sheet.set_column(0, 0, 25)
        sheet.set_column(1, 2, 15)
        sheet.set_column(4, 5, 25)
        sheet.set_column(6, 8, 15)
        sheet.merge_range(0, 1, 0, 3, 'Genreal Ledger', format0)

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        init_balance = data['form'].get('initial_balance', True)
        sortby = data['form'].get('sortby', 'sort_date')
        display_account = data['form']['display_account']
        codes = []
        if data['form'].get('journal_ids', False):
            codes = [journal.code for journal in self.env['account.journal'].search([('id', 'in', data['form']['journal_ids'])])]

        accounts = docs if self.model == 'account.account' else self.env['account.account'].search([])
        accounts_res = self.with_context(data['form'].get('used_context',{}))._get_account_move_entry(accounts, init_balance, sortby, display_account)

        print_journal = codes

        row = 2
        for account in accounts_res:
            row += 2
            sheet.write(row, 0, "Journals:", font_size_12_l_bold)
            sheet.write(row, 2, _("Sorted By:") if lines.sortby else _(" "),font_size_12_l_bold)
            sheet.write(row, 3, _("Date From: " + str(lines.date_from.strftime("%Y-%m-%d"))) if lines.date_from else _(" "),font_size_12_l_bold)
            sheet.write(row, 4, "Display Account:", font_size_12_l_bold)
            sheet.write(row, 5, "Target Moves:", font_size_12_l_bold)
            row += 1
            sheet.set_row(row, 50)
            sheet.merge_range(row, 0 , row, 1, str(', '.join([ lt or '' for lt in print_journal])), font_size_12_l_bold)
            sheet.write(row, 2, _("Date") if lines.sortby == 'sort_date' else _("Journal and Partner "),font_size_12_l_bold)
            sheet.write(row, 3, _("Date To: " + str(lines.date_to.strftime("%Y-%m-%d"))) if lines.date_to else _(" "),font_size_12_l_bold)
            sheet.write(row, 4, _('All accounts') if lines.display_account == 'all' else _(_('With movements') if lines.display_account == 'movement' else _("With balance not equal to zero")), font_size_12_l_bold)
            sheet.write(row, 5, _('All Entries') if lines.target_move == 'all' else _('All Posted Entries'), font_size_12_l_bold)
            row += 2
            sheet.write(row,0, "Date", format11)
            sheet.write(row,1, "JRNL", format11)
            sheet.write(row,2, "Partner", format11)
            sheet.write(row,3, "Ref", format11)
            sheet.write(row,4, "Move", format11)
            sheet.write(row,5, "Entry Label", format11)
            sheet.write(row,6, "Debit", format11)
            sheet.write(row,7, "Credit", format11)
            sheet.write(row,8, "Balance", format11)
            sheet.write(row,9, "Currency", format11)
            row += 1
            sheet.write(row, 0, str(account['code'] + ' ' + str(account['name'])), format12_bold)
            sheet.write(row, 6, account['debit'], format12_bold)
            sheet.write(row, 7, account['credit'], format12_bold)
            sheet.write(row, 8, account['balance'], format12_bold)
            row +=1

            for aml in account['move_lines']:
                sheet.write(row,0, str(aml['ldate'].strftime("%Y-%m-%d")), format12)
                sheet.write(row,1, aml['lcode'], format12)
                sheet.write(row,2, aml['partner_name'], format12)
                sheet.write(row,3, aml['lref'], font_size_12_l)
                sheet.write(row,4, aml['move_name'], format12)
                sheet.write(row,5, aml['lname'], format12)
                sheet.write(row,6, aml['debit'], format12)
                sheet.write(row,7, aml['credit'], format12)
                sheet.write(row,8, aml['balance'], format12)
                sheet.write(row,9, _(str(aml['amount_currency']) + ' ' + str(aml['currency_code'])) if aml['amount_currency'] > 0.00 else _(" "), format12)
                row +=1
