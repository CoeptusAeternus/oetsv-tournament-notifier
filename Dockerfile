FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app

ADD . .

RUN pip install -r requirements.txt

CMD ["cron", "-f"]