FROM ubuntu:20.04 AS event-management
WORKDIR /app

ENV DATABASE_URL postgres://nishi:root@localhost/event

RUN apt-get update && apt-get install libmagic1 gcc python3-dev -y && apt-get install python3-venv -y && apt-get install git -y

RUN python3 -m venv /opt/venv && apt-get update && /opt/venv/bin/pip install pip --upgrade

COPY requirements.txt /app
RUN  /opt/venv/bin/pip install -r requirements.txt

FROM event-management as event
COPY . /app

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]