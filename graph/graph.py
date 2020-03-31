from flask import request
import datetime
import json




@app.route("/api/getGraph", methods=["GET"])
def get_graph():
    """
    Call this api to get graph
    ---
    tags:
     - GetGraph
     parameters:
     - name: span
       in: body
       type: integer
       required: true
       description: 周查询/月查询
       example: week
    responses:
      200:
       description: 获取图表成功,返回sales和profit
       schema:
         $ref: "#/definitions/Graph"

    definitions:
        Graph:
          properties:
            sales:
              type: array
              example: [10,10,0,20,40,10,0]
            profit:
              type: array
              example: [100,200,-10,200,-200,60,70]
    """
    data = request.get_json()
    # 获取时间跨度
    span = data.get("span")
    now_time = datetime.datetime.now()

