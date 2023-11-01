# -*- coding: utf-8 -*-
from odoo import _, models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    total_cost_price = fields.Float(compute='_compute_total_cost_price', readonly=True, store=True)

    @api.depends('standard_price', 'qty_available')
    def _compute_total_cost_price(self):
        for record in self:
            record.total_cost_price = record.standard_price * record.qty_available

    @api.onchange('standard_price', 'qty_available')
    def _onchange_standard_price(self):
        for record in self:
            record.total_cost_price = record.standard_price * record.qty_available


class ProductProduct(models.Model):
    _inherit = 'product.product'

    total_cost_price = fields.Float(compute='_compute_total_cost_price', readonly=True, store=True)


    @api.depends('standard_price', 'qty_available')
    def _compute_total_cost_price(self):
        for record in self:
            record.total_cost_price = record.standard_price * record.qty_available

    @api.onchange("standard_price", "qty_available")
    def _onchange_standard_price(self):
        for record in self:
            record.total_cost_price = record.standard_price * record.qty_available
