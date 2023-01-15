FROM python:3.11-slim

RUN pip3 install --no-cache --upgrade pip redis flask

WORKDIR /app
COPY --chown=1000:1000 . /app

USER 1000:1000

EXPOSE 5000
ENTRYPOINT ["python3", "-m", "flask", "run", "--host", "0.0.0.0"]
