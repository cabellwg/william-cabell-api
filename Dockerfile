# Build stage
FROM python:3.7-alpine as build

RUN apk update && apk add --no-cache \
        bash \
        make \
        linux-headers \
        g++ \
        pcre \
        pcre-dev

COPY requirements.txt Makefile /app/
WORKDIR /app

RUN make init

# Production stage
FROM python3.7-alpine as prod

COPY --from=build /app /app
COPY . /app

ENTRYPOINT /app/p3_7env/bin/uwsgi --ini /app/uwsgi/williamcabell.ini
