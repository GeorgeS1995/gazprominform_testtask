FROM python:3.9.6-slim-buster
ENV PYTHONPATH=/code/
RUN apt-get update -y && \
    apt-get install curl -y && \
    apt-get autoremove -y &&\
    apt-get autoclean -y && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir /code
WORKDIR /code
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY poetry.lock /code/
COPY pyproject.toml /code/
RUN $HOME/.poetry/bin/poetry config virtualenvs.create false
RUN $HOME/.poetry/bin/poetry install
COPY . /code/
EXPOSE 8000
CMD cd ./gazprominfo && gunicorn gz.wsgi:application --bind 0.0.0.0:8000