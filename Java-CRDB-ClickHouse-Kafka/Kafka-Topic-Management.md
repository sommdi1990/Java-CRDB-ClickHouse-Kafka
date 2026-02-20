# Topic Management

<div align="right">

[← بازگشت به Kafka](Kafka-Home) | [← صفحه اصلی](Kafka-Home)

</div>

---

## هدف

مدیریت Topics در Kafka.

## Topic Creation

### Command Line

```bash
kafka-topics --create \
  --topic order-events \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 3
```

### Configuration

```yaml
kafka:
  topics:
    order-events:
      partitions: 3
      replication-factor: 3
      retention-ms: 604800000  # 7 days
```

## Topic Configuration

### Retention

- **Time-based**: retention بر اساس زمان
- **Size-based**: retention بر اساس حجم
- **Both**: ترکیب هر دو

### Compression

- **GZIP**: High compression
- **Snappy**: Fast compression
- **LZ4**: Balanced

## Topic Monitoring

### Metrics

- Message rate
- Lag
- Partition count
- Replication status

### Tools

#### برای Apache Kafka

- **Kafka Manager**: Web UI
- **Kafdrop**: Web UI
- **Confluent Control Center**: Enterprise UI

#### برای Redpanda (توصیه شده)

- **Redpanda Console**: Built-in Web UI (رایگان)
- **Redpanda Admin API**: REST API برای مدیریت

## Best Practices

1. **Naming Convention**: نام‌گذاری استاندارد
2. **Partition Count**: تعداد مناسب
3. **Replication**: حداقل 3 replicas
4. **Retention**: تنظیم مناسب retention

## لینک‌های مفید

### Apache Kafka

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka Topic Configuration](https://kafka.apache.org/documentation/#topicconfigs)
- [Kafka Manager](https://github.com/yahoo/kafka-manager)
- [Kafdrop Documentation](https://github.com/obsidiandynamics/kafdrop)
- [Confluent Control Center](https://docs.confluent.io/platform/current/control-center/index.html)
- [Kafka Best Practices](https://kafka.apache.org/documentation/#bestPractices)

### Redpanda (توصیه شده)

- [راهنمای کامل Redpanda در پروژه](Redpanda)
- [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison)
- [Redpanda Console Documentation](https://docs.redpanda.com/docs/console/)
- [Redpanda Topic Management](https://docs.redpanda.com/docs/manage/topics/)

---

<div align="center">

[↑ بازگشت به بالا](#topic-management) | [← بازگشت به Kafka](Kafka-Home) | [← صفحه اصلی](Kafka-Home)

</div>

