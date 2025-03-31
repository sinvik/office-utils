FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --index-url https://pypi.org/simple

EXPOSE 5000

CMD ["python", "app.py"]