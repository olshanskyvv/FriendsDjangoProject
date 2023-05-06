FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

CMD python3 manage.py runserver 0.0.0.0:8000