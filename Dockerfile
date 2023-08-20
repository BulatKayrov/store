FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip poetry
#RUN pip install -r requirements.txt

RUN poetry config virtualenvs.create false --local
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY . /app

CMD ["gunicorn", "store.wsgi:application", "--bind", "0.0.0.0:8000"]
