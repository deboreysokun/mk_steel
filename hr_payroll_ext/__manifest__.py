# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'HR Payroll Extension',
    'version': '13.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Human Resources',
    'author': "A2A Digital",
    'summary': "Manage extra HR Payroll for Local",
    #'website': '',
    'depends': [
        'hr_payroll_community',
    ],
    'data': [
        'data/hr_payroll_data.xml',
        'views/hr_payslip_views.xml',
    ],
    'installable': True,
    'application': False,
}
