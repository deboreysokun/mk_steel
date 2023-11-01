# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    grand_total_weight = fields.Float(string='Total Weigth:',compute='_compute_sum_quantity')
    tot_qty = fields.Float(string='Total Pcs:', compute='_compute_sum_quantity')

    is_partially_paid = fields.Boolean(string="Partially Paid",readonly=1,copy=False)
    is_fully_paid = fields.Boolean(string="Fully Paid",readonly=1,copy=False)


    @api.depends('order_line.product_uom_qty', 'order_line.secondary_uom_qty')
    def _compute_sum_quantity(self):
        for order in self:
            tot_qty = 0
            grand_total_weight = 0
            for line in order.order_line:
                if line.product_id.type == 'product':
                    tot_qty += line.secondary_uom_qty
                    grand_total_weight += line.product_uom_qty
            order.tot_qty = tot_qty
            order.grand_total_weight = grand_total_weight

class AccountMove(models.Model):
    _inherit = "account.move"

    iss_invoice = fields.Boolean(string="Is Invoice", compute="_compute_sale_invoice" ,store=True)

    @api.depends("amount_residual")
    def _compute_sale_invoice(self):
        for i in self:
            sale_order = i.env['sale.order'].search([])
            for j in sale_order:
                if j.name == i.invoice_origin:
                    if i.invoice_payment_state == "paid":
                        j.write({
							"is_partially_paid": True,
							"is_fully_paid": False
						})
                        amount = 0
                        for record in j.invoice_ids:
                            if record.invoice_payment_state == 'paid' and i.amount_residual == 0:
                                if record.type in ('out_refund'):
                                    amount -= record.amount_total
                                else:
                                    amount += record.amount_total
                        if amount == j.amount_total:
                            j.write({
								"is_partially_paid": False,
								"is_fully_paid": True
							})
                    else:
                        j.write({
                            "is_fully_paid": False
                        })
                    i.iss_invoice = True

