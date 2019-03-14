FROM python:3.7-slim

RUN pip install --upgrade pip
RUN pip install redis rq

COPY boot.sh ./
RUN chmod a+x boot.sh

ENTRYPOINT ["./boot.sh"]