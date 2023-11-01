# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare, float_round


class AccountMove(models.Model):
    _inherit = "account.move"

    exchange_rate = fields.Float('Exchange Rate')
    amount_total_khr = fields.Float(string='Total in KHR', compute='_compute_amount_total_khr')

    @api.depends('exchange_rate')
    def _compute_amount_total_khr(self):
        self.amount_total_khr = self.amount_total * self.exchange_rate

    @api.onchange('amount_total', 'exchange_rate')
    def _onchange_amount_total(self):
        self.amount_total_khr = self.amount_total * self.exchange_rate

    grand_total_weight = fields.Float(string='Total Weigth:',compute='_compute_sum_quantity')
    tot_qty = fields.Float(string='Total Pieces:', compute='_compute_sum_quantity')

    @api.depends('invoice_line_ids.secondary_uom_qty', 'invoice_line_ids.quantity')
    def _compute_sum_quantity(self):
        for order in self:
            tot_qty = 0
            grand_total_weight = 0
            for line in order.invoice_line_ids:
                if line.product_id.type == 'product':
                    tot_qty += line.secondary_uom_qty
                    grand_total_weight += line.quantity
            order.tot_qty = tot_qty
            order.grand_total_weight = grand_total_weight

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    secondary_uom_qty = fields.Float(
        string="Pieces",
        digits=dp.get_precision("Product Unit of Measure"),
    )
    secondary_uom_id = fields.Many2one(
        "product.secondary.unit",
        string="Kg/Pcs",
        ondelete="restrict",
    )

    @api.onchange("secondary_uom_id", "secondary_uom_qty")
    def onchange_secondary_uom(self):
        if not self.secondary_uom_id:
            return
        factor = self.secondary_uom_id.factor * self.product_uom_id.factor
        qty = float_round(
            self.secondary_uom_qty * factor, precision_rounding=self.product_uom_id.rounding
        )
        if (
            float_compare(self.quantity, qty, precision_rounding=self.product_uom_id.rounding)
            != 0
        ):
            self.quantity = qty

    @api.onchange("quantity")
    def onchange_secondary_unit_product_uom_qty(self):
        if not self.secondary_uom_id:
            return
        factor = self.secondary_uom_id.factor * self.product_uom_id.factor
        qty = float_round(
            self.quantity / (factor or 1.0),
            precision_rounding=self.secondary_uom_id.uom_id.rounding,
        )
        if (
            float_compare(
                self.secondary_uom_qty,
                qty,
                precision_rounding=self.secondary_uom_id.uom_id.rounding,
            )
            != 0
        ):
            self.secondary_uom_qty = qty

    @api.onchange("uom_id")
    def onchange_product_uom_for_secondary(self):
        if not self.secondary_uom_id:
            return
        factor = self.product_uom_id.factor * self.secondary_uom_id.factor
        qty = float_round(
            self.quantity / (factor or 1.0), precision_rounding=self.product_uom_id.rounding
        )
        if (
            float_compare(
                self.secondary_uom_qty, qty, precision_rounding=self.product_uom_id.rounding
            )
            != 0
        ):
            self.secondary_uom_qty = qty

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """
        If default sales secondary unit set on product, put on secondary
        quantity 1 for being the default quantity. We override this method,
        that is the one that sets by default 1 on the other quantity with that
        purpose.
        """
        res = super(AccountMoveLine, self)._onchange_product_id()
        self.secondary_uom_id = self.product_id.sale_secondary_uom_id
        if self.secondary_uom_id:
            self.secondary_uom_qty = 1.0
            self.onchange_secondary_uom()
        return res

