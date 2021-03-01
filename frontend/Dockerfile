FROM python:3.7-slim
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
CMD streamlit run app.py --server.port $PORT