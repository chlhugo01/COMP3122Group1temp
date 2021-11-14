FROM python:3.8

WORKDIR /app/
COPY menu.py requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

CMD python menu.py