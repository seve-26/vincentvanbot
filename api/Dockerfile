FROM python:3.8-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY api.py ./api.py
COPY ["Vincent Van Bot-67b2b35a7d0c.json", "./Vincent Van Bot-67b2b35a7d0c.json"]

ENV GOOGLE_APPLICATION_CREDENTIALS='Vincent Van Bot-67b2b35a7d0c.json'

CMD uvicorn api:app --host 0.0.0.0 --port $PORT
