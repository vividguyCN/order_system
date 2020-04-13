import datetime
from flask import Blueprint
from app.database.graph import get_order_by_time
import json

graph_api = Blueprint('graph', __name__)


# 获取一周销售图表
@graph_api.route("/getWeekGraph", methods=["GET"])
def get_week_graph():
    """
    使用这个api来获取最近一周的表格
    ---
    tags:
     - GetWeeklyGraph
    responses:
      200:
       description: 获取图表成功,返回sales和profit
       schema:
         $ref: "#/definitions/WeekGraph"

    definitions:
        WeekGraph:
          properties:
            sales:
              type: array
              example: [10,10,0,20,40,10,0]
            profit:
              type: array
              example: [100,200,-10,200,-200,60,70]
    """
    today = datetime.datetime.now()
    back_data = get_order_by_time(7, today)

    return json.dumps(back_data), 200


# 获取这个月销售图表
@graph_api.route("/getMonthGraph", methods=["GET"])
def get_month_graph():
    """
    使用这个api来获取这个月以来的表格
    ---
    tags:
     - GetMonthlyGraph
    responses:
      200:
       description: 获取图表成功,返回days,sales和profit
       schema:
         $ref: "#/definitions/MonthGraph"

    definitions:
        MonthGraph:
          properties:
            day:
              type: string
              example: 28
            sales:
              type: array
              example: [10,10,0,20,40,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            profit:
              type: array
              example: [100,200,-10,200,-200,60,70,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    """
    today = datetime.datetime.now()
    first = today.replace(day=1)
    span = (today - first).days + 1

    back_data = get_order_by_time(span, today)
    back_data["day"] = span

    return json.dumps(back_data), 200
