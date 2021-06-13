FROM python:3.8-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY src src
CMD ["python", "src"]
