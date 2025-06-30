# 🔧 Versioni Allineate con AWS Managed Services

Questo stack utilizza versioni compatibili con i servizi gestiti di AWS per garantire la massima compatibilità e facilità di migrazione.

## 📊 **Versioni Componenti**

### **Grafana 10.4.8**
- **AWS Managed Grafana**: versione 10.4 (supportata da maggio 2024)
- **Versione Docker**: `v10.4.8` (ultima patch stabile)
- **Feature supportate**:
  - ✅ Correlations (collegamento tra data sources)
  - ✅ Subfolders (organizzazione gerarchica dashboard)
  - ✅ Service Accounts (sostituzione API keys)
  - ✅ Nuove visualizzazioni: XY Chart, Datagrid, Trend panel
  - ✅ Simplified Alert Notification Routing
  - ✅ Return to Previous navigation

### **Prometheus 2.54.1**
- **AWS Managed Service for Prometheus**: completamente compatibile
- **Versione Docker**: `v2.54.1` (LTS stabile)
- **Feature supportate**:
  - ✅ Remote Write API
  - ✅ PromQL query language
  - ✅ Recording e Alerting rules
  - ✅ High cardinality metrics
  - ✅ UTF-8 support per Alertmanager

### **OpenTelemetry Collector v0.128.0**
- **Versione**: `v0.128.0` (stabile)
- **Protocolli**: HTTP (4318) + gRPC (4317)
- **Compatibilità**: AWS Distro for OpenTelemetry

### **Altri Componenti**
- **Tempo**: `v2.8.1` (tracing)
- **Loki**: `v3.5.1` (logs)
- **Pyroscope**: `v1.14.0` (profiling)
- **InfluxDB**: `3-core` (latest)

## 🚀 **Vantaggi dell'Allineamento AWS**

### **Migrazione Semplificata**
- ✅ Grafana 10.4 = AWS Managed Grafana
- ✅ Prometheus 2.54 = compatibile AWS Managed Prometheus
- ✅ Feature flags identiche ai servizi AWS
- ✅ Configurazioni trasferibili 1:1

### **Feature Avanzate di Grafana 10.4**
- 🔗 **Correlations**: collegamento automatico metrics ↔ logs
- 📁 **Subfolders**: organizzazione dashboard enterprise
- 🔔 **Simplified Routing**: gestione alert semplificata
- 🎯 **Service Accounts**: autenticazione moderna
- 📊 **Nuovi panel**: XY Chart, Datagrid, Trend

### **Sicurezza Enterprise**
- 🔐 RBAC (Role-Based Access Control)
- 🔒 SAML 2.0 integration ready
- 📊 CloudTrail audit logging ready
- 🌐 VPC endpoint compatibility

## 🔧 **Build e Deploy**

### **Build dell'immagine personalizzata**
```bash
# Build con versioni AWS-aligned
docker build -t otel-lgtm-aws:latest docker/

# Run dello stack completo
docker run -p 3000:3000 -p 4317:4317 -p 4318:4318 -p 9090:9090 \
  otel-lgtm-aws:latest
```

### **Rimozione Docker Compose**
Il `docker-compose-with-influxdb.yml` può essere eliminato in favore del Dockerfile unificato:
```bash
# Rimuovi il file docker-compose
rm docker-compose-with-influxdb.yml

# Usa solo il Dockerfile
./build-lgtm.sh
./run-lgtm.sh
```

## 📈 **Roadmap AWS**

### **Grafana v11 (prossima)**
- 🚨 **Breaking**: Rimozione completa Angular support
- ✨ Nuove feature di correlazione avanzata
- 🎨 UI/UX improvements

### **Prometheus Evolution**
- 📊 Enhanced UTF-8 support
- 🔄 Improved collector functionality
- 📈 Better high-cardinality handling

## 🌐 **Accessi Stack**

| Servizio          | URL                   | Versione | Compatibilità AWS        |
| ----------------- | --------------------- | -------- | ------------------------ |
| **Grafana**       | http://localhost:3000 | 10.4.8   | ✅ AWS Managed Grafana    |
| **Prometheus**    | http://localhost:9090 | 2.54.1   | ✅ AWS Managed Prometheus |
| **InfluxDB**      | http://localhost:8086 | 3-core   | ➖ Non gestito da AWS     |
| **OpenTelemetry** | 4317/4318             | 0.128.0  | ✅ AWS Distro for OTel    |
| **Tempo**         | http://localhost:3200 | 2.8.1    | ✅ Compatibile            |
| **Loki**          | http://localhost:3100 | 3.5.1    | ✅ Compatibile            |

## 📚 **Riferimenti AWS**

- [AWS Managed Grafana v10.4](https://aws.amazon.com/about-aws/whats-new/2024/05/amazon-managed-grafana-supports-version-10-4/)
- [AWS Managed Prometheus](https://aws.amazon.com/prometheus/)
- [AWS Distro for OpenTelemetry](https://aws-otel.github.io/docs/introduction)
- [Migration Guide](https://docs.aws.amazon.com/grafana/latest/userguide/version-differences.html)

---
**Ultimo aggiornamento**: Gennaio 2025  
**Compatibilità testata**: ✅ AWS Managed Services  
**Dockerfile**: `docker/Dockerfile` (versioni aggiornate) 