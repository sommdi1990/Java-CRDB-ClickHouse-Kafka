# معماری Kafka

<div align="right">

[← بازگشت به Kafka](Kafka-Home) | [← صفحه اصلی](Kafka-Home)

</div>

---

## هدف

معماری Kafka برای event-driven communication.

## Components

### 1. Kafka Cluster

- Brokers
- Topics
- Partitions
- Replication

### 2. Producers

- Event producers
- Schema registry
- Serialization

### 3. Consumers

- Event consumers
- Consumer groups
- Offset management

## Topics & Partitions

### Topic Structure

```
topic-name
├── partition-0
├── partition-1
└── partition-2
```

### Partitioning Strategy

- **Key-based**: Partition بر اساس key
- **Round-robin**: توزیع یکنواخت
- **Custom**: Partitioning سفارشی

## Event Schema

### Schema Registry

- **Avro**: Binary format
- **JSON Schema**: JSON format
- **Protobuf**: Google's format

### Schema Evolution

- Backward compatibility
- Forward compatibility
- Schema versioning

## Consumer Groups

### Group Coordination

- Load balancing
- Partition assignment
- Rebalancing

### Offset Management

- Automatic commits
- Manual commits
- Offset reset

## Best Practices

1. **Topic Naming**: نام‌گذاری استاندارد
2. **Partition Count**: تعداد مناسب partitions
3. **Replication Factor**: حداقل 3 replicas
4. **Retention Policy**: تنظیم retention

## Redpanda (جایگزین پیشنهادی)

**نکته مهم**: برای این پروژه، **Redpanda** به عنوان جایگزین مدرن و بهینه‌تر برای Apache Kafka توصیه می‌شود. Redpanda
100% compatible با Kafka API است و performance بهتری دارد.

برای جزئیات کامل، به [راهنمای کامل Redpanda](Redpanda) و [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison)
مراجعه کنید.

### مزایای Redpanda

- ✅ Performance بالاتر (تا 10x بیشتر throughput)
- ✅ Latency پایین‌تر (تا 6x بهتر)
- ✅ بدون ZooKeeper (استفاده از Raft consensus)
- ✅ Built-in Schema Registry
- ✅ Redpanda Console (UI رایگان)
- ✅ Resource efficiency (50% CPU کمتر، 30% Memory کمتر)
- ✅ Kubernetes native

## لینک‌های مفید

### Apache Kafka

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka Getting Started](https://kafka.apache.org/documentation/#gettingStarted)
- [Kafka Streams Documentation](https://kafka.apache.org/documentation/streams/)
- [Confluent Platform Documentation](https://docs.confluent.io/platform/current/)
- [Schema Registry Documentation](https://docs.confluent.io/platform/current/schema-registry/index.html)
- [Kafka Best Practices](https://kafka.apache.org/documentation/#bestPractices)
- [Kafka Performance Tuning](https://kafka.apache.org/documentation/#performance)

### Redpanda

- [راهنمای کامل Redpanda در پروژه](Redpanda)
- [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison)
- [Redpanda Documentation](https://docs.redpanda.com/)
- [Redpanda Getting Started](https://docs.redpanda.com/docs/get-started/)

---

<div align="center">

[↑ بازگشت به بالا](#معماری-kafka) | [← بازگشت به Kafka](Kafka-Home) | [← صفحه اصلی](Kafka-Home)

</div>

