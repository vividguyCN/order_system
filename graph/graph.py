import datetime
import datetime
import json

from application import app
from order.order_database import get_order_by_time


# 获取一周销售图表
@app.route("/api/getWeekGraph", methods=["GET"])
def get_week_graph():
    """
    Call this api to get weekly graph
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
@app.route("/api/getMonthGraph", methods=["GET"])
def get_month_graph():
    """
    Call this api to get monthly graph
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
