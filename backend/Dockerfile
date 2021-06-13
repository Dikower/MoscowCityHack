FROM python:3.8-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY src src
#CMD ["uvicorn", "src.__main__:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "src"]
