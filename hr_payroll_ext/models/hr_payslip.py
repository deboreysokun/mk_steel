
from odoo import api, fields, models,_


class HrPayslip(models.Model):

    _inherit = 'hr.payslip'

    incentive = fields.Float(string="Incentive(%)",readonly=True,states={'draft': [('readonly', False)]})
    severance = fields.Float(string="Severance",readonly=True,states={'draft': [('readonly', False)]})
    seniority_bonus = fields.Float(string="Seniority Bonus", readonly=True,states={'draft': [('readonly', False)]})
    seniority_payment = fields.Float(string="Seniority Payment", readonly=True,states={'draft': [('readonly', False)]})
    deduction = fields.Float(string="Deduction($)", readonly=True,states={'draft': [('readonly', False)]})
    attendance_bonus = fields.Float(string="Attendance Bonus", readonly=True, states={'draft': [('readonly', False)]})
    additional_allowance = fields.Float(string="Additional Allowance", readonly=True, states={'draft': [('readonly', False)]})
    remaining_leave = fields.Float(string="Remaining AL(days)", readonly=True, states={'draft': [('readonly', False)]})
    overtime_150 = fields.Float(string='Overtime WeekDay (150%)', readonly=True, states={'draft': [('readonly', False)]})
    overtime_200 = fields.Float(string='Overtime WeekDay (200%)', readonly=True, states={'draft': [('readonly', False)]})
    exchange_rate = fields.Float(string='1$ to KHR = ', readonly=True, states={'draft': [('readonly', False)]})


