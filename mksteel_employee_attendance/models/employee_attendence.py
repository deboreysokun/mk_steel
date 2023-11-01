
from odoo import models, fields, api, tools


class EmployeeAttendance(models.Model):
    _name = 'employee.attendance'

    employee_id = fields.Many2one('hr.employee', string="Employee", store=True)
    date = fields.Date(string='Date', required=True)
    worked_hours = fields.Float(string="Hours", store=True)
    overtime_hours = fields.Float(string="OT Nor", store=True)
    overtime_sunday = fields.Float(string="OT Sun", store=True)
    late_coming = fields.Boolean(string="Late/Left Early", store=True)
    inital_al = fields.Boolean(string="Inital AL", store=True)
    annual_leave = fields.Float(string="AL", store=True)
