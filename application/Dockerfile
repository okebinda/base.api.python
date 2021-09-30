FROM python:3.9.7-alpine as base


# use a temporary image to create initial build
FROM base as builder

RUN mkdir /install
WORKDIR /install

# install tools
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev openssl-dev python3-dev postgresql-dev pcre pcre-dev
RUN pip install pipenv uwsgi

# install dependencies
COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt
RUN pip install --target=/install -r /install/requirements.txt


# create final application image
FROM base

# create user
RUN adduser -D appuser
WORKDIR /home/appuser
RUN mkdir tmp

# install system packages
RUN apk add --no-cache postgresql-client pcre

# copy dependencies from builder image
COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uwsgi
COPY --from=builder /install /usr/local/lib/python3.9/site-packages

# copy application configuration
COPY config/uwsgi.ini ./uwsgi.ini

# copy application source code
COPY src/main/python/ ./python/
COPY src/main/scripts/ ./scripts/
COPY src/main/migrations/ ./migrations/
RUN chown -R appuser:appuser ./

# start uwsgi application server on port 5000
USER appuser
EXPOSE 5000
CMD ["uwsgi", "--ini", "/home/appuser/uwsgi.ini"]
