FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

COPY alembic.ini /app/alembic.ini
COPY alembic/ /app/alembic/
COPY app/ /app/app/
COPY src/ /app/src/
COPY main.py /app/main.py

EXPOSE 8000

CMD ["/bin/sh", "-lc", "python -m alembic upgrade head && uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --workers 1"]
