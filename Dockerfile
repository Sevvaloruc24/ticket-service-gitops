FROM python:3.9-slim

WORKDIR /app

# Katman önbelleğini (layer cache) korumak için önce bağımlılıkları kopyalıyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyalıyoruz
COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]