# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    grand_total_weight = fields.Float(string='Total Weigth:',compute='_compute_sum_quantity')
    tot_qty = fields.Float(string='Total Pcs:', compute='_compute_sum_quantity')

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


_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To be approved"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("paid", "Paid"),
    ("done", "Done"),
]

class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    employee_id = fields.Many2one(comodel_name="hr.employee",string='Requester', required=True)

    state = fields.Selection(
        selection=_STATES,
        string="Status",
        index=True,
        track_visibility="onchange",
        required=True,
        copy=False,
        default="draft",
    )

    def button_paid(self):
        return self.write({"state": "paid"})


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    employee_id = fields.Many2one(comodel_name="hr.employee",string='Requester', related="request_id.employee_id", store=True)

