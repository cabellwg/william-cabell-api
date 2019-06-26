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
FROM python:3.7-alpine as prod

RUN apk update && apk add --no-cache pcre

RUN addgroup -S flask && adduser -S flask -G flask
USER flask

COPY --from=build /app /app
COPY . /app
WORKDIR /app

ENTRYPOINT ["/app/p3_7env/bin/uwsgi", "--ini", "/app/uwsgi/williamcabell.ini"]
