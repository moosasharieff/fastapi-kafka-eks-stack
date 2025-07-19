#!/bin/bash

set -e

echo "🔍 Checking running Docker containers..."
docker ps --format "table {{.Names}}	{{.Status}}" | grep -E "order-service|prometheus|grafana|jaeger|postgres-exporter|kafka-exporter|otel-collector|redpanda|postgres"

echo -e "\n🌐 Testing metrics endpoints..."
for url in \
  "http://localhost:8000/metrics" \
  "http://localhost:9187/metrics" \
  "http://localhost:9308/metrics"
do
  echo -n "Checking $url ... "
  curl -sf "$url" > /dev/null && echo "✅ OK" || echo "❌ FAILED"
done

echo -e "\n📡 Checking Prometheus targets..."
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {instance, health, scrapeUrl}'

echo -e "\n🧠 Verifying Prometheus query works..."
curl -s "http://localhost:9090/api/v1/query?query=http_requests_total" | jq '.status'

echo -e "\n📊 Verifying Grafana is accessible..."
curl -sf http://localhost:3000/login > /dev/null && echo "✅ Grafana login page is up" || echo "❌ Grafana not responding"

echo -e "\n🔎 Checking Jaeger traces UI..."
curl -sf http://localhost:16686 > /dev/null && echo "✅ Jaeger UI is up" || echo "❌ Jaeger UI not responding"

echo -e "\n✅ All basic observability services checked. For Grafana dashboards and Jaeger traces, need to use the web UI."
