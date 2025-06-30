#!/usr/bin/env python3

import random
import time

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Configure the metric exporter to send to OpenTelemetry Collector via gRPC
metric_exporter = OTLPMetricExporter(
    endpoint="http://127.0.0.1:4317",  # OpenTelemetry Collector gRPC endpoint
    insecure=True,  # Use insecure connection for local testing
)

# Create a metric reader that exports metrics every 5 seconds
metric_reader = PeriodicExportingMetricReader(
    exporter=metric_exporter,
    export_interval_millis=5000,
)

# Set up the meter provider
metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))

# Create a meter
meter = metrics.get_meter("test_influxdb_grpc_metrics")

# Create counters and histograms
request_counter = meter.create_counter(
    name="grpc_http_requests_total",
    description="Total number of HTTP requests via gRPC",
    unit="1",
)

response_time_histogram = meter.create_histogram(
    name="grpc_http_request_duration",
    description="HTTP request duration in seconds via gRPC",
    unit="s",
)

# Create additional metrics for testing
error_counter = meter.create_counter(
    name="grpc_application_errors_total",
    description="Total application errors via gRPC",
    unit="1",
)

active_connections_gauge = meter.create_up_down_counter(
    name="grpc_active_connections",
    description="Number of active connections via gRPC",
    unit="1",
)

def simulate_traffic():
    """Simulate some application traffic with gRPC telemetry"""
    endpoints = ["/api/users", "/api/orders", "/api/products", "/health", "/metrics"]
    methods = ["GET", "POST", "PUT", "DELETE"]
    status_codes = [200, 201, 400, 404, 500]
    
    active_connections = 0
    
    for i in range(150):  # More requests for better testing
        # Simulate HTTP requests
        endpoint = random.choice(endpoints)
        method = random.choice(methods)
        status_code = random.choice(status_codes)
        
        # Simulate connection changes
        if random.random() < 0.3:  # 30% chance to change connections
            if random.random() < 0.5:
                active_connections += random.randint(1, 3)
            else:
                active_connections = max(0, active_connections - random.randint(1, 2))
        
        # Record active connections
        active_connections_gauge.add(1 if random.random() < 0.6 else -1, {
            "service": "test-grpc-service",
            "instance": "instance-1",
        })
        
        # Increment request counter
        request_counter.add(
            1,
            {
                "method": method,
                "endpoint": endpoint,
                "status_code": str(status_code),
                "service": "test-grpc-service",
                "protocol": "grpc",
            }
        )
        
        # Record response time
        response_time = random.uniform(0.005, 3.0)  # 5ms to 3s
        response_time_histogram.record(
            response_time,
            {
                "method": method,
                "endpoint": endpoint,
                "status_code": str(status_code),
                "service": "test-grpc-service",
                "protocol": "grpc",
            }
        )
        
        # Record errors for 4xx and 5xx status codes
        if status_code >= 400:
            error_counter.add(
                1,
                {
                    "error_type": "client_error" if status_code < 500 else "server_error",
                    "endpoint": endpoint,
                    "service": "test-grpc-service",
                    "protocol": "grpc",
                }
            )
        
        print(f"gRPC Request {i+1}: {method} {endpoint} -> {status_code} ({response_time:.3f}s) [Active: {active_connections}]")
        time.sleep(0.08)  # Slightly faster requests

if __name__ == "__main__":
    print("🚀 Starting OpenTelemetry gRPC metrics test...")
    print("📡 Sending metrics to InfluxDB via OpenTelemetry Collector (gRPC)...")
    print("⏱️  Metrics will be exported every 5 seconds.")
    print("🔌 Using gRPC endpoint: http://127.0.0.1:4317")
    print()
    
    try:
        simulate_traffic()
        print("\n✅ Traffic simulation completed. Waiting for final metrics export...")
        time.sleep(10)  # Wait for final export
        print("🎉 gRPC test completed successfully!")
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
    finally:
        # Force final export
        try:
            metric_reader.force_flush()
            print("📤 Final metrics exported via gRPC.")
        except Exception as e:
            print(f"⚠️  Error during final export: {e}") 