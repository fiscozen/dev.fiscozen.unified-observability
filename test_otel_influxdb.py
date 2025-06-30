#!/usr/bin/env python3

import random
import time

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Configure the metric exporter to send to OpenTelemetry Collector
metric_exporter = OTLPMetricExporter(
    endpoint="http://127.0.0.1:4318/v1/metrics",  # OpenTelemetry Collector HTTP endpoint
)

# Create a metric reader that exports metrics every 5 seconds
metric_reader = PeriodicExportingMetricReader(
    exporter=metric_exporter,
    export_interval_millis=5000,
)

# Set up the meter provider
metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))

# Create a meter
meter = metrics.get_meter("test_influxdb_metrics")

# Create counters and gauges
request_counter = meter.create_counter(
    name="http_requests_total",
    description="Total number of HTTP requests",
    unit="1",
)

response_time_histogram = meter.create_histogram(
    name="http_request_duration",
    description="HTTP request duration in seconds",
    unit="s",
)

def simulate_traffic():
    """Simulate some application traffic"""
    endpoints = ["/api/users", "/api/orders", "/api/products", "/health"]
    methods = ["GET", "POST", "PUT", "DELETE"]
    status_codes = [200, 201, 400, 404, 500]
    
    for i in range(100):
        # Simulate HTTP requests
        endpoint = random.choice(endpoints)
        method = random.choice(methods)
        status_code = random.choice(status_codes)
        
        # Increment request counter
        request_counter.add(
            1,
            {
                "method": method,
                "endpoint": endpoint,
                "status_code": str(status_code),
                "service": "test-service",
            }
        )
        
        # Record response time
        response_time = random.uniform(0.01, 2.0)
        response_time_histogram.record(
            response_time,
            {
                "method": method,
                "endpoint": endpoint,
                "status_code": str(status_code),
                "service": "test-service",
            }
        )
        
        print(f"Request {i+1}: {method} {endpoint} -> {status_code} ({response_time:.3f}s)")
        time.sleep(0.1)

if __name__ == "__main__":
    print("Starting OpenTelemetry metrics test...")
    print("Sending metrics to InfluxDB via OpenTelemetry Collector...")
    print("Metrics will be exported every 5 seconds.")
    print()
    
    try:
        simulate_traffic()
        print("\nTraffic simulation completed. Waiting for final metrics export...")
        time.sleep(10)  # Wait for final export
        print("Test completed!")
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        # Force final export
        metric_reader.force_flush()
        print("Final metrics exported.") 