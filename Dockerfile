FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app/
COPY phones_data.csv /app/phones_data.csv
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
