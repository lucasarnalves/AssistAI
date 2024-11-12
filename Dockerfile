FROM python:3.12

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]