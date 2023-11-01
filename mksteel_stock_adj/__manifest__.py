# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Adjustment MKSteel",
    "summary": "",
    "version": "13.0.1.0.0",
    "category": "stock",
    "website": "",
    "author": "",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["stock", "stock_secondary_unit"],
    "data": [
        "views/stock_move_view.xml",
        "report/report_delivery_slip.xml",
        "report/report_delivery_slip_eoun.xml",
        "report/report_picking.xml",
    ],
}
