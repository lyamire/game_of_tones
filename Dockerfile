FROM python:3.12.3

LABEL vendor="Tatsiana M" \
      com.example.version=1.0.0-release \
      com.example.release-date=2024-04-01

EXPOSE 8000
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000
