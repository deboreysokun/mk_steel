from odoo import models, fields, api, _

class SalesDailyReport(models.TransientModel):
    _name = 'sale.daily.report'

    start_date = fields.Datetime(string="Start Date", required=True,
        default=lambda self: fields.Datetime.today())
    end_date = fields.Datetime(string="End Date", required=True,
        default=lambda self: fields.Datetime.today().replace(hour=16, minute=59, second=59))

    def print_daily_sale_report(self):
        data = {
            "ids": self.ids,
            "model": "sale.order",
            "form": self.read(["start_date", "end_date"])[0],
        }
        return self.env.ref('mksteel_sale_order_adj.action_sale_daily_report').report_action([], data=data)
