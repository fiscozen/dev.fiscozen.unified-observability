#!/bin/bash

. logging.sh

# Create data directory
mkdir -p /data/influxdb

echo "Starting InfluxDB 3 Core..."

/otel-lgtm/influxdb/bin/influxdb3 serve \
    --object-store file \
    --data-dir /data/influxdb \
    --node-id node1 \
    --http-bind 0.0.0.0:8086 \
    --without-auth
