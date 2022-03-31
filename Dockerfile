FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y jackd qjackctl libasound2-dev pipenv
COPY Pipfile Pipfile
RUN pipenv sync
