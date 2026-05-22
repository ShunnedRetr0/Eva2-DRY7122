FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install --no-cache-dir --disable-pip-version-check --progress-bar off flask
EXPOSE 9999
CMD ["python", "app.py"]
