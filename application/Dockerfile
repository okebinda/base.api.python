FROM python:3.9-alpine

# create user
RUN adduser -D appuser
WORKDIR /home/appuser

# install tools
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev openssl-dev python3-dev postgresql-dev
RUN pip install pipenv uwsgi

# install dependencies
COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r /home/appuser/requirements.txt

# copy application configuration
COPY config/uwsgi.ini ./uwsgi.ini

# copy application source code
COPY src/main/python/ ./
RUN chown -R appuser:appuser ./

# start uwsgi application server on port 5000
USER appuser
EXPOSE 5000
CMD ["uwsgi", "--ini", "/home/appuser/uwsgi.ini"]
