FROM python:3.8

WORKDIR /app

RUN pip install --no-cache-dir Flask Flask-CORS mysql-connector-python

COPY . /app/

RUN python /app/app.py
#docker build . -t backend-agenda.image
#docker run -p 3000:3000 --network=bridge -e TZ=America/Sao_Paulo --restart=always --name backend-agenda.container -d backend-agenda.image
