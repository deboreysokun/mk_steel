# -*- coding: utf-8 -*-

from odoo import models, _
from datetime import datetime, timedelta
import calendar

class ProfitlossXls(models.AbstractModel):
    _name = 'report.accounting_excel_report.export.xlsx'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_financial']

    def generate_xlsx_report(self, workbook, data, lines):
        report_name = lines.account_report_id.name
        account_line = self.get_account_lines(data.get('form'))
        comp = lines.company_id.name
        sheet = workbook.add_worksheet(lines.account_report_id.name)
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'border': True})
        format11 = workbook.add_format({
            'font_size': 12, 'align': 'center', 'bold': True,
            'border': True, 'bg_color': '#FFFFCC'})
        font_size_12_l_bold = workbook.add_format({'font_size': 12, 'align': 'left','bold': True})
        font_size_12_l = workbook.add_format({'font_size': 12, 'align': 'left','bold': False})
        format12 = workbook.add_format({'font_size': 12,'align': 'left', 'border': True, 'bg_color': '#FFFFCC', 'bold': True,})
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 3, 20)
        sheet.merge_range(1, 3, 2, 6, report_name, format0)
        sheet.merge_range(3, 3, 3, 6, comp, format11)
        sheet.write(4,0, 'Target Move', format11)
        sheet.write(5, 0, _('All Entries') if lines.target_move == 'all' else _('All Posted Entries'),format11)
        sheet.write(4, 1, _('Date From: ' + str(lines.date_from.strftime("%Y-%m-%d"))) if lines.date_from else _(''),format12 if lines.date_from else font_size_12_l)
        sheet.write(5, 1, _('Date To: '+ str(lines.date_to.strftime("%Y-%m-%d"))) if lines.date_to else _(''),format12 if lines.date_to else font_size_12_l)
        sheet.write(7, 0, 'Name', format11)

        col = 1
        if lines.debit_credit:
            sheet.write(7, col, 'Debit', format11 )
            sheet.write(7, col + 1, 'Credit', format11 )
            sheet.write(7, col + 2, 'Balance', format11)
        elif lines.enable_filter and not lines.debit_credit:
            sheet.write(7, col, 'Balance', format11 )
            sheet.write(7, col + 1, lines.label_filter, format11 )
        else:
            sheet.write(7, col, 'Balance', format11)
        row= 8
        if not lines.debit_credit and not lines.enable_filter:
            for account in account_line:
                if account['level'] != 0:
                    sheet.write(row, 0, account['name'], font_size_12_l if int(account['level']) > 3 else font_size_12_l_bold)
                    sheet.write(row, 1, account['balance'], font_size_12_l if int(account['level']) > 3 else font_size_12_l_bold)
                    row +=1

        if lines.enable_filter and not lines.debit_credit :
            for account in account_line:
                if account['level'] != 0:
                    sheet.write(row, 0, account['name'], font_size_12_l if int(account['level']) > 3 else font_size_12_l_bold)
                    sheet.write(row, 1, account['balance'], font_size_12_l if int(account['level']) > 3 else font_size_12_l_bold)
                    sheet.write(row, 2, account['balance_cmp'], font_size_12_l if int(account['level']) > 3 else font_size_12_l_bold)
                    row +=1

        if lines.debit_credit:
            for account in account_line:
                if account['level'] != 0:
                    sheet.write(row, 0, account['name'], font_size_12_l if int(account['level']) > 3 else font_size_12_l_bold)
                    sheet.write(row, 1, account['debit'], font_size_12_l if int(account['level']) > 3 else font_size_12_l_bold)
                    sheet.write(row, 2, account['credit'], font_size_12_l if int(account['level']) > 3 else font_size_12_l_bold)
                    sheet.write(row, 3, account['balance'], font_size_12_l if int(account['level']) > 3 else font_size_12_l_bold)
                    row +=1
