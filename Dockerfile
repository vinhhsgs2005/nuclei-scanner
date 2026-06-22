FROM projectdiscovery/nuclei:latest

USER root

RUN apk add --no-cache python3 py3-pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 10000

CMD gunicorn app:app --bind 0.0.0.0:10000
