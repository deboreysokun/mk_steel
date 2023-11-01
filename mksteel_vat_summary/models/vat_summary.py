# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class VatSummary(models.Model):
    _name = 'vat.summary'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Vat Summary'

    name = fields.Char(store=True, required=True)
    vat_summary_ids = fields.One2many(string="Vat Summary",
        comodel_name='vat.summary.line',
        inverse_name="vat_summary_id",
        copy=False,)
    forward_balance = fields.Float()
    end_balance = fields.Float(compute="_compute_balance", store=True,help="Total Vat In minus Total Vat Out.")
    exchange_rate = fields.Float(string="Exchange Rate", default=1.0 ,store=True)
    end_balance_usd = fields.Float(String="Total USD", compute="_compute_balance_usd")
    active = fields.Boolean('Active', default=True)

    @api.depends('vat_summary_ids', 'forward_balance', 'vat_summary_ids.vat_amount','vat_summary_ids.vat_in')
    def _compute_balance(self):
        for line in self:
            total_vat_amount_out = sum([l.vat_amount for l in line.vat_summary_ids])
            total_vat_in = sum([l.vat_in for l in line.vat_summary_ids])
            line.end_balance = total_vat_in - total_vat_amount_out

    @api.onchange("exchange_rate")
    def _compute_balance_usd(self):
        for record in self:
            record.end_balance_usd = record.end_balance / record.exchange_rate


class VatSummaryLine(models.Model):
    _name = 'vat.summary.line'

    vat_summary_id = fields.Many2one('vat.summary')
    number_id = fields.Char(string='Inv.No')
    date = fields.Date()
    partner_name = fields.Char(string="Customer")
    amount = fields.Float(string='Amount(Riel)')
    vat_amount = fields.Float(string="VAT Out", compute="_compute_vat_amount", store=True)
    vat_in = fields.Float(string="VAT In")
    balance = fields.Float(string="Balance")
    no_vat = fields.Boolean(default=False)

    @api.depends('amount','no_vat')
    def _compute_vat_amount(self):
        for line in self:
            if line.no_vat == False:
                line.vat_amount = line.amount * 0.1
            else:
                line.vat_amount = 0.0

    @api.onchange('amount', 'no_vat')
    def onchange_amount(self):
        for line in self:
            if line.no_vat == False:
                line.vat_amount = line.amount * 0.1
            else:
                line.vat_amount = 0.0

