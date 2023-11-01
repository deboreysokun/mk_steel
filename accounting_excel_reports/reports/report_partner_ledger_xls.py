# -*- coding: utf-8 -*-
from odoo import api, models, _


class ReportPartnerLedgerXls(models.AbstractModel):
    _name = 'report.accounting_excel_report.partner_ledger.xlsx'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_partnerledger']

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Partner ledger")
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True, 'border': True})
        format11 = workbook.add_format({
            'font_size': 12, 'align': 'center', 'bold': True,
            'border': True, 'bg_color': '#FFFFCC'})
        font_size_12_l_bold = workbook.add_format({'font_size': 12, 'align': 'left','bold': True})
        font_size_12_l = workbook.add_format({'font_size': 12, 'align': 'left','bold': False})
        format12 = workbook.add_format({'font_size': 12,'align': 'center'})
        format12_bold = workbook.add_format({'font_size': 12,'align': 'center', 'bold': True})
        sheet.set_column(3, 3, 65)
        sheet.set_column(0, 2, 15)
        sheet.set_column(4, 7, 15)
        sheet.merge_range(1, 0, 0, 3, 'Partner Ledger', format0)

        data['computed'] = {}

        obj_partner = self.env['res.partner']
        query_get_data = self.env['account.move.line'].with_context(data['form'].get('used_context', {}))._query_get()
        data['computed']['move_state'] = ['draft', 'posted']
        if data['form'].get('target_move', 'all') == 'posted':
            data['computed']['move_state'] = ['posted']
        result_selection = data['form'].get('result_selection', 'customer')
        if result_selection == 'supplier':
            data['computed']['ACCOUNT_TYPE'] = ['payable']
        elif result_selection == 'customer':
            data['computed']['ACCOUNT_TYPE'] = ['receivable']
        else:
            data['computed']['ACCOUNT_TYPE'] = ['payable', 'receivable']

        self.env.cr.execute("""
            SELECT a.id
            FROM account_account a
            WHERE a.internal_type IN %s
            AND NOT a.deprecated""", (tuple(data['computed']['ACCOUNT_TYPE']),))
        data['computed']['account_ids'] = [a for (a,) in self.env.cr.fetchall()]
        params = [tuple(data['computed']['move_state']), tuple(data['computed']['account_ids'])] + query_get_data[2]
        reconcile_clause = "" if data['form']['reconciled'] else ' AND "account_move_line".full_reconcile_id IS NULL '
        query = """
            SELECT DISTINCT "account_move_line".partner_id
            FROM """ + query_get_data[0] + """, account_account AS account, account_move AS am
            WHERE "account_move_line".partner_id IS NOT NULL
                AND "account_move_line".account_id = account.id
                AND am.id = "account_move_line".move_id
                AND am.state IN %s
                AND "account_move_line".account_id IN %s
                AND NOT account.deprecated
                AND """ + query_get_data[1] + reconcile_clause
        self.env.cr.execute(query, tuple(params))
        partner_ids = [res['partner_id'] for res in self.env.cr.dictfetchall()]
        partners = obj_partner.browse(partner_ids)
        partners = sorted(partners, key=lambda x: (x.ref or '', x.name or ''))
        move_lines = self._lines
        sum_partner = self._sum_partner

        row = 2
        for partner in partners:
            row += 2
            sheet.write(row, 0, "Company:", font_size_12_l_bold)
            sheet.write(row, 1, _("Date From:") if lines.date_from else _(" "),font_size_12_l_bold)
            sheet.write(row, 2, _(str(lines.date_from.strftime("%Y-%m-%d"))) if lines.date_from else _(" "),font_size_12_l_bold)
            sheet.write(row, 3, "Target Moves:", font_size_12_l_bold)
            row += 1
            sheet.write(row, 0, lines.company_id.name, font_size_12_l)
            sheet.write(row, 1, _("Date To:") if lines.date_to else _(" "),font_size_12_l_bold)
            sheet.write(row, 2, _(str(lines.date_to.strftime("%Y-%m-%d"))) if lines.date_to else _(" "),font_size_12_l_bold)
            sheet.write(row, 3, _('All Entries') if data['form']['target_move'] == 'all' else _('All Posted Entries'), font_size_12_l)
            row += 2
            sheet.write(row,0, "Date", format11)
            sheet.write(row,1, "JRNL", format11)
            sheet.write(row,2, "Account", format11)
            sheet.write(row,3, "Ref", format11)
            sheet.write(row,4, "Debit", format11)
            sheet.write(row,5, "Credit", format11)
            sheet.write(row,6, "Balance", format11)
            sheet.write(row,7, _("Currency") if data['form']['amount_currency'] else _(" "), format11 if data['form']['amount_currency'] else font_size_12_l)
            row += 1
            sheet.merge_range(row, 0, row, 2, partner.name, format12_bold)
            sheet.write(row, 4, sum_partner(data, partner, 'debit'), format12_bold)
            sheet.write(row, 5, sum_partner(data, partner, 'credit'), format12_bold)
            sheet.write(row, 6, sum_partner(data, partner, 'debit - credit'), format12_bold)
            row +=1
            for aml in move_lines(data, partner):
                sheet.write(row,0, str(aml['date'].strftime("%Y-%m-%d")), format12)
                sheet.write(row,1, aml['code'], format12)
                sheet.write(row,2, aml['a_code'], format12)
                sheet.write(row,3, aml['displayed_name'], font_size_12_l)
                sheet.write(row,4, aml['debit'], format12)
                sheet.write(row,5, aml['credit'], format12)
                sheet.write(row,6, aml['progress'], format12)
                if data['form']['amount_currency']:
                    sheet.write(row,7,_(aml['amount_currency'] if aml['currency_id'] else _(" ")), format12)
                row +=1
