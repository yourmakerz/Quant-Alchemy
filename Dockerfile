FROM python:3.10-slim-bullseye

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0","--port","8000"]
