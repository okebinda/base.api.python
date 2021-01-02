FROM python:3.9-alpine

WORKDIR /code

ENV FLASK_APP=main
ENV FLASK_RUN_HOST=0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev openssl-dev python3-dev postgresql-dev
RUN pip install pipenv

COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r /code/requirements.txt

EXPOSE 5000
COPY src/main/python/ ./
CMD ["flask", "run"]
