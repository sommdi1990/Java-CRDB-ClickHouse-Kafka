# Event Streaming

<div align="right">

[← بازگشت به Kafka](Kafka-Home) | [← صفحه اصلی](Kafka-Home)

</div>

---

## هدف

Event streaming با Kafka برای communication بین services.

## Event Types

### Domain Events

- Business events
- State changes
- User actions

### Integration Events

- Cross-service events
- System events
- Notification events

## Event Structure

### Event Schema

```json
{
  "eventId": "uuid",
  "eventType": "OrderCreated",
  "aggregateId": "order-123",
  "timestamp": "2024-01-01T00:00:00Z",
  "payload": {
    // Event data
  }
}
```

## Producer

### Spring Kafka Producer

```java
@Service
public class EventProducer {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;
    
    public void publishEvent(DomainEvent event) {
        kafkaTemplate.send("domain-events", event);
    }
}
```

## Consumer

### Spring Kafka Consumer

```java
@KafkaListener(topics = "domain-events")
public void consumeEvent(DomainEvent event) {
    // Process event
}
```

## Event Sourcing

### Event Store

- Store events as source of truth
- Replay events
- Time travel

### CQRS

- Separate read and write models
- Event-driven updates
- Eventual consistency

## Best Practices

1. **Idempotency**: Consumers باید idempotent باشند
2. **Ordering**: حفظ ترتیب events
3. **Error Handling**: retry و dead letter queue
4. **Monitoring**: monitoring events

## Redpanda (جایگزین پیشنهادی)

**نکته مهم**: برای این پروژه، **Redpanda** به عنوان جایگزین مدرن و بهینه‌تر برای Apache Kafka توصیه می‌شود. Redpanda
100% compatible با Kafka API است و تمام کدهای Spring Kafka بدون تغییر کار می‌کنند.

برای جزئیات کامل، به [راهنمای کامل Redpanda](Redpanda) و [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison)
مراجعه کنید.

## لینک‌های مفید

### Apache Kafka

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Spring Kafka Documentation](https://docs.spring.io/spring-kafka/reference/html/)
- [Event Sourcing Pattern](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)
- [Idempotency Pattern](https://restfulapi.net/idempotent-rest-apis/)
- [Dead Letter Queue Pattern](https://www.enterpriseintegrationpatterns.com/patterns/messaging/DeadLetterChannel.html)

### Redpanda (توصیه شده)

- [راهنمای کامل Redpanda در پروژه](Redpanda)
- [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison)
- [Redpanda Documentation](https://docs.redpanda.com/)
- [Redpanda with Spring Boot](https://docs.redpanda.com/docs/develop/develop-with-spring/)

---

<div align="center">

[↑ بازگشت به بالا](#event-streaming) | [← بازگشت به Kafka](Kafka-Home) | [← صفحه اصلی](Kafka-Home)

</div>

