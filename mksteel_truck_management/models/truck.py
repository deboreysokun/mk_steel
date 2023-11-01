# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class Truck(models.Model):
    _name = 'truck.truck'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Truck'
    _order = 'name asc'

    name = fields.Char(store=True, required=True)
    active = fields.Boolean('Active', default=True, tracking=True)
    register_number = fields.Char(tracking=True, string='Register No.')
    buy_date = fields.Date(string="Buy Date")
    license_plate = fields.Char(tracking=True, string='Plate No.',
        help='License plate number of the Truck')
    chassis = fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)', copy=False)
    driver_ids = fields.Many2many('hr.employee',copy=False)
    model_id = fields.Many2one('truck.model', 'Model Name',
    tracking=True, help='Model of the Truck')
    insurance = fields.Char()
    company = fields.Char()
    expiry_date = fields.Date(string="Expiry Date", tracking=True,copy=False)
    inspection_date = fields.Date(string="Inspection Date", tracking=True,copy=False)

    maintenance_ids = fields.One2many(
        comodel_name="truck.maintenance.line",
        inverse_name="truck_id",
        string="Repair History",
        copy=False,
    )
    fuel_log_ids = fields.One2many(
        comodel_name="truck.fuel.line",
        inverse_name="truck_id",
        string="Fuel History",
        copy=False,
    )

class TruckModel(models.Model):
    _name = 'truck.model'

    name = fields.Char(stirng="Model Name", store=True)

class TruckMaintenanceLine(models.Model):
    _name = 'truck.maintenance.line'

    truck_id = fields.Many2one('truck.truck', string='Truck')
    date = fields.Date(string="Date", required=True)
    description = fields.Char(string='Description', required=True)
    amount = fields.Float(string='Cost')
    active = fields.Boolean('Active', default=True, tracking=True, compute="inactive_line")

    @api.depends('truck_id.active')
    def inactive_line(self):
        for vehicle in self:
            vehicle.active = vehicle.truck_id.active

class TruckFuelLine(models.Model):
    _name = 'truck.fuel.line'

    truck_id = fields.Many2one('truck.truck', string="Truck")
    date = fields.Date(string="Date", required=True)
    description = fields.Char('Description', required=True)
    fuel_qty = fields.Float(string='Fuel(L)')
    km = fields.Float(string="Km")
    travel_count = fields.Integer(string="Count")
    active = fields.Boolean('Active', default=True, tracking=True, compute="inactive_line")

    driver_id = fields.Many2one('hr.employee', string="Driver")
    ass_driver_id = fields.Many2one('hr.employee', string="Ass/Driver")

    @api.depends('truck_id.active')
    def inactive_line(self):
        for vehicle in self:
            vehicle.active = vehicle.truck_id.active

