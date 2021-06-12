FROM python:3.8-slim

WORKDIR backend
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
WORKDIR backend/
COPY . .
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]