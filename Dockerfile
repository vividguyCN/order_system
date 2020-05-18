FROM python:3.7

COPY ./order_system ./order_system

RUN pip3 install --default-timeout=100 -r order_system/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


ENTRYPOINT ["python","order_system/main.py"]

EXPOSE 3000

