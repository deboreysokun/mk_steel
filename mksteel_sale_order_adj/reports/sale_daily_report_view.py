import time
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, models, fields


class ReportSalesSalespersonWise(models.AbstractModel):
    _name = 'report.mksteel_sale_order_adj.sale_daily_report_view'

    def _get_sale_order_data(self, start_date, end_date):
        order = self.env["sale.order"].search(
            [("date_order", ">=", start_date), ("date_order", "<=", end_date),
            ("state", "not in", ["draft", "cancel"])]
        )
        return order

    @api.model
    def _get_report_values(self, docids, data=None):
        active_model = self.env.context.get("active_model")
        if data is None:
            data = {}
        if not docids:
            docids = data["form"].get("docids")
        sale_order = self.env["sale.order"].browse(docids)
        start_date = data["form"].get("start_date", fields.Date.today())
        end_date = data["form"].get(
            "end_date",
            str(datetime.now() + relativedelta(months=+1, day=1, days=-1))[
                :10
            ],
        )
        rm_act = self.with_context(data["form"].get("used_context", {}))
        _get_sale_order_data = rm_act._get_sale_order_data(
            start_date, end_date
        )
        return {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            "data": data["form"],
            "docs": sale_order,
            "get_data": _get_sale_order_data,
        }
