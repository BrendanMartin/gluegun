FROM python:3.7-slim

RUN adduser --disabled-password objdetect

WORKDIR /home/objdetect

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y \
    python-opencv \
    libsm6

# To prevent docker-compose from overwriting venv with volumes, putting code one more level down
RUN mkdir /objdetect
WORKDIR /home/objdetect/objdetect

COPY app app
COPY extractor extractor
COPY config.py db.py log.py reddit_api.py run.py boot.sh ./
RUN chmod a+x boot.sh

#ENV FLASK_APP run.py
#ENV FLASK_CONFIG prod

RUN chown -R objdetect:objdetect ./
USER objdetect


EXPOSE 5000
ENTRYPOINT ["./boot.sh"]