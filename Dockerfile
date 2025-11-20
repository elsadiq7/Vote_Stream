FROM python:3.10.19-alpine3.21


WORKDIR /usr/src/app

RUN apk add --no-cache curl gcc musl-dev cargo

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .




CMD ["uvicorn","app.main:app","--host",  "--port","8000"]
