FROM python:3.8-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./

ENV GOOGLE_APPLICATION_CREDENTIALS=nikki-bctp-d9ee839f22f5.json

CMD uvicorn api:app --host 0.0.0.0 --port $PORT