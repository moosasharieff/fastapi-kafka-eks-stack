# ✅ Observability Stack Verification Guide

This guide and shell script will help you verify if the observability stack (Prometheus, Grafana, Jaeger, Kafka/Postgres exporters, etc.) is working properly.

---

## 🔧 Prerequisites

- Docker containers must be running via `docker-compose up`
- `curl` and `jq` must be installed

---

## 🚀 Run the Health Check Script

Save and run:

```bash
chmod +x verify_observability.sh
./verify_observability.sh
```

---

## ✅ What It Verifies

| Check                   | What It Confirms                          |
|------------------------|-------------------------------------------|
| Docker containers       | All observability services are running   |
| `/metrics` endpoints    | FastAPI, Postgres exporter, Kafka exporter are live |
| Prometheus targets      | Prometheus is scraping metrics correctly |
| Prometheus query        | Sample query (`http_requests_total`) works |
| Grafana availability    | UI is reachable at port `3000`           |
| Jaeger UI               | Trace UI reachable at port `16686`       |

---

## 📍 Visual Interfaces

| Service    | URL                         |
|------------|-----------------------------|
| Prometheus | http://localhost:9090       |
| Grafana    | http://localhost:3000       |
| Jaeger     | http://localhost:16686      |
| FastAPI Metrics | http://localhost:8000/metrics |
| Kafka Exporter | http://localhost:9308/metrics |
| Postgres Exporter | http://localhost:9187/metrics |

---

## 🧪 Generate Activity

To see live data:

```bash
curl -X POST http://localhost:8000/order \
  -H "Content-Type: application/json" \
  -d '{"item": "test", "quantity": 1}'
```

Then check Grafana panels and Jaeger traces.

