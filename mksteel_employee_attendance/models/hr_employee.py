# -*- coding:utf-8 -*-

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    khmer_name = fields.Char(string="Khmer Name")
    employee_number = fields.Char(string="Employee Id")
    family_information = fields.Text()
    start_working_date = fields.Date(string="Entry Date")

class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    khmer_name = fields.Char(string="Khmer Name", readonly=True)
    employee_number = fields.Char(string="Employee Id",readonly=True)
    family_information = fields.Text(readonly=True)
    start_working_date = fields.Date(string="Entry Date",readonly=True)


class HrContract(models.Model):
    _inherit = 'hr.contract'

    entry_salary = fields.Monetary('Entry Salary', tracking=True)
