# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class StockPicking(models.Model):
    _inherit = "stock.picking"

    grand_total_weight = fields.Float(string='Total Weigth:',compute='_compute_sum_quantity')
    tot_qty = fields.Float(string='Total Pieces:', compute='_compute_sum_quantity')
    invoice_number = fields.Char(string="Invoice Number", store=True)

    @api.depends('move_line_ids_without_package.qty_done', 'move_line_ids_without_package.secondary_uom_qty')
    def _compute_sum_quantity(self):
        for move in self:
            tot_qty = 0
            grand_total_weight = 0
            for line in move.move_line_ids_without_package:
                tot_qty += line.secondary_uom_qty
                grand_total_weight += line.qty_done
            move.tot_qty = tot_qty
            move.grand_total_weight = grand_total_weight

