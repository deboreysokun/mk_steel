# -*- coding: utf-8 -*-
import time
from datetime import datetime
from odoo import api, models, _


class ReportAgedPartnerBalanceXlsx(models.AbstractModel):
    _name = 'report.accounting_excel_report.aged_partner_balance.xlsx'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_agedpartnerbalance']

    def generate_xlsx_report(self, workbook, data, lines):
        target_move = data['form'].get('target_move', 'all')
        date_from = data['form'].get('date_from', time.strftime('%Y-%m-%d'))

        if data['form']['result_selection'] == 'customer':
            account_type = ['receivable']
        elif data['form']['result_selection'] == 'supplier':
            account_type = ['payable']
        else:
            account_type = ['payable', 'receivable']

        partner_move_line, total, dummy = self._get_partner_move_lines(account_type, date_from, target_move, data['form']['period_length'])
        sheet = workbook.add_worksheet('Aged Partner Balance')
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'border': True})
        format11 = workbook.add_format({
            'font_size': 12, 'align': 'center', 'bold': True,
            'border': True, 'bg_color': '#FFFFCC'})
        format11_center = workbook.add_format({
        'font_size': 12, 'align': 'center', 'bold': False,
        'border': True, 'bg_color': '#FFFFCC'})
        font_size_12_l_bold = workbook.add_format({'font_size': 12, 'align': 'left','bold': True})
        font_size_12_l = workbook.add_format({'font_size': 12, 'align': 'left','bold': False})
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 7, 20)
        sheet.merge_range(1, 3, 2, 6, 'Aged Partner Balance', format0)

        sheet.write(4, 0, 'Start Date:', format11)
        sheet.write(5, 0, date_from ,format11_center)
        sheet.write(6, 0, ("Partner's:"), format11)
        sheet.write(7, 0, _('Receivable Accounts') if lines.result_selection == 'customer' else (_('Payable Accounts') if lines.result_selection == 'supplier' else _('Receivable and Payable Accounts')),format11_center)

        sheet.write(4, 1, 'Period Length (Days):', format11)
        sheet.write(5, 1, lines.period_length, format11_center)
        sheet.write(6, 1, ('Target Move:'), format11)
        sheet.write(7, 1,_('All Entries') if lines.target_move == 'all' else _('All Posted Entries'),format11_center)

        sheet.write(9, 0, 'Partners', format11)
        sheet.write(9, 1, 'Not Due', format11)
        sheet.write(9, 2, data['form']['4']['name'], format11)
        sheet.write(9, 3, data['form']['3']['name'], format11)
        sheet.write(9, 4, data['form']['2']['name'], format11)
        sheet.write(9, 5, data['form']['1']['name'], format11)
        sheet.write(9, 6, data['form']['0']['name'], format11)
        sheet.write(9, 7, 'Total', format11)

        if partner_move_line:
            sheet.write(10, 0, 'Account Total', font_size_12_l_bold)
            sheet.write(10, 1, total[6], font_size_12_l_bold)
            sheet.write(10, 2, total[4], font_size_12_l_bold)
            sheet.write(10, 3, total[3], font_size_12_l_bold)
            sheet.write(10, 4, total[2], font_size_12_l_bold)
            sheet.write(10, 5, total[1], font_size_12_l_bold)
            sheet.write(10, 6, total[0], font_size_12_l_bold)
            sheet.write(10, 7, total[5], font_size_12_l_bold)

        row = 11
        for partner in partner_move_line:
            sheet.write(row, 0, partner['name'], font_size_12_l)
            sheet.write(row, 1, partner['direction'], font_size_12_l)
            sheet.write(row, 2, partner['4'], font_size_12_l)
            sheet.write(row, 3, partner['3'], font_size_12_l)
            sheet.write(row, 4, partner['2'], font_size_12_l)
            sheet.write(row, 5, partner['1'], font_size_12_l)
            sheet.write(row, 6, partner['0'], font_size_12_l)
            sheet.write(row, 7, partner['total'], font_size_12_l)
            row += 1

