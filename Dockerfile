FROM python:3.8-slim
COPY api/requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY api /api
COPY vincentvanbot/params.py /vincentvanbot/params.py
COPY vincentvanbot/utils.py /vincentvanbot/utils.py
COPY vincentvanbot/preprocessing.py /vincentvanbot/preprocessing.py

ENV GOOGLE_APPLICATION_CREDENTIALS='api/Vincent Van Bot-67b2b35a7d0c.json'

CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
