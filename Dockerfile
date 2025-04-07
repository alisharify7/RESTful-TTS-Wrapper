FROM  alisharify7/gunicorn-uvicorn-nginx:alpine-1.0.0

WORKDIR /app

COPY . /app
COPY requirements.txt /app/requirements.txt
COPY app.py /app/main.py

ENV GUNICORN_WORKERS 4
ENV GUNICORN_THREADS 4
ENV GUNICORN_TIMEOUT 60
ENV GUNICORN_BIND_PORT 6565
ENV GUNICORN_BIND_ADDRESS 0.0.0.0

RUN pip3 install -r requirements.txt
