# Event-Driven Architecture

<div align="right">

[← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

---

## معرفی

Event-Driven Architecture (EDA) یک الگوی معماری است که در آن سرویس‌ها از طریق events با یکدیگر ارتباط برقرار می‌کنند.
این معماری برای سیستم‌های reactive، scalable و loosely coupled مناسب است.

## تعریف

**Event-Driven Architecture** معماری‌ای است که:

- سرویس‌ها از طریق events با یکدیگر ارتباط برقرار می‌کنند
- Events به صورت asynchronous پردازش می‌شوند
- Producers و Consumers از یکدیگر مستقل هستند
- سیستم reactive و responsive است

## مزایای Event-Driven Architecture

### 1. Loose Coupling

- سرویس‌ها وابستگی مستقیم به یکدیگر ندارند
- تغییرات در یک سرویس تأثیر کمی بر سایر سرویس‌ها دارد
- استقلال در توسعه و deploy

### 2. Scalability

- امکان scale کردن producers و consumers به صورت مستقل
- Horizontal scaling
- Load distribution

### 3. Responsiveness

- Real-time processing
- Asynchronous operations
- Non-blocking communication

### 4. Resilience

- Fault isolation
- Retry mechanisms
- Dead letter queues
- Circuit breakers

### 5. Flexibility

- اضافه کردن consumers جدید بدون تغییر producers
- Easy integration با سیستم‌های جدید
- Event replay برای recovery

## مفاهیم اصلی

### 1. Event

**تعریف:**
یک event یک رخداد یا تغییر state است که در سیستم اتفاق می‌افتد.

**ساختار Event:**

```java
public class DomainEvent {
    private String eventId;
    private String eventType;
    private String aggregateId;
    private String aggregateType;
    private LocalDateTime timestamp;
    private Object payload;
    private String version;
}
```

**مثال:**

```java
public class OrderCreatedEvent extends DomainEvent {
    private String orderId;
    private String customerId;
    private List<OrderItem> items;
    private Money totalAmount;

    public OrderCreatedEvent(Order order) {
        this.eventId = UUID.randomUUID().toString();
        this.eventType = "OrderCreated";
        this.aggregateId = order.getId();
        this.aggregateType = "Order";
        this.timestamp = LocalDateTime.now();
        this.orderId = order.getId();
        this.customerId = order.getCustomerId();
        this.items = order.getItems();
        this.totalAmount = order.getTotalAmount();
        this.version = "1.0";
    }
}
```

### 2. Event Producer

**تعریف:**
سرویسی که events را تولید و publish می‌کند.

**مثال:**

```java

@Service
public class OrderEventProducer {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Transactional
    public void publishOrderCreated(Order order) {
        // Save to database
        orderRepository.save(order);

        // Create event
        OrderCreatedEvent event = new OrderCreatedEvent(order);

        // Publish event
        kafkaTemplate.send("order-created", order.getId(), event);
    }
}
```

### 3. Event Consumer

**تعریف:**
سرویسی که به events subscribe می‌کند و آن‌ها را پردازش می‌کند.

**مثال:**

```java

@Service
public class InventoryEventConsumer {
    @Autowired
    private InventoryService inventoryService;

    @KafkaListener(topics = "order-created", groupId = "inventory-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        try {
            // Process event
            inventoryService.reserveItems(event.getItems());
        } catch (Exception e) {
            // Error handling
            log.error("Failed to process OrderCreated event", e);
            // Send to dead letter queue
        }
    }
}
```

### 4. Event Broker

**تعریف:**
سیستم مرکزی که events را دریافت، ذخیره و توزیع می‌کند.

**در این پروژه: Apache Kafka**

```
Producer ──> Kafka Topic ──> Consumer
```

## الگوهای Event-Driven

### 1. Event Sourcing

**مفهوم:**
ذخیره events به عنوان source of truth به جای current state.

**مزایا:**

- Complete audit trail
- Time travel capability
- Replay events
- Natural event generation

**مثال:**

```java
// Event Store
@Entity
public class EventStore {
    @Id
    private String eventId;
    private String aggregateId;
    private String eventType;
    private String payload;
    private LocalDateTime timestamp;
    private Long version;
}

// Replay events to rebuild state
public Order rebuildOrder(String orderId) {
    List<EventStore> events = eventStoreRepository
            .findByAggregateIdOrderByVersion(orderId);

    Order order = new Order();
    for (EventStore event : events) {
        order.apply(event);
    }
    return order;
}
```

### 2. CQRS (Command Query Responsibility Segregation)

**مفهوم:**
جداسازی read و write models.

**معماری:**

```
Command Side (Write)          Query Side (Read)
     │                              │
     │                              │
     ▼                              ▼
Database ──Event──> Event Store ──Event──> Read Model
```

**مثال:**

```java
// Command Side - Write Model
@Service
public class OrderCommandService {
    public void createOrder(CreateOrderCommand command) {
        Order order = new Order(command);
        orderRepository.save(order);
        eventPublisher.publish(new OrderCreatedEvent(order));
    }
}

// Query Side - Read Model
@Service
public class OrderQueryService {
    @KafkaListener(topics = "order-created")
    public void updateReadModel(OrderCreatedEvent event) {
        // Update read model (denormalized)
        orderReadRepository.save(new OrderReadModel(event));
    }

    public OrderReadModel getOrder(String orderId) {
        return orderReadRepository.findById(orderId);
    }
}
```

### 3. Saga Pattern

**مفهوم:**
مدیریت distributed transactions با events.

**انواع:**

1. **Choreography**: هر سرویس events خود را publish می‌کند
2. **Orchestration**: یک orchestrator workflow را مدیریت می‌کند

**مثال Choreography:**

```java
// Order Service
@Transactional
public void createOrder(Order order) {
    orderRepository.save(order);
    eventPublisher.publish(new OrderCreatedEvent(order));
}

// Inventory Service
@KafkaListener(topics = "order-created")
public void reserveInventory(OrderCreatedEvent event) {
    inventoryService.reserve(event.getItems());
    eventPublisher.publish(new InventoryReservedEvent(event.getOrderId()));
}

// Payment Service
@KafkaListener(topics = "inventory-reserved")
public void processPayment(InventoryReservedEvent event) {
    paymentService.charge(event.getOrderId());
    eventPublisher.publish(new PaymentProcessedEvent(event.getOrderId()));
}
```

### 4. Transactional Outbox Pattern

**مفهوم:**
Reliable event publishing با استفاده از outbox table.

**معماری:**

```
Application ──> Database (Business Data + Outbox) ──> Outbox Poller ──> Kafka
```

**مثال:**

```java

@Transactional
public void createOrder(Order order) {
    // Save business data
    orderRepository.save(order);

    // Save event to outbox (same transaction)
    OutboxEvent outboxEvent = new OutboxEvent();
    outboxEvent.setAggregateId(order.getId());
    outboxEvent.setEventType("OrderCreated");
    outboxEvent.setPayload(objectMapper.writeValueAsString(order));
    outboxEvent.setStatus("PENDING");
    outboxRepository.save(outboxEvent);
}

// Outbox Poller
@Scheduled(fixedDelay = 1000)
public void pollAndPublish() {
    List<OutboxEvent> events = outboxRepository
            .findByStatus("PENDING", PageRequest.of(0, 100));

    for (OutboxEvent event : events) {
        kafkaTemplate.send(event.getEventType(), event.getPayload());
        event.setStatus("PROCESSED");
        outboxRepository.save(event);
    }
}
```

## انواع Events

### 1. Domain Events

**تعریف:**
رویدادهای دامنه تجاری که در business logic اتفاق می‌افتد.

**مثال:**

- `OrderCreated`
- `OrderCancelled`
- `PaymentProcessed`
- `DocumentApproved`

```java
public class OrderCreatedEvent extends DomainEvent {
    private String orderId;
    private String customerId;
    private List<OrderItem> items;
}
```

### 2. Integration Events

**تعریف:**
رویدادهای یکپارچه‌سازی بین سرویس‌ها.

**مثال:**

- `OrderCreatedIntegrationEvent`
- `InventoryUpdatedIntegrationEvent`

```java
public class OrderCreatedIntegrationEvent {
    private String orderId;
    private String customerId;
    private LocalDateTime createdAt;
    // Integration-specific fields
}
```

### 3. System Events

**تعریف:**
رویدادهای سیستم و infrastructure.

**مثال:**

- `ServiceStarted`
- `ServiceStopped`
- `HealthCheckFailed`

```java
public class ServiceStartedEvent {
    private String serviceName;
    private String instanceId;
    private LocalDateTime startedAt;
}
```

## Best Practices

### 1. Idempotency

**مشکل:**
Events ممکن است duplicate شوند.

**راه‌حل:**
Consumers باید idempotent باشند.

```java

@KafkaListener(topics = "order-created")
public void handleOrderCreated(OrderCreatedEvent event) {
    // Check if already processed
    if (processedEventRepository.exists(event.getEventId())) {
        return; // Already processed
    }

    // Process event
    inventoryService.reserveItems(event.getItems());

    // Mark as processed
    processedEventRepository.save(new ProcessedEvent(event.getEventId()));
}
```

### 2. Event Ordering

**مشکل:**
حفظ ترتیب events.

**راه‌حل:**

- Kafka partitioning
- Sequence numbers
- Partition key strategy

```java
// Use orderId as partition key for ordering
kafkaTemplate.send("order-events",order.getId(),event);
```

### 3. Error Handling

**استراتژی:**

- Retry mechanism
- Dead letter queue
- Circuit breaker

```java

@KafkaListener(topics = "order-created")
@RetryableTopic(
        attempts = "3",
        backoff = @Backoff(delay = 1000, multiplier = 2)
)
public void handleOrderCreated(OrderCreatedEvent event) {
    try {
        inventoryService.reserveItems(event.getItems());
    } catch (Exception e) {
        log.error("Failed to process event", e);
        throw e; // Will retry
    }
}
```

### 4. Event Versioning

**مشکل:**
تغییرات در event schema.

**راه‌حل:**

- Schema versioning
- Backward compatibility
- Schema evolution

```java

@Schema(version = "2.0")
public class OrderCreatedEventV2 extends OrderCreatedEvent {
    private String newField; // New field in v2
}

// Consumer handles multiple versions
@KafkaListener(topics = "order-created")
public void handleOrderCreated(String eventJson) {
    OrderCreatedEvent event = deserializeEvent(eventJson);
    if (event.getVersion().equals("2.0")) {
        // Handle v2
    } else {
        // Handle v1
    }
}
```

### 5. Monitoring و Observability

**متریک‌ها:**

- Event throughput
- Processing latency
- Error rates
- Dead letter queue size

```java

@Component
public class EventMetrics {
    private final MeterRegistry meterRegistry;

    public void recordEventPublished(String eventType) {
        meterRegistry.counter("events.published", "type", eventType).increment();
    }

    public void recordEventProcessed(String eventType, Duration duration) {
        meterRegistry.timer("events.processed", "type", eventType)
                .record(duration);
    }
}
```

## پیاده‌سازی در پروژه

### تکنولوژی‌های استفاده شده

- **Apache Kafka / Redpanda**: Event broker (توصیه: Redpanda برای performance بهتر و operational simplicity)
- **Spring Kafka**: Integration framework
- **Confluent Schema Registry / Redpanda Built-in**: Schema management
- **Transactional Outbox Pattern**: Reliable publishing
- **Kafka Streams / Redpanda Streams**: Stream processing (در صورت نیاز)
- برای مقایسه Kafka و Redpanda، به [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison) مراجعه کنید

### ساختار Events

```
Events/
├── Domain Events/
│   ├── OrderCreated
│   ├── OrderCancelled
│   ├── PaymentProcessed
│   └── DocumentApproved
├── Integration Events/
│   ├── OrderCreatedIntegration
│   └── InventoryUpdatedIntegration
└── System Events/
    ├── ServiceStarted
    └── HealthCheckFailed
```

### Event Flow

```
1. Business Action
   ↓
2. Save to Database + Outbox
   ↓
3. Outbox Poller publishes to Kafka
   ↓
4. Consumers process events
   ↓
5. Update read models / Trigger actions
```

## چالش‌ها و راه‌حل‌ها

### چالش 1: Eventual Consistency

**مشکل:**
Data ممکن است برای مدتی inconsistent باشد.

**راه‌حل:**

- پذیرش eventual consistency
- Compensation logic
- Saga pattern

### چالش 2: Event Ordering

**مشکل:**
حفظ ترتیب events در distributed system.

**راه‌حل:**

- Kafka partitioning
- Sequence numbers
- Partition key strategy

### چالش 3: Duplicate Events

**مشکل:**
Events ممکن است duplicate شوند.

**راه‌حل:**

- Idempotent consumers
- Event deduplication
- Idempotency keys

### چالش 4: Debugging

**مشکل:**
Debugging event-driven systems پیچیده است.

**راه‌حل:**

- Distributed tracing
- Correlation IDs
- Event logging
- Event replay

## لینک‌های مفید

- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)
- [Saga Pattern](https://microservices.io/patterns/data/saga.html)
- [Transactional Outbox Pattern](https://microservices.io/patterns/data/transactional-outbox.html)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Spring Kafka Documentation](https://docs.spring.io/spring-kafka/reference/html/)
- [Event-Driven Architecture Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/)

---

<div align="center">

[↑ بازگشت به بالا](#event-driven-architecture) | [← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

