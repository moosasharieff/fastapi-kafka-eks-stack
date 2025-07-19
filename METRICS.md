# 📈 Metrics Collection Architecture (FastAPI + PostgreSQL + Kafka + Prometheus + Grafana)

> ✅ This document explains how metrics are **generated**, **collected**, and **visualized** in your Docker-based observability stack.



## 📘 Summary

| Component            | Role                                                                            |
| -------------------- | ------------------------------------------------------------------------------- |
| `order-service`      | Exposes FastAPI metrics at `/metrics` using `prometheus_fastapi_instrumentator` |
| `postgres-exporter`  | Exposes PostgreSQL metrics in Prometheus format                                 |
| `kafka-exporter`     | Exposes Kafka/Redpanda metrics for topics, partitions, and consumer lag         |
| `prometheus`         | Scrapes metrics from defined targets in `prometheus.yml`                        |
| `grafana`            | Visualizes metrics by querying Prometheus                                       |
| `docker-compose.yml` | Wires all services into one Docker network                                      |
| `prometheus.yml`     | Declares scrape targets for Prometheus                                          |



## 🔄 Metrics Flow Diagram

```
[ order-service ] --> exposes /metrics (FastAPI HTTP stats)
       |
       v
[ Prometheus ] <-- scrapes order-service:8000

[ postgres-exporter ] --> exposes PostgreSQL metrics
       |
       v
[ Prometheus ] <-- scrapes postgres-exporter:9187

[ kafka-exporter ] --> exposes Redpanda Kafka topic & consumer lag metrics
       |
       v
[ Prometheus ] <-- scrapes kafka-exporter:9308

       |
       v
[ Grafana ] <-- queries Prometheus for all metrics
```

## 📊 Observability Stack Verification Guide

For a complete guide to verifying observability components in this microservice architecture and metric flows, see:  
➡️ [docs/observability_verification_doc.md](docs/observability_verification_doc.md)



## 🧠 How It All Connects

### 🧱 Docker Compose Networking

* All containers are on the **same default Docker network**.
* Services communicate using **container names** (e.g., `order-service`, `postgres-exporter`, `kafka-exporter`).



### 🗂️ Prometheus Scrape Config (`prometheus.yml`)

```yaml
scrape_configs:
  - job_name: 'order-service'
    static_configs:
      - targets: ['order-service:8000']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'kafka'
    static_configs:
      - targets: ['kafka-exporter:9308']
```

Prometheus polls each of these `/metrics` endpoints periodically (default: every 1s).



## 🚀 FastAPI Setup for Metrics

In your FastAPI app (`main.py`):

```python
# order/app/main.py (Microserver: 'order')
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

This exposes HTTP metrics at:
📍 `http://localhost:8000/metrics`



## 📦 Metrics Overview

### 📊 From `order-service` (FastAPI)

| Metric                          | Description                     |
| ------------------------------- | ------------------------------- |
| `http_requests_total`           | Count of HTTP requests          |
| `http_request_duration_seconds` | Histogram of response durations |
| `http_requests_in_progress`     | Number of in-progress requests  |

➡️ [`http://localhost:8000/metrics`](http://localhost:8000/metrics)



### 🗃️ From `postgres-exporter`

| Metric                   | Description                    |
| ------------------------ | ------------------------------ |
| `pg_up`                  | PostgreSQL availability status |
| `pg_database_size_bytes` | Size of each database          |
| `pg_stat_activity_count` | Active DB connections          |

➡️ [`http://localhost:9187/metrics`](http://localhost:9187/metrics)



### 🧵 From `kafka-exporter` (Redpanda-compatible)

| Metric                                 | Description                            |
| -------------------------------------- | -------------------------------------- |
| `kafka_topic_partition_current_offset` | Latest offset per topic partition      |
| `kafka_consumergroup_current_offset`   | Consumer group committed offset        |
| `kafka_consumergroup_lag`              | Lag between head and consumer position |
| `kafka_topic_partition_oldest_offset`  | Oldest offset in topic                 |

➡️ [`http://localhost:9308/metrics`](http://localhost:9308/metrics)



### 📥 Collected by Prometheus

| Source              | Endpoint                 | Metrics Type           |
| ------------------- | ------------------------ | ---------------------- |
| `order-service`     | `order-service:8000`     | FastAPI metrics        |
| `postgres-exporter` | `postgres-exporter:9187` | PostgreSQL DB metrics  |
| `kafka-exporter`    | `kafka-exporter:9308`    | Kafka/Redpanda metrics |

Prometheus UI: [`http://localhost:9090`](http://localhost:9090)
→ Check **"Targets" tab** to confirm everything is UP.

## 📊 Visualized in Grafana

Grafana queries Prometheus for metrics visualization.

| Purpose        | Recommended Dashboard ID |
| -------------- | ------------------------ |
| FastAPI        | Any Prometheus API Panel |
| PostgreSQL     | `9628`                   |
| Kafka/Redpanda | `7589`                   |

📍 Access Grafana: [`http://localhost:3000`](http://localhost:3000)
Default login: `admin / admin`