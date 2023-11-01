# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Vat Summary MKSteel",
    "summary": "Record Summary Vat",
    "version": "13.0.1.0.0",
    "category": "Accounting",
    "website": "https://a2a-digital.com/",
    "author": "A2A Digital",
    "license": "AGPL-3",
    "depends": ['account'],
    "data": [
        "views/vat_summary_view.xml",
        "security/ir.model.access.csv",
        "reports/vat_summary_report.xml",
    ],
    "application": False,
    "installable": True,
}
