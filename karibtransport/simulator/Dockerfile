FROM python:3.11-slim

WORKDIR /simulator

RUN pip install --no-cache-dir requests

COPY gps_simulator.py .

CMD ["python", "gps_simulator.py"]
