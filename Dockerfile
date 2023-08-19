FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

CMD ["gunicorn", "store.wsgi:application", "--bind", "0.0.0.0:8000"]




