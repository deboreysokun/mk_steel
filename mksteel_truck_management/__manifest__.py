# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Truck Management For MKSteel",
    "summary": "Keep tracking on truck repair maintance and fuel log record",
    "version": "13.0.1.0.0",
    "category": "fleet",
    "website": "https://a2a-digital.com/",
    "author": "A2A Digital",
    "license": "AGPL-3",
    "depends": ['base', 'mail', 'hr'],
    "data": [
        "views/truck_view.xml",
        "security/ir.model.access.csv",
    ],
    "application": False,
    "installable": True,
}
