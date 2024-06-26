FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN mkdir /adnAPI

WORKDIR /adnAPI

COPY requirements.txt /adnAPI/

RUN pip install -r requirements.txt

COPY . /adnAPI/

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000