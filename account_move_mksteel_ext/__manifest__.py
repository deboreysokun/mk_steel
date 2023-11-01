# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Move Extension for MKsteel",
    "version": "13.0.2.0.0",
    "category": "Invoicing",
    "author": "A2A digital",
    "summary": "invoice extension",
    "website": "https://a2a-digital.com/",
    "license": "AGPL-3",
    "depends": ["account", "sale_order_secondary_unit"],
    "data": [
        "views/account_move_view.xml",
        "reports/report_invoice_tax_invoice.xml",
        "reports/report_invoice_tax_invoice_government.xml",
        "reports/report_invoice_mksteel.xml",
        ],
    "installable": True,
    "auto_install": False,
}
