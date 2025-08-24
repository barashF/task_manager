FROM python:3.12

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y postgresql-client

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]