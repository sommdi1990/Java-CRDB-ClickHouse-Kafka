# راهنمای کامل Redpanda - جایگزین مدرن برای Apache Kafka

<div align="right">

[← بازگشت به صفحه اصلی](Home) | [پروپوزال](Proposal) | [لینک‌های مفید](References)

</div>

---

## فهرست مطالب

1. [مقدمه و تئوری Redpanda](#1-مقدمه-و-تئوری-redpanda)
2. [مقایسه Redpanda با Apache Kafka](#2-مقایسه-redpanda-با-apache-kafka)
3. [لزوم استفاده در پروژه](#3-لزوم-استفاده-در-پروژه)
4. [مقایسه تفصیلی برای پروژه](Kafka-Redpanda-Comparison)
4. [ویژگی‌های نسخه رایگان (Community Edition)](#4-ویژگیهای-نسخه-رایگان-community-edition)
5. [معماری و مفاهیم اصلی](#5-معماری-و-مفاهیم-اصلی)
6. [نصب و راه‌اندازی](#6-نصب-و-راهاندازی)
7. [استقرار در Kubernetes](#7-استقرار-در-kubernetes)
8. [مزایا و محاسن](#8-مزایا-و-محاسن)
9. [چالش‌ها و معایب](#9-چالشها-و-معایب)
10. [Migration از Kafka به Redpanda](#10-migration-از-kafka-به-redpanda)
11. [Best Practices](#11-best-practices)
12. [سوالات متداول (FAQ)](#12-سوالات-متداول-faq)
13. [لینک‌های مفید و منابع](#13-لینکهای-مفید-و-منابع)

---

## 1. مقدمه و تئوری Redpanda

### 1.1. Redpanda چیست؟

**Redpanda** یک پلتفرم event streaming مدرن و open-source است که به عنوان جایگزینی برای Apache Kafka طراحی شده است.
Redpanda با هدف ارائه عملکرد بالاتر، سادگی بیشتر در مدیریت و کاهش پیچیدگی‌های عملیاتی توسعه یافته است.

### 1.2. تاریخچه Redpanda

- **سال 2019**: Redpanda توسط تیم Vectorized (اکنون Redpanda Data) توسعه داده شد
- **سال 2020**: نسخه اولیه منتشر شد
- **سال 2021**: نسخه production-ready منتشر شد
- **سال 2022**: Redpanda Cloud راه‌اندازی شد
- **تا امروز**: Redpanda به عنوان یکی از جایگزین‌های محبوب Kafka شناخته می‌شود

### 1.3. چرا Redpanda؟

**مشکلات Apache Kafka:**

1. **وابستگی به ZooKeeper**: Kafka به ZooKeeper برای coordination نیاز دارد که پیچیدگی عملیاتی را افزایش می‌دهد
2. **Resource Intensive**: Kafka نیاز به منابع زیادی (CPU, Memory, Disk) دارد
3. **پیچیدگی Configuration**: تنظیمات پیچیده و نیاز به tuning زیاد
4. **JVM Overhead**: اجرا بر روی JVM باعث overhead می‌شود
5. **Operational Complexity**: مدیریت و نگهداری cluster پیچیده است

**راه‌حل Redpanda:**

- **بدون ZooKeeper**: استفاده از Raft consensus protocol
- **Performance بالا**: نوشته شده با C++ برای عملکرد بهینه
- **سادگی Configuration**: تنظیمات ساده‌تر و self-tuning
- **Native Binary**: بدون JVM overhead
- **Operational Simplicity**: مدیریت و نگهداری آسان‌تر

### 1.4. معماری کلی Redpanda

```
┌─────────────────────────────────────────────────────────┐
│                    Redpanda Cluster                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Redpanda │  │ Redpanda │  │ Redpanda │            │
│  │  Node 1  │  │  Node 2  │  │  Node 3  │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│       │              │              │                   │
│       └──────────────┼──────────────┘                   │
│                     │                                   │
│              Raft Consensus                             │
└─────────────────────────────────────────────────────────┘
         │                    │
    ┌────▼────┐          ┌────▼────┐
    │Producer │          │Consumer │
    └─────────┘          └─────────┘
```

---

## 2. مقایسه Redpanda با Apache Kafka

### 2.1. جدول مقایسه

| ویژگی                       | Apache Kafka        | Redpanda                  |
|-----------------------------|---------------------|---------------------------|
| **زبان برنامه‌نویسی**       | Java (JVM)          | C++ (Native)              |
| **وابستگی**                 | ZooKeeper یا KRaft  | بدون وابستگی (Raft)       |
| **Performance**             | خوب                 | بهتر (تا 10x)             |
| **Latency**                 | متوسط               | پایین‌تر                  |
| **Memory Usage**            | بالا                | پایین‌تر                  |
| **Disk I/O**                | بالا                | بهینه‌تر                  |
| **Configuration**           | پیچیده              | ساده‌تر                   |
| **Kafka API Compatibility** | Native              | 100% Compatible           |
| **Schema Registry**         | نیاز به Confluent   | Built-in                  |
| **Management UI**           | نیاز به ابزار خارجی | Redpanda Console (رایگان) |
| **Cloud Native**            | متوسط               | بهتر                      |
| **Community**               | بزرگ                | در حال رشد                |

### 2.2. Performance Comparison

**Benchmark Results (Typical):**

- **Throughput**: Redpanda تا 10x بیشتر از Kafka
- **Latency**: Redpanda تا 6x پایین‌تر از Kafka
- **CPU Usage**: Redpanda تا 50% کمتر از Kafka
- **Memory Usage**: Redpanda تا 30% کمتر از Kafka

### 2.3. API Compatibility

Redpanda **100% compatible** با Kafka API است، یعنی:

- تمام Kafka clients کار می‌کنند
- تمام Kafka tools کار می‌کنند
- Migration بدون تغییر کد امکان‌پذیر است

---

## 3. لزوم استفاده در پروژه

### 3.1. نیازمندی‌های پروژه

با توجه به پروپوزال پروژه، نیازمندی‌های زیر وجود دارد:

1. **Event-Driven Architecture**: نیاز به messaging platform برای ارتباط asynchronous بین میکروسرویس‌ها
2. **High Throughput**: نیاز به پردازش تعداد زیادی events
3. **Low Latency**: نیاز به latency پایین برای real-time processing
4. **Scalability**: نیاز به مقیاس‌پذیری بالا
5. **Reliability**: نیاز به reliability و durability بالا
6. **Kubernetes Deployment**: نیاز به استقرار در Kubernetes
7. **Operational Simplicity**: نیاز به مدیریت و نگهداری آسان

### 3.2. چرا Redpanda برای این پروژه مناسب است؟

#### 3.2.1. Performance بالا

- **Throughput بالا**: برای پردازش تعداد زیادی events در سیستم‌های سازمانی بزرگ
- **Latency پایین**: برای real-time processing و event-driven communication
- **Resource Efficiency**: استفاده بهینه از منابع برای کاهش هزینه‌ها

#### 3.2.2. Operational Simplicity

- **بدون ZooKeeper**: کاهش پیچیدگی عملیاتی
- **Self-tuning**: تنظیمات خودکار برای کاهش نیاز به manual tuning
- **Built-in Schema Registry**: بدون نیاز به نصب جداگانه
- **Redpanda Console**: UI رایگان برای مدیریت

#### 3.2.3. Kubernetes Native

- **Helm Charts**: استقرار آسان با Helm
- **StatefulSet Support**: پشتیبانی کامل از StatefulSet
- **Resource Optimization**: استفاده بهینه از منابع Kubernetes

#### 3.2.4. Cost Efficiency

- **نسخه رایگان**: Community Edition رایگان است
- **Resource Efficiency**: نیاز به منابع کمتر
- **کاهش هزینه‌های Infrastructure**: کاهش هزینه‌های سرور و storage

#### 3.2.5. Compatibility

- **Kafka API Compatibility**: استفاده از تمام ابزارها و کتابخانه‌های موجود
- **Migration آسان**: امکان migration تدریجی از Kafka
- **Spring Kafka**: استفاده مستقیم از Spring Kafka بدون تغییر

### 3.3. Use Cases در پروژه

#### 3.3.1. Event-Driven Communication

```java
// استفاده از Spring Kafka (بدون تغییر کد)
@Service
public class EventProducer {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    public void publishEvent(DomainEvent event) {
        kafkaTemplate.send("domain-events", event);
    }
}
```

#### 3.3.2. Transactional Outbox Pattern

- استفاده از Redpanda برای reliable event publishing
- پشتیبانی از transactions
- At-least-once delivery guarantee

#### 3.3.3. Real-time Analytics

- Stream processing با Kafka Streams (compatible)
- Real-time reporting
- Event sourcing

#### 3.3.4. Document Processing

- Async document processing
- Event-driven document generation
- Batch processing با Kafka

---

## 4. ویژگی‌های نسخه رایگان (Community Edition)

### 4.1. ویژگی‌های اصلی Community Edition

#### 4.1.1. Core Features (رایگان)

✅ **Event Streaming**

- Unlimited topics
- Unlimited partitions
- Unlimited throughput
- Unlimited retention

✅ **Kafka API Compatibility**

- 100% Kafka API compatible
- تمام Kafka clients کار می‌کنند
- تمام Kafka tools کار می‌کنند

✅ **Schema Registry**

- Built-in Schema Registry
- Avro, JSON Schema, Protobuf support
- Schema evolution

✅ **Redpanda Console**

- Web-based management UI
- Topic management
- Consumer group monitoring
- Schema management

✅ **Raft Consensus**

- Built-in consensus protocol
- No ZooKeeper dependency
- Automatic leader election

✅ **Security**

- SASL/SCRAM authentication
- TLS/SSL encryption
- ACL (Access Control Lists)

✅ **Monitoring**

- Prometheus metrics
- Grafana dashboards
- Health checks

✅ **Kubernetes Support**

- Helm charts
- StatefulSet support
- Operator (در حال توسعه)

### 4.2. محدودیت‌های Community Edition

❌ **Enterprise Features (نیاز به License)**

- **Redpanda Cloud**: Managed service
- **Advanced Monitoring**: Enterprise monitoring features
- **Support**: Enterprise support
- **Advanced Security**: LDAP/AD integration, OAuth
- **Multi-region Replication**: Cross-region replication
- **Data Governance**: Advanced data governance features

### 4.3. مقایسه Community vs Enterprise

| ویژگی                  | Community Edition | Enterprise Edition |
|------------------------|-------------------|--------------------|
| **Core Features**      | ✅ رایگان          | ✅ رایگان           |
| **Schema Registry**    | ✅ رایگان          | ✅ رایگان           |
| **Redpanda Console**   | ✅ رایگان          | ✅ رایگان           |
| **Security (Basic)**   | ✅ رایگان          | ✅ رایگان           |
| **Monitoring (Basic)** | ✅ رایگان          | ✅ رایگان           |
| **Support**            | Community         | Enterprise         |
| **Advanced Security**  | ❌                 | ✅                  |
| **Multi-region**       | ❌                 | ✅                  |
| **Data Governance**    | ❌                 | ✅                  |

**نتیجه**: برای اکثر پروژه‌ها، Community Edition کافی است.

---

## 5. معماری و مفاهیم اصلی

### 5.1. معماری Redpanda

#### 5.1.1. Core Components

```
┌─────────────────────────────────────────┐
│         Redpanda Node                   │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐          │
│  │ Storage  │  │  Raft     │          │
│  │ Engine   │  │ Consensus │          │
│  └──────────┘  └──────────┘          │
│  ┌──────────┐  ┌──────────┐          │
│  │ Kafka    │  │ Schema   │          │
│  │ API      │  │ Registry │          │
│  └──────────┘  └──────────┘          │
└─────────────────────────────────────────┘
```

#### 5.1.2. Storage Engine

- **Seastar Framework**: High-performance async framework
- **Zero-copy**: برای کاهش memory overhead
- **Compression**: Built-in compression (snappy, lz4, zstd, gzip)
- **Indexing**: Efficient indexing برای fast reads

#### 5.1.3. Raft Consensus

- **Leader Election**: Automatic leader election
- **Replication**: Automatic replication
- **Fault Tolerance**: Tolerance تا (n-1)/2 failures
- **No ZooKeeper**: بدون نیاز به ZooKeeper

### 5.2. مفاهیم اصلی

#### 5.2.1. Topics و Partitions

مشابه Kafka:

- **Topic**: Logical grouping of messages
- **Partition**: Physical division of topic
- **Replication**: Replication factor برای fault tolerance

#### 5.2.2. Producers و Consumers

- **Producer**: ارسال messages به topics
- **Consumer**: دریافت messages از topics
- **Consumer Groups**: Load balancing و parallel processing

#### 5.2.3. Schema Registry

- **Built-in**: بدون نیاز به نصب جداگانه
- **Schema Evolution**: Backward/forward compatibility
- **Formats**: Avro, JSON Schema, Protobuf

---

## 6. نصب و راه‌اندازی

### 6.1. نصب با Docker

#### 6.1.1. Docker Compose

**docker-compose-redpanda.yml:**

```yaml
version: '3.8'

services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:latest
    container_name: redpanda
    command:
      - redpanda
      - start
      - --kafka-addr
      - internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr
      - internal://redpanda:9092,external://localhost:19092
      - --pandaproxy-addr
      - internal://0.0.0.0:8082,external://0.0.0.0:18082
      - --advertise-pandaproxy-addr
      - internal://redpanda:8082,external://localhost:18082
      - --schema-registry-addr
      - internal://0.0.0.0:8081,external://0.0.0.0:18081
      - --advertise-schema-registry-addr
      - internal://redpanda:8081,external://localhost:18081
      - --rpc-addr
      - redpanda:33145
      - --advertise-rpc-addr
      - redpanda:33145
      - --smp
      - '1'
      - --memory
      - 1G
      - --mode dev-container
      - --default-log-level=info
    ports:
      - "18081:18081"
      - "18082:18082"
      - "19092:19092"
      - "19644:9644"
    volumes:
      - redpanda-data:/var/lib/redpanda/data
    networks:
      - redpanda-network

  redpanda-console:
    image: docker.redpanda.com/redpandadata/console:latest
    container_name: redpanda-console
    environment:
      CONFIG_FILEPATH: /tmp/config.yml
      CONSOLE_CONFIG_FILEPATH: /tmp/console-config.yml
      KAFKA_BROKERS: redpanda:9092
      KAFKA_SCHEMAREGISTRY_ENABLED: "true"
      KAFKA_SCHEMAREGISTRY_URLS: http://redpanda:8081
    ports:
      - "8080:8080"
    networks:
      - redpanda-network
    depends_on:
      - redpanda

volumes:
  redpanda-data:

networks:
  redpanda-network:
    driver: bridge
```

#### 6.1.2. اجرا

```bash
# اجرای Redpanda
docker-compose -f docker-compose-redpanda.yml up -d

# بررسی status
docker-compose -f docker-compose-redpanda.yml ps

# Logs
docker-compose -f docker-compose-redpanda.yml logs -f redpanda
```

### 6.2. نصب روی Rocky Linux 9

#### 6.2.1. نصب با Package Manager

```bash
# اضافه کردن repository
curl -1sLf 'https://packages.vectorized.io/nzc4ZYQK3WRGd9M/redpanda/cfg/setup/bash.rpm.sh' | sudo -E bash

# نصب Redpanda
sudo dnf install redpanda -y

# فعال‌سازی و شروع سرویس
sudo systemctl enable redpanda
sudo systemctl start redpanda

# بررسی status
sudo systemctl status redpanda
```

#### 6.2.2. Configuration

**/etc/redpanda/redpanda.yaml:**

```yaml
redpanda:
  data_directory: /var/lib/redpanda/data
  node_id: 1
  rpc_server:
    address: 0.0.0.0
    port: 33145
  kafka_api:
    - address: 0.0.0.0
      port: 9092
  admin:
    - address: 0.0.0.0
      port: 9644
  seed_servers:
    - host:
        address: localhost
        port: 33145
      node_id: 1
  developer_mode: false

pandaproxy:
  pandaproxy_api:
    - address: 0.0.0.0
      port: 8082

schema_registry:
  schema_registry_api:
    - address: 0.0.0.0
      port: 8081
```

### 6.3. نصب Redpanda Console

```bash
# با Docker
docker run -d \
  --name redpanda-console \
  -p 8080:8080 \
  -e KAFKA_BROKERS=localhost:9092 \
  -e KAFKA_SCHEMAREGISTRY_ENABLED=true \
  -e KAFKA_SCHEMAREGISTRY_URLS=http://localhost:8081 \
  docker.redpanda.com/redpandadata/console:latest
```

---

## 7. استقرار در Kubernetes

### 7.1. نصب با Helm

#### 7.1.1. اضافه کردن Helm Repository

```bash
helm repo add redpanda https://charts.redpanda.com
helm repo update
```

#### 7.1.2. نصب Redpanda

```bash
# نصب Redpanda
helm install redpanda redpanda/redpanda \
  --namespace redpanda \
  --create-namespace \
  --set statefulset.replicas=3 \
  --set storage.size=100Gi \
  --set resources.cpu.cores=2 \
  --set resources.memory.size=4Gi
```

#### 7.1.3. نصب Redpanda Console

```bash
helm install redpanda-console redpanda/console \
  --namespace redpanda \
  --set config.kafka.brokers[0]=redpanda.redpanda.svc.cluster.local:9092 \
  --set config.kafka.schemaRegistry.enabled=true \
  --set config.kafka.schemaRegistry.urls[0]=http://redpanda.redpanda.svc.cluster.local:8081
```

### 7.2. StatefulSet Configuration

**redpanda-statefulset.yaml:**

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redpanda
  namespace: production
spec:
  serviceName: redpanda
  replicas: 3
  selector:
    matchLabels:
      app: redpanda
  template:
    metadata:
      labels:
        app: redpanda
    spec:
      containers:
        - name: redpanda
          image: docker.redpanda.com/redpandadata/redpanda:latest
          ports:
            - containerPort: 9092
              name: kafka
            - containerPort: 8081
              name: schema-registry
            - containerPort: 8082
              name: pandaproxy
            - containerPort: 9644
              name: admin
          env:
            - name: REDPANDA_NODE_ID
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: REDPANDA_SEED_SERVERS
              value: "redpanda-0.redpanda:33145,redpanda-1.redpanda:33145,redpanda-2.redpanda:33145"
            - name: REDPANDA_RPC_SERVER_ADDRESS
              value: "0.0.0.0"
            - name: REDPANDA_RPC_SERVER_PORT
              value: "33145"
            - name: REDPANDA_KAFKA_ADDRESS
              value: "0.0.0.0"
            - name: REDPANDA_KAFKA_PORT
              value: "9092"
            - name: REDPANDA_ADMIN_ADDRESS
              value: "0.0.0.0"
            - name: REDPANDA_ADMIN_PORT
              value: "9644"
            - name: REDPANDA_PANDAPROXY_ADDRESS
              value: "0.0.0.0"
            - name: REDPANDA_PANDAPROXY_PORT
              value: "8082"
            - name: REDPANDA_SCHEMA_REGISTRY_ADDRESS
              value: "0.0.0.0"
            - name: REDPANDA_SCHEMA_REGISTRY_PORT
              value: "8081"
            - name: REDPANDA_SMP
              value: "2"
            - name: REDPANDA_MEMORY
              value: "2G"
          resources:
            requests:
              cpu: 2000m
              memory: 4Gi
            limits:
              cpu: 4000m
              memory: 8Gi
          volumeMounts:
            - name: redpanda-data
              mountPath: /var/lib/redpanda/data
  volumeClaimTemplates:
    - metadata:
        name: redpanda-data
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 200Gi
        storageClassName: fast-ssd
---
apiVersion: v1
kind: Service
metadata:
  name: redpanda
  namespace: production
spec:
  clusterIP: None
  ports:
    - port: 9092
      name: kafka
    - port: 8081
      name: schema-registry
    - port: 8082
      name: pandaproxy
    - port: 9644
      name: admin
  selector:
    app: redpanda
---
apiVersion: v1
kind: Service
metadata:
  name: redpanda-external
  namespace: production
spec:
  type: ClusterIP
  ports:
    - port: 9092
      targetPort: 9092
      name: kafka
  selector:
    app: redpanda
```

### 7.3. Configuration برای پروژه

**values.yaml برای Helm:**

```yaml
statefulset:
  replicas: 3

storage:
  size: 200Gi
  storageClass: fast-ssd

resources:
  cpu:
    cores: 2
  memory:
    size: 4Gi

config:
  redpanda:
    data_directory: /var/lib/redpanda/data
    rpc_server:
      address: 0.0.0.0
      port: 33145
    kafka_api:
      - address: 0.0.0.0
        port: 9092
    admin:
      - address: 0.0.0.0
        port: 9644
  pandaproxy:
    pandaproxy_api:
      - address: 0.0.0.0
        port: 8082
  schema_registry:
    schema_registry_api:
      - address: 0.0.0.0
        port: 8081
```

---

## 8. مزایا و محاسن

### 8.1. Performance

#### 8.1.1. Throughput بالا

- **تا 10x بیشتر از Kafka**: در benchmarkهای مختلف
- **Zero-copy architecture**: کاهش overhead
- **Seastar framework**: High-performance async I/O

#### 8.1.2. Latency پایین

- **تا 6x پایین‌تر از Kafka**: برای real-time applications
- **Sub-millisecond latency**: برای use cases حساس به latency
- **Efficient indexing**: برای fast reads

#### 8.1.3. Resource Efficiency

- **CPU Usage**: تا 50% کمتر از Kafka
- **Memory Usage**: تا 30% کمتر از Kafka
- **Disk I/O**: بهینه‌تر از Kafka

### 8.2. Operational Simplicity

#### 8.2.1. بدون ZooKeeper

- **Raft Consensus**: Built-in consensus protocol
- **کاهش پیچیدگی**: بدون نیاز به مدیریت ZooKeeper cluster
- **کاهش منابع**: بدون نیاز به منابع اضافی برای ZooKeeper

#### 8.2.2. Self-tuning

- **Automatic tuning**: تنظیمات خودکار برای performance
- **کاهش manual configuration**: نیاز کمتر به tuning دستی
- **Best practices built-in**: بهترین practices به صورت پیش‌فرض

#### 8.2.3. Built-in Features

- **Schema Registry**: بدون نیاز به نصب جداگانه
- **Redpanda Console**: UI رایگان برای مدیریت
- **Monitoring**: Built-in Prometheus metrics

### 8.3. Developer Experience

#### 8.3.1. Kafka API Compatibility

- **100% Compatible**: تمام Kafka clients کار می‌کنند
- **بدون تغییر کد**: استفاده مستقیم از Spring Kafka
- **Migration آسان**: امکان migration تدریجی

#### 8.3.2. Documentation

- **مستندات کامل**: مستندات خوب و به‌روز
- **Examples**: مثال‌های متعدد
- **Community**: جامعه فعال و در حال رشد

### 8.4. Cost Efficiency

#### 8.4.1. نسخه رایگان

- **Community Edition**: رایگان و open-source
- **تمام Core Features**: بدون محدودیت
- **Production Ready**: مناسب برای production

#### 8.4.2. Resource Efficiency

- **کاهش هزینه‌های Infrastructure**: نیاز به منابع کمتر
- **کاهش هزینه‌های Storage**: بهینه‌تر از Kafka
- **کاهش هزینه‌های Operational**: مدیریت آسان‌تر

### 8.5. Kubernetes Native

#### 8.5.1. Helm Charts

- **استقرار آسان**: با Helm charts
- **Configuration**: با values.yaml
- **Best Practices**: Best practices built-in

#### 8.5.2. StatefulSet Support

- **StatefulSet**: پشتیبانی کامل
- **Persistent Storage**: با PVC
- **Scaling**: آسان‌تر از Kafka

---

## 9. چالش‌ها و معایب

### 9.1. چالش‌های فنی

#### 9.1.1. Community کوچکتر

**چالش:**

- جامعه کاربری کوچکتر از Kafka
- منابع و tutorials کمتر
- پشتیبانی community محدودتر

**راه‌حل:**

- استفاده از مستندات رسمی
- مشارکت در community
- استفاده از Kafka resources (به دلیل compatibility)

#### 9.1.2. Ecosystem

**چالش:**

- Ecosystem کوچکتر از Kafka
- ابزارهای کمتر
- Integrationهای کمتر

**راه‌حل:**

- استفاده از Kafka tools (compatible)
- استفاده از Redpanda Console
- توسعه ابزارهای مورد نیاز

#### 9.1.3. Learning Curve

**چالش:**

- نیاز به یادگیری مفاهیم جدید
- تفاوت‌های جزئی با Kafka
- نیاز به adaptation

**راه‌حل:**

- استفاده از Kafka knowledge (compatible)
- مطالعه مستندات Redpanda
- آزمایش در محیط dev/stage

### 9.2. محدودیت‌های نسخه رایگان

#### 9.2.1. Enterprise Features

**محدودیت‌ها:**

- ❌ Multi-region replication
- ❌ Advanced security (LDAP/AD, OAuth)
- ❌ Data governance features
- ❌ Enterprise support

**راه‌حل:**

- برای اکثر پروژه‌ها، Community Edition کافی است
- در صورت نیاز، می‌توان Enterprise Edition را خریداری کرد

#### 9.2.2. Support

**محدودیت:**

- Community support (نه enterprise support)
- Response time بیشتر
- بدون SLA

**راه‌حل:**

- استفاده از community forums
- مطالعه مستندات
- در صورت نیاز، خرید Enterprise Edition

### 9.3. Migration Challenges

#### 9.3.1. Migration از Kafka

**چالش:**

- نیاز به migration strategy
- نیاز به testing
- نیاز به rollback plan

**راه‌حل:**

- Migration تدریجی
- Testing کامل
- Rollback plan

#### 9.3.2. Compatibility Issues

**چالش:**

- ممکن است برخی ابزارها 100% compatible نباشند
- نیاز به testing

**راه‌حل:**

- Testing کامل قبل از production
- استفاده از ابزارهای tested
- در صورت نیاز، استفاده از Kafka برای specific use cases

### 9.4. Operational Challenges

#### 9.4.1. Monitoring

**چالش:**

- نیاز به setup monitoring
- نیاز به dashboards
- نیاز به alerts

**راه‌حل:**

- استفاده از Prometheus + Grafana
- استفاده از Redpanda Console
- Setup alerts

#### 9.4.2. Backup و Recovery

**چالش:**

- نیاز به backup strategy
- نیاز به recovery plan
- نیاز به testing

**راه‌حل:**

- استفاده از Kubernetes snapshots
- استفاده از persistent volumes
- Testing backup/recovery

---

## 10. Migration از Kafka به Redpanda

### 10.1. استراتژی Migration

#### 10.1.1. Migration تدریجی

**مراحل:**

1. **Phase 1: Evaluation**
    - Testing Redpanda در محیط dev
    - Benchmark performance
    - بررسی compatibility

2. **Phase 2: Parallel Run**
    - اجرای همزمان Kafka و Redpanda
    - مقایسه performance
    - Testing compatibility

3. **Phase 3: Migration**
    - Migration تدریجی services
    - Monitoring performance
    - Rollback plan

4. **Phase 4: Complete Migration**
    - حذف Kafka
    - Optimization
    - Documentation

### 10.2. Migration Steps

#### 10.2.1. Preparation

```bash
# 1. Backup Kafka data
# 2. Setup Redpanda cluster
# 3. Test connectivity
# 4. Verify compatibility
```

#### 10.2.2. Configuration Changes

**Spring Boot Configuration:**

```yaml
# application.yaml
spring:
  kafka:
    bootstrap-servers: redpanda:9092  # تغییر از kafka:9092
    # سایر تنظیمات بدون تغییر
```

#### 10.2.3. Code Changes

**بدون تغییر کد**: به دلیل 100% compatibility، نیازی به تغییر کد نیست.

```java
// کد موجود بدون تغییر کار می‌کند
@Service
public class EventProducer {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    public void publishEvent(DomainEvent event) {
        kafkaTemplate.send("domain-events", event);
    }
}
```

### 10.3. Testing Strategy

#### 10.3.1. Compatibility Testing

- Testing تمام Kafka clients
- Testing تمام Kafka tools
- Testing تمام integrations

#### 10.3.2. Performance Testing

- Benchmark throughput
- Benchmark latency
- Benchmark resource usage

#### 10.3.3. Integration Testing

- Testing با Spring Kafka
- Testing با Kafka Streams
- Testing با Schema Registry

### 10.4. Rollback Plan

#### 10.4.1. Rollback Strategy

1. **Keep Kafka Running**: در طول migration
2. **Dual Write**: نوشتن به هر دو (در صورت نیاز)
3. **Switch Back**: در صورت مشکل، بازگشت به Kafka

#### 10.4.2. Monitoring

- Monitoring performance
- Monitoring errors
- Monitoring compatibility

---

## 11. Best Practices

### 11.1. Configuration

#### 11.1.1. Resource Allocation

```yaml
resources:
  cpu:
    cores: 2  # حداقل 2 cores
  memory:
    size: 4Gi  # حداقل 4GB
```

#### 11.1.2. Storage

```yaml
storage:
  size: 200Gi  # بر اساس نیاز
  storageClass: fast-ssd  # SSD recommended
```

#### 11.1.3. Replication

```yaml
statefulset:
  replicas: 3  # حداقل 3 برای production
```

### 11.2. Topic Management

#### 11.2.1. Topic Naming

- استفاده از naming convention استاندارد
- مثال: `domain.events`, `integration.events`

#### 11.2.2. Partitioning

- تعداد partitions مناسب (حداقل 3)
- Key-based partitioning برای ordering

#### 11.2.3. Retention

- تنظیم retention policy مناسب
- استفاده از TTL برای cleanup

### 11.3. Security

#### 11.3.1. Authentication

```yaml
# SASL/SCRAM
security:
  sasl:
    mechanism: SCRAM-SHA-256
    username: admin
    password: secure-password
```

#### 11.3.2. Encryption

```yaml
# TLS/SSL
security:
  tls:
    enabled: true
    certFile: /path/to/cert.pem
    keyFile: /path/to/key.pem
```

#### 11.3.3. ACL

- استفاده از ACL برای access control
- Principle of least privilege

### 11.4. Monitoring

#### 11.4.1. Metrics

- استفاده از Prometheus metrics
- Setup Grafana dashboards
- Monitoring key metrics

#### 11.4.2. Alerts

- Setup alerts برای critical issues
- Monitoring latency
- Monitoring throughput

#### 11.4.3. Logging

- Centralized logging
- Log aggregation
- Log analysis

### 11.5. Backup و Recovery

#### 11.5.1. Backup Strategy

- Regular backups
- Snapshot-based backups
- Testing backups

#### 11.5.2. Recovery Plan

- Documented recovery plan
- Testing recovery
- RTO/RPO targets

### 11.6. Performance Optimization

#### 11.6.1. Tuning

- استفاده از self-tuning (پیش‌فرض)
- Manual tuning در صورت نیاز
- Benchmark و testing

#### 11.6.2. Scaling

- Horizontal scaling
- Vertical scaling
- Auto-scaling در Kubernetes

---

## 12. سوالات متداول (FAQ)

### 12.1. سوالات عمومی

#### Q1: آیا Redpanda جایگزین کامل Kafka است؟

**A:** بله، Redpanda 100% compatible با Kafka API است و می‌تواند به عنوان جایگزین کامل استفاده شود.

#### Q2: آیا می‌توانم از Kafka clients با Redpanda استفاده کنم؟

**A:** بله، تمام Kafka clients (Spring Kafka, kafka-python, و غیره) با Redpanda کار می‌کنند.

#### Q3: آیا Redpanda برای production مناسب است؟

**A:** بله، Redpanda Community Edition برای production مناسب است و بسیاری از شرکت‌ها از آن استفاده می‌کنند.

#### Q4: تفاوت Community Edition و Enterprise Edition چیست؟

**A:** Community Edition شامل تمام core features است. Enterprise Edition شامل advanced features مانند multi-region
replication و enterprise support است.

### 12.2. سوالات فنی

#### Q5: آیا Redpanda به ZooKeeper نیاز دارد؟

**A:** خیر، Redpanda از Raft consensus protocol استفاده می‌کند و نیازی به ZooKeeper ندارد.

#### Q6: چگونه می‌توانم از Kafka به Redpanda migrate کنم؟

**A:** به دلیل 100% compatibility، می‌توانید به سادگی endpoint را تغییر دهید. برای جزئیات، به بخش Migration مراجعه کنید.

#### Q7: آیا Redpanda Schema Registry دارد؟

**A:** بله، Redpanda دارای built-in Schema Registry است و نیازی به نصب جداگانه ندارد.

#### Q8: چگونه می‌توانم Redpanda را در Kubernetes deploy کنم؟

**A:** می‌توانید از Helm charts استفاده کنید. برای جزئیات، به بخش Kubernetes Deployment مراجعه کنید.

### 12.3. سوالات مربوط به پروژه

#### Q9: آیا Redpanda برای پروژه من مناسب است؟

**A:** با توجه به نیازمندی‌های پروژه (event-driven architecture، performance بالا، Kubernetes deployment)، Redpanda
گزینه مناسبی است.

#### Q10: آیا می‌توانم از Spring Kafka با Redpanda استفاده کنم؟

**A:** بله، Spring Kafka 100% compatible با Redpanda است و نیازی به تغییر کد نیست.

#### Q11: آیا Redpanda برای Transactional Outbox Pattern مناسب است؟

**A:** بله، Redpanda از transactions پشتیبانی می‌کند و برای Transactional Outbox Pattern مناسب است.

#### Q12: هزینه Redpanda چقدر است؟

**A:** Community Edition کاملاً رایگان است. Enterprise Edition نیاز به license دارد.

---

## 13. لینک‌های مفید و منابع

### 13.1. مستندات رسمی

- [Redpanda Documentation](https://docs.redpanda.com/)
- [Redpanda Getting Started](https://docs.redpanda.com/docs/get-started/)
- [Redpanda Kubernetes Guide](https://docs.redpanda.com/docs/deploy/deployment-option/kubernetes/)
- [Redpanda Console](https://docs.redpanda.com/docs/console/)

### 13.2. Tutorials و Guides

- [Redpanda Tutorial](https://docs.redpanda.com/docs/get-started/quick-start/)
- [Redpanda with Spring Boot](https://docs.redpanda.com/docs/develop/develop-with-spring/)
- [Redpanda Performance Tuning](https://docs.redpanda.com/docs/deploy/deployment-option/self-hosted/manual/performance-tuning/)

### 13.3. Community

- [Redpanda GitHub](https://github.com/redpanda-data/redpanda)
- [Redpanda Slack](https://redpanda.com/slack)
- [Redpanda Discord](https://discord.gg/redpanda)
- [Redpanda Forum](https://forum.redpanda.com/)

### 13.4. Tools

- [Redpanda Console](https://github.com/redpanda-data/console)
- [Redpanda Helm Charts](https://github.com/redpanda-data/helm-charts)
- [Redpanda Operator](https://github.com/redpanda-data/redpanda-operator)

### 13.5. Benchmarks و Comparisons

- [Redpanda vs Kafka Benchmark](https://redpanda.com/blog/kafka-vs-redpanda-performance-benchmark)
- [Redpanda Performance](https://redpanda.com/blog/redpanda-performance)

### 13.6. Videos و Webinars

- [Redpanda YouTube Channel](https://www.youtube.com/c/RedpandaData)
- [Redpanda Webinars](https://redpanda.com/webinars)

---

## نتیجه‌گیری

Redpanda یک جایگزین مدرن و قدرتمند برای Apache Kafka است که با ارائه performance بالاتر، سادگی بیشتر در مدیریت و کاهش
پیچیدگی‌های عملیاتی، گزینه مناسبی برای پروژه‌های event-driven است.

**برای پروژه شما:**

- ✅ Performance بالا برای event-driven architecture
- ✅ Operational simplicity برای کاهش هزینه‌های عملیاتی
- ✅ Kubernetes native برای استقرار آسان
- ✅ 100% Kafka API compatibility برای migration آسان
- ✅ Community Edition رایگان برای شروع

**توصیه:**
با توجه به نیازمندی‌های پروژه، Redpanda گزینه مناسبی است. پیشنهاد می‌شود:

1. Testing در محیط dev/stage
2. Benchmark performance
3. Migration تدریجی
4. Monitoring و optimization

**نکته**: برای مقایسه تفصیلی Redpanda و Kafka (نسخه رایگان) از نظر مزایا، معایب، و مناسب‌بودن برای این پروژه با معماری
DDD در Java، به [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison) مراجعه کنید.

---

<div align="center">

[↑ بازگشت به بالا](#راهنمای-کامل-redpanda---جایگزین-مدرن-برای-apache-kafka) | [← بازگشت به صفحه اصلی](Home) | [پروپوزال](Proposal) | [لینک‌های مفید](References)

</div>