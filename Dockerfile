FROM alpine:latest
RUN apk add --update --no-cache python3 py3-pip
WORKDIR /app
COPY . .
RUN python3 -m venv .env
RUN .env/bin/pip install -r message-service/requirements.txt
EXPOSE 5000
CMD [".env/bin/python", "message-service/app.py"]