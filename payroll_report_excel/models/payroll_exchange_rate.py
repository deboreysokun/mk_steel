
from odoo import models, fields, api


class EmployeeAttendance(models.Model):
    _name = 'payroll.exchange.rate'

    date = fields.Date(string='Date', required=True)
    payroll_rate = fields.Float(string="Payroll's Rate")


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def create(self, vals):
        rate = self.env['payroll.exchange.rate'].search([], limit=1)
        vals['exchange_rate'] = rate.payroll_rate
        return super(HrPayslip, self).create(vals)

    def action_payslip_cancel(self):
        self.write({'state': 'cancel'})
        return super(HrPayslip, self).action_payslip_cancel()

