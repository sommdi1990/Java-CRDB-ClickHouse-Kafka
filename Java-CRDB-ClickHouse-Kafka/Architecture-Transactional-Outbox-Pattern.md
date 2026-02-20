# Transactional Outbox Pattern

<div align="right">

[← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

---

## مشکل Dual-Write

### تعریف مشکل

مشکل **Dual-Write** زمانی رخ می‌دهد که یک application نیاز به نوشتن در دو سیستم مختلف به صورت همزمان دارد (مثلاً
database و message queue) و این دو عملیات باید به صورت atomic انجام شوند.

### سناریوی مشکل

```
┌─────────────┐
│ Application │
└──────┬──────┘
       │
       ├─── Write to Database ────┐
       │                           │
       └─── Publish to Kafka ──────┘
```

### مثال عملی

```java
@Transactional
public void createOrder(Order order) {
    // Step 1: Save to database
    orderRepository.save(order);  // ✅ Success
    
    // Step 2: Publish event to Kafka
    kafkaTemplate.send("order-created", order);  // ❌ Fails!
    
    // Problem: Database committed but event not published
    // Other services won't know about the new order
}
```

### مشکلات ناشی از Dual-Write

1. **Data Inconsistency**
    - داده در database ذخیره شده اما event ارسال نشده
    - سایر سرویس‌ها از تغییرات مطلع نمی‌شوند

2. **Lost Events**
    - Eventها ممکن است از دست بروند
    - عدم اطلاع سایر سرویس‌ها از تغییرات

3. **Ordering Issues**
    - عدم تضمین ترتیب events
    - Race conditions

4. **Transaction Rollback Complexity**
    - اگر Kafka publish موفق شود اما database commit نشود
    - نیاز به compensation logic

## راه‌حل: Transactional Outbox Pattern

### مفهوم Pattern

Transactional Outbox Pattern یک الگوی طراحی است که مشکل Dual-Write را با استفاده از یک جدول "outbox" در همان database حل
می‌کند.

### معماری

```
┌─────────────┐
│ Application │
└──────┬──────┘
       │
       ├─── Write to Database (in same transaction)
       │    ├── Business Data
       │    └── Outbox Table ───┐
       │                         │
       └─────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Outbox Poller         │
                    │  (Separate Process)     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                            ┌─────────┐
                            │  Kafka  │
                            └─────────┘
```

### مراحل پیاده‌سازی

#### Step 1: ایجاد Outbox Table

```sql
CREATE TABLE outbox (
    id UUID PRIMARY KEY,
    aggregate_id VARCHAR(255) NOT NULL,
    aggregate_type VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL,
    processed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'PENDING',
    retry_count INTEGER DEFAULT 0,
    INDEX idx_status_created (status, created_at)
);
```

#### Step 2: نوشتن در Outbox در همان Transaction

```java
@Transactional
public void createOrder(Order order) {
    // Step 1: Save business data
    orderRepository.save(order);
    
    // Step 2: Save event to outbox (in same transaction)
    OutboxEvent event = new OutboxEvent();
    event.setAggregateId(order.getId());
    event.setAggregateType("Order");
    event.setEventType("OrderCreated");
    event.setPayload(objectMapper.writeValueAsString(order));
    event.setStatus("PENDING");
    
    outboxRepository.save(event);
    
    // Both operations in same transaction
    // If one fails, both rollback
}
```

#### Step 3: Outbox Poller (Separate Process)

```java
@Component
@Scheduled(fixedDelay = 1000) // Poll every second
public class OutboxPoller {
    
    @Transactional
    public void pollAndPublish() {
        List<OutboxEvent> events = outboxRepository
            .findByStatusOrderByCreatedAt("PENDING", PageRequest.of(0, 100));
        
        for (OutboxEvent event : events) {
            try {
                // Publish to Kafka
                kafkaTemplate.send(event.getEventType(), event.getPayload());
                
                // Mark as processed
                event.setStatus("PROCESSED");
                event.setProcessedAt(LocalDateTime.now());
                outboxRepository.save(event);
                
            } catch (Exception e) {
                // Handle error, maybe retry later
                event.setRetryCount(event.getRetryCount() + 1);
                if (event.getRetryCount() > MAX_RETRIES) {
                    event.setStatus("FAILED");
                }
                outboxRepository.save(event);
                log.error("Failed to publish event", e);
            }
        }
    }
}
```

### مزایای Transactional Outbox Pattern

1. **Atomicity**: نوشتن در database و outbox در یک transaction
2. **Reliability**: تضمین ارسال events (at-least-once delivery)
3. **Consistency**: عدم inconsistency بین database و message queue
4. **Ordering**: امکان حفظ ترتیب events
5. **Idempotency**: امکان retry بدون duplicate events

### پیاده‌سازی در Spring Boot

#### Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>
```

#### Entity

```java
@Entity
@Table(name = "outbox")
public class OutboxEvent {
    @Id
    private UUID id;
    
    @Column(nullable = false)
    private String aggregateId;
    
    @Column(nullable = false)
    private String aggregateType;
    
    @Column(nullable = false)
    private String eventType;
    
    @Column(nullable = false, columnDefinition = "JSONB")
    private String payload;
    
    @Column(nullable = false)
    private LocalDateTime createdAt;
    
    private LocalDateTime processedAt;
    
    @Column(nullable = false)
    private String status;
    
    private Integer retryCount = 0;
}
```

## راه‌حل‌های جایگزین

### 1. Change Data Capture (CDC)

**مفهوم:**
استفاده از CDC tools برای capture تغییرات database و publish به message queue.

**Tools:**

- **Debezium**: Open-source CDC platform
- **AWS DMS**: Amazon Database Migration Service
- **Maxwell**: MySQL binlog reader

**مزایا:**

- No application code changes
- Automatic event generation
- Low latency

**معایب:**

- نیاز به setup و configuration
- ممکن است events غیرضروری تولید شود

### 2. Event Sourcing

**مفهوم:**
ذخیره events به عنوان source of truth به جای state.

**مزایا:**

- Complete audit trail
- Time travel capability
- Natural event generation

**معایب:**

- پیچیدگی بیشتر
- نیاز به redesign application

### 3. Saga Pattern

**مفهوم:**
استفاده از distributed transactions با compensation.

**مزایا:**

- مناسب برای workflows پیچیده
- Compensation logic

**معایب:**

- پیچیدگی بالا
- نیاز به مدیریت state

## Best Practices

1. **Idempotency**: Consumers باید idempotent باشند
2. **Retry Strategy**: Exponential backoff برای retries
3. **Dead Letter Queue**: برای events که نمی‌توانند process شوند
4. **Monitoring**: Monitoring برای outbox table size
5. **Cleanup**: حذف events پردازش شده بعد از مدت زمان مشخص

## Monitoring

- Size of outbox table
- Processing lag
- Failed events
- Retry count
- Processing time

## لینک‌های مفید

- [Transactional Outbox Pattern](https://microservices.io/patterns/data/transactional-outbox.html)
- [Outbox Pattern Explained](https://event-driven.io/en/outbox_inbox_patterns_and_delivery_guarantees/)
- [Debezium Documentation](https://debezium.io/documentation/)
- [Event Sourcing Pattern](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Saga Pattern](https://microservices.io/patterns/data/saga.html)
- [Distributed Transactions](https://martinfowler.com/articles/patterns-of-distributed-systems/)
- [Spring Kafka Documentation](https://docs.spring.io/spring-kafka/reference/html/)

---

<div align="center">

[↑ بازگشت به بالا](#transactional-outbox-pattern) | [← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

