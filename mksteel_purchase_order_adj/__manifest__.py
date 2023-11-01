# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Adjustment MKSteel",
    "summary": "",
    "version": "13.0.1.0.0",
    "category": "Purchase",
    "website": "",
    "author": "A2A Digital",
    "license": "AGPL-3",
    "depends": [
        "purchase_order_secondary_unit",
        "purchase_request",
        "mksteel_sale_order_adj",
    ],
    "data": [
        "views/purchase_order_view.xml",
        "views/purchase_request_view.xml",
        "report/report_purchase_order.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
