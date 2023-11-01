# -*- coding: utf-8 -*-

from odoo import models, _


class ReportJournalXlsx(models.AbstractModel):
    _name = 'report.accounting_excel_report.journals_audit.xlsx'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_journal']

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Journals Audit")
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'border': True})
        format11 = workbook.add_format({
            'font_size': 12, 'align': 'center', 'bold': True,
            'border': True, 'bg_color': '#FFFFCC'})
        font_size_12_l_bold = workbook.add_format({'font_size': 12, 'align': 'left','bold': True})
        font_size_12_l = workbook.add_format({'font_size': 12, 'align': 'left','bold': False})
        format12 = workbook.add_format({'font_size': 12,'align': 'center'})

        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 3, 20)
        sheet.set_column(4, 4, 40)
        sheet.set_column(5, 7, 20)

        journals = self.env['account.journal'].browse(data['form']['journal_ids'])

        ## Move lines by Journal
        target_move = data['form'].get('target_move', 'all')
        sort_selection = data['form'].get('sort_selection', 'date')
        res = {}
        for j in data['form']['journal_ids']:
            res[j] = self.with_context(data['form'].get('used_context', {})).lines(target_move, j, sort_selection, data)
        journal_lines = res

        sum_debit = self._sum_debit
        sum_credit = self._sum_credit
        get_taxs = self._get_taxes

        row = 0
        for journal in journals:
            row += 1
            sheet.write(row, 0, journal.name, format0)
            row += 2
            sheet.write(row, 0, "Company:", font_size_12_l_bold)
            sheet.write(row, 2, "Journal:", font_size_12_l_bold)
            sheet.write(row, 4, "Entries Sorted By:", font_size_12_l_bold)
            sheet.write(row, 5, "Target Moves:", font_size_12_l_bold)
            row += 1
            sheet.write(row, 0, lines.company_id.name, font_size_12_l)
            sheet.write(row, 2, journal.name, font_size_12_l)
            sheet.write(row, 4, _("Journal Entry Number") if data['form']['sort_selection'] != "date" else _("Date"), font_size_12_l)
            sheet.write(row, 5, _('All Entries') if data['form']['target_move'] == 'all' else _('All Posted Entries'), font_size_12_l)
            row += 2
            sheet.write(row,0, "Move", format11)
            sheet.write(row,1, "Date", format11)
            sheet.write(row,2, "Account", format11)
            sheet.write(row,3, "Partner", format11)
            sheet.write(row,4, "label", format11)
            sheet.write(row,5, "Debit", format11)
            sheet.write(row,6, "Credit", format11)
            sheet.write(row,7, _("Currency") if data['form']['amount_currency'] else _(" "), format11 if data['form']['amount_currency'] else font_size_12_l)
            row += 1

            for aml in journal_lines[journal.id]:
                sheet.write(row, 0, aml.move_id.name,format12)
                sheet.write(row, 1, str(aml.date.strftime("%Y-%m-%d")), format12)
                sheet.write(row, 2, aml.account_id.code, format12)
                sheet.write(row, 3, aml.sudo().partner_id and aml.sudo().partner_id.name and aml.sudo().partner_id.name[:23] or '', format12)
                sheet.write(row, 4, aml.name and aml.name[:35] or '', format12)
                sheet.write(row, 5, aml.debit, format12)
                sheet.write(row, 6, aml.credit, format12)
                sheet.write(row, 7, _(aml.amount_currency) if data['form']['amount_currency'] and aml.amount_currency else _(""), format12)
                row +=1

            sheet.write(row, 4, "Total", format11)
            sheet.write(row, 5, sum_debit(data, journal), format11)
            sheet.write(row, 6, sum_credit(data, journal),format11)
            row +=1
            sheet.merge_range(row, 0, row, 2, "Tax Declaration", format11)
            row +=1
            sheet.write(row, 0, "Name", format11)
            sheet.write(row, 1, "Base Amount", format11)
            sheet.write(row, 2, "Tax Amount", format11)
            row += 1
            taxes = get_taxs(data, journal)
            for tax in taxes:
                sheet.write(row, 0, tax.name, format12)
                sheet.write(row, 1, taxes[tax]['base_amount'], format12)
                sheet.write(row, 2, taxes[tax]['tax_amount'], format12)
                row +=1







