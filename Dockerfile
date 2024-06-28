FROM python:3.11.4-slim-buster

WORKDIR /opt/bot

COPY requirements.txt /opt/bot/requirements.txt
COPY src/ /opt/bot/

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD ["main.py"]