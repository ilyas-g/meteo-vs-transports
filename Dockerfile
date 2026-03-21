FROM apache/airflow:2.9.3-python3.11

WORKDIR /opt/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/airflow

ENV PYTHONPATH=/opt/airflow