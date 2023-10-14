FROM python:3.11.6-alpine
COPY ./app /app
COPY run.sh /app
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["./run.sh"]

EXPOSE 5001
