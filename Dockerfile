FROM python:3.9-slim-buster

COPY .  .
COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

RUN pip install --requirement requirements.txt

RUN chmod +x ./docker-entrypoint.sh
# RUN pip install pipenv
# RUN ls -la \
#   && rm -rf .venv \
#   && pipenv install --system 

ENTRYPOINT ./docker-entrypoint.sh