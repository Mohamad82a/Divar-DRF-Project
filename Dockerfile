FROM python:latest
EXPOSE 8000
WORKDIR /app

COPY requirements.txt /app

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]