# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools.float_utils import float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        if self.secondary_uom_id:
            res["secondary_uom_qty"] = self.secondary_uom_qty
            res["secondary_uom_id"] = self.secondary_uom_id.id
        return res

