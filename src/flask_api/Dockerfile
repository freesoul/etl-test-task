# syntax=docker/dockerfile:1

FROM python:3.7.6-buster

WORKDIR /api

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
RUN chmod +x ./wait-for-it.sh
CMD ["./wait-for-it.sh", "localhost:5672", "--timeout=6", "--", "python", "main.py"]
