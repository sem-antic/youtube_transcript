FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python", "app.py"]