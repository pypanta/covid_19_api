FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /covid-19
WORKDIR /covid-19

COPY Pipfile /covid-19/
RUN pip install pipenv && pipenv install --system --skip-lock

COPY . /covid-19

ENTRYPOINT ["./run.sh"]
