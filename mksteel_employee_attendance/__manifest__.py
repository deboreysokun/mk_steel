# -*- coding: utf-8 -*-

{
    'name': 'Manage Employee Attendance',
    'version': '13.0.1.0.0',
    'summary': """ """,
    'description': """""",
    'author': "A2A Digital",
    'company': 'A2A digital',
    'website': '',
    'category': 'Human Resources',
    'depends': ['hr', 'hr_contract'],
    'data': [
        'views/employee_attendance_view.xml',
        'security/ir.model.access.csv',
        'reports/employee_attendance_report_view.xml',
        'views/hr_employee_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
