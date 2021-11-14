FROM python:3.8

WORKDIR /app/
COPY customer_order.py requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

CMD python customer_order.py