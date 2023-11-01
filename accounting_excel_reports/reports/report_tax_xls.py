# -*- coding: utf-8 -*-

from odoo import models, _


class ReportTaxXls(models.AbstractModel):
    _name = 'report.accounting_excel_report.tax_report.xlsx'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_tax']

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Tax Report")
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'border': True})
        format11 = workbook.add_format({
            'font_size': 12, 'align': 'center', 'bold': True,
            'border': True, 'bg_color': '#FFFFCC'})
        format12_bold = workbook.add_format({'font_size': 12,'align': 'center', 'bold': True, 'text_wrap': True})
        sheet.set_column(0, 6, 20)
        sheet.merge_range(1, 0, 0, 2, "Tax Report", format0)
        sheet.write(3, 0, "Company:",format11)
        sheet.write(4, 0, lines.company_id.name, format11)
        sheet.write(3, 1, _('Date From: ' + str(lines.date_from.strftime("%Y-%m-%d"))),format11)
        sheet.write(4, 1, _('Date To: '+ str(lines.date_to.strftime("%Y-%m-%d"))), format11)

        tax_lines = self.get_lines(data.get('form'))

        sheet.write(6,0, "Sale", format11)
        sheet.write(6,1, "Net", format11)
        sheet.write(6,2, "Tax", format11)
        row = 7
        for line in tax_lines['sale']:
            sheet.write(row, 0, line.get('name'), format12_bold)
            sheet.write(row, 1, line.get('net'), format12_bold)
            sheet.write(row, 2, line.get('tax'), format12_bold)
            row += 1
        sheet.write(row, 0, "Purchase",format11)
        sheet.write(row, 1, "Net", format11)
        sheet.write(row, 2, "Tax", format11)
        row += 1
        for line in tax_lines['purchase']:
            sheet.write(row, 0, line.get('name'), format12_bold)
            sheet.write(row, 1, line.get('net'), format12_bold)
            sheet.write(row, 2, line.get('tax'), format12_bold)
            row += 1
