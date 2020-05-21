import datetime
from flask import Blueprint
from app.database.graph import get_order_by_time
import json

graph_api = Blueprint('graph', __name__)


# 获取一周销售图表
@graph_api.route("/getWeekGraph", methods=["GET"])
def get_week_graph():
    today = datetime.datetime.now()
    back_data = get_order_by_time(7, today)

    return json.dumps(back_data), 200


# 获取这个月销售图表
@graph_api.route("/getMonthGraph", methods=["GET"])
def get_month_graph():
    today = datetime.datetime.now()
    first = today.replace(day=1)
    span = (today - first).days + 1

    back_data = get_order_by_time(span, today)
    back_data["day"] = span

    return json.dumps(back_data), 200
