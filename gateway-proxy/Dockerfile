FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gateway.py .

# mocks klasörünü /app/mocks altına kopyala
COPY mocks/ /app/mocks/

EXPOSE 80

CMD ["uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "80"]