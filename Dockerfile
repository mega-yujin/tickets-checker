FROM python:3.11.6-alpine
COPY ./app /app
COPY requirements.txt /app

WORKDIR /app

ENV PYTHONPATH=/
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]

EXPOSE 5001
