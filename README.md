# 🚀 fastapi-kafka-eks-stack

Production-ready microservice architecture using **FastAPI**, **Kafka (Redpanda)**, **PostgreSQL**, **Prometheus**, **Grafana**, and **Jaeger**, containerized with **Docker Compose**.

Built for:
- High-performance **event-driven communication**
- Scalable **observability**
- Cloud-native deployment on **AWS EKS** (with MSK, RDS, CloudWatch, Secrets Manager)



## 📦 Stack Overview

| Component          | Role                                                   |
|--------------------|--------------------------------------------------------|
| FastAPI (`order-service`) | REST API Microservice for placing and storing orders   |
| PostgreSQL         | Async persistence layer (via SQLModel + asyncpg)       |
| Kafka (Redpanda)   | High-throughput event bus for decoupled communication  |
| Prometheus         | Scrapes metrics from services and exporters            |
| Grafana            | Visualizes service-level metrics and performance trends |
| Jaeger             | Distributed tracing via OpenTelemetry                  |
| kafka-exporter     | Exposes Kafka topic/partition/consumer lag metrics     |
| postgres-exporter  | Exposes PostgreSQL metrics in Prometheus format        |
| OTEL Collector     | Aggregates and exports tracing data to Jaeger          |



## 🧭 Architecture Diagram

```
       +-------------+             +---------------------+
       | order-service (FastAPI)  | -->  /metrics (Prometheus)
       +-------------+            |
             |                    |
        writes to DB             +----->  Kafka (Redpanda)  ----+
             |                                 ^               |
             v                                 |               v
       PostgreSQL                        kafka-exporter   postgres-exporter
                                                 |               |
                                                 v               v
                                             Prometheus <--------+
                                                 |
                                                 v
                                               Grafana
```



## ⚙️ Getting Started

### 🐳 Spin up services:

```bash
docker-compose down -v
docker-compose up --build
```

### 📁 Environment config (`.env`)

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=orderdb
POSTGRES_DSN=postgresql+asyncpg://postgres:postgres@postgres:5432/orderdb
POSTGRES_EXPORTER_DSN=postgresql://postgres:postgres@postgres:5432/orderdb?sslmode=disable
KAFKA_BOOTSTRAP_SERVERS=redpanda:9092
SERVICE_NAME=order-service
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
```



## 🔍 Observability Dashboards

| Tool       | Access URL                | Default Login     |
|------------|---------------------------|--------------------|
| Prometheus | http://localhost:9090     | N/A                |
| Grafana    | http://localhost:3000     | `admin / admin`    |
| Jaeger     | http://localhost:16686    | N/A                |
| Metrics    | `/metrics` endpoints      | FastAPI, Exporters |

📄 Full guide: [Observability Metrics Architecture](./Docs/Observability/observability_metrics.md)  
✅ Verification checklist: [Observability Validation Guide](./Docs/Observability/observability_verification_doc.md)



## 📬 Example: Send an Order

```bash
curl -X POST http://localhost:8000/order \
  -H "Content-Type: application/json" \
  -d '{"item": "book", "quantity": 2}'
```



## 🧪 Load Testing

Use the built-in load testing script:

```bash
python order/load_test_random_data.py
```

> Simulates concurrent order submissions using Faker + aiohttp



## 📈 Metrics You Get

- `http_requests_total`, `http_request_duration_seconds` — API performance
- `pg_stat_activity_count`, `pg_up` — Postgres health
- `kafka_topic_partition_current_offset`, `kafka_consumergroup_lag` — Kafka metrics
- Full tracing of API + Kafka calls via Jaeger (via OTLP tracing)



## 🛠️ Developer Tools

| Tool     | Purpose                     |
|----------|-----------------------------|
| `Makefile` | `install`, `format`, `lint`, `test` routines |
| `black`  | Auto-code formatting        |
| `ruff`   | Linting                     |
| `pytest` | Testing framework           |
| `mypy`   | Type-checking               |



## 📦 Future Enhancements

- [ ] Deploy to **AWS EKS** with Helm
- [ ] Connect Prometheus → CloudWatch
- [ ] Add API Gateway + Auth0 integration
- [ ] Add Slack alerts for Kafka lag or DB failures



## 📝 License

[MIT](./LICENSE)



## 🙌 Credits

Built with ❤️ using FastAPI, SQLModel, aiokafka, and OpenTelemetry.  
Inspired by cloud-native microservice observability best practices.
