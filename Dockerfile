FROM python:3.8-slim-buster

COPY .  .

RUN pip install --requirement requirements.txt

# COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
# RUN chmod +x ./docker-entrypoint.sh
# ENTRYPOINT ./docker-entrypoint.sh

# RUN pip install pipenv
# RUN pipenv install

RUN export FLASK_APP=app.py

EXPOSE 5555
EXPOSE 5555/tcp

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--cert=adhoc"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5555"]
# CMD [ "python3", "-m" , "flask", "run","--cert=adhoc"]
