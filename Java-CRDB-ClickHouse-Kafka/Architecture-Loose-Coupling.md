# Loose Coupling (اتصال سست)

<div align="right">

[← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

---

## معرفی

Loose Coupling یکی از اصول اساسی معماری میکروسرویس است که هدف آن کاهش وابستگی بین سرویس‌ها و افزایش استقلال هر سرویس
است.

## تعریف

**Loose Coupling** به معنای طراحی سیستم‌هایی است که:

- سرویس‌ها وابستگی کمی به یکدیگر دارند
- تغییرات در یک سرویس تأثیر کمی بر سایر سرویس‌ها دارد
- هر سرویس می‌تواند به صورت مستقل توسعه، deploy و نگهداری شود

## مزایای Loose Coupling

### 1. استقلال در توسعه

- تیم‌ها می‌توانند به صورت مستقل کار کنند
- کاهش conflicts در development
- سرعت بیشتر در توسعه

### 2. استقلال در Deploy

- Deploy یک سرویس بدون تأثیر بر سایر سرویس‌ها
- کاهش risk در production deployments
- امکان rollback مستقل

### 3. مقیاس‌پذیری

- Scale کردن سرویس‌ها به صورت مستقل
- Resource optimization
- Cost efficiency

### 4. Fault Isolation

- خطا در یک سرویس به سایر سرویس‌ها سرایت نمی‌کند
- Resilience بهتر
- Availability بالاتر

### 5. Technology Diversity

- امکان استفاده از تکنولوژی‌های مختلف برای هر سرویس
- انتخاب بهترین tool برای هر use case
- عدم محدودیت به یک technology stack

## استراتژی‌های پیاده‌سازی

### 1. Messaging و Events به جای Direct API Calls

**مشکل Direct API Calls:**

```
Service A ──HTTP──> Service B
```

- وابستگی مستقیم به location و availability
- Tight coupling
- مشکل در fault tolerance

**راه‌حل: Event-Driven Communication:**

```
Service A ──Event──> Kafka ──Event──> Service B
```

- عدم وابستگی مستقیم
- Loose coupling
- Better fault tolerance

**مثال:**

```java
// ❌ Tight Coupling - Direct API Call
@Service
public class OrderService {
    @Autowired
    private RestTemplate restTemplate;
    
    public void createOrder(Order order) {
        // Direct dependency on InventoryService
        restTemplate.post("http://inventory-service/api/inventory/check", order);
    }
}

// ✅ Loose Coupling - Event-Driven
@Service
public class OrderService {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;
    
    public void createOrder(Order order) {
        orderRepository.save(order);
        // Publish event - no direct dependency
        kafkaTemplate.send("order-created", new OrderCreatedEvent(order));
    }
}
```

### 2. API Gateway Pattern

**هدف:**
Decoupling frontend از backend services

**مزایا:**

- Single entry point
- Aggregation و transformation
- Routing و load balancing
- Authentication و authorization

**معماری:**

```
Frontend ──> API Gateway ──> Services
```

**مثال با Spring Cloud Gateway:**

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
        - id: inventory-service
          uri: lb://inventory-service
          predicates:
            - Path=/api/inventory/**
```

### 3. Database per Service

**اصل:**
هر سرویس database خود را دارد و به database سایر سرویس‌ها دسترسی ندارد.

**مزایا:**

- استقلال در schema evolution
- Technology diversity
- Fault isolation
- Scalability

**Data Synchronization:**

- از طریق events
- Eventual consistency
- CQRS pattern

**مثال:**

```java
// Order Service - Own Database
@Entity
@Table(name = "orders", schema = "order_service")
public class Order {
    // Order-specific data
}

// Inventory Service - Own Database
@Entity
@Table(name = "inventory", schema = "inventory_service")
public class Inventory {
    // Inventory-specific data
}

// Synchronization via Events
@KafkaListener(topics = "order-created")
public void handleOrderCreated(OrderCreatedEvent event) {
    // Update inventory based on event
    inventoryService.reserveItems(event.getItems());
}
```

### 4. Contract-Based Communication

**استفاده از Schemas:**

- Event schemas (Avro, JSON Schema)
- API contracts (OpenAPI/Swagger)
- Versioning برای backward compatibility

**Schema Registry:**

```java
// Event Schema Definition
@Schema(version = "1.0")
public class OrderCreatedEvent {
    private String orderId;
    private String customerId;
    private List<OrderItem> items;
    private LocalDateTime createdAt;
}

// Producer with Schema
@Service
public class OrderEventProducer {
    @Autowired
    private KafkaTemplate<String, OrderCreatedEvent> kafkaTemplate;
    
    public void publishOrderCreated(Order order) {
        OrderCreatedEvent event = new OrderCreatedEvent(
            order.getId(),
            order.getCustomerId(),
            order.getItems(),
            LocalDateTime.now()
        );
        kafkaTemplate.send("order-created", event);
    }
}
```

### 5. Service Discovery

**هدف:**
کاهش hard-coded dependencies

**راه‌حل‌ها:**

- **Kubernetes**: Built-in DNS-based service discovery (برای production و stage)
- **Consul**: Service registry (اختیاری)
- **Eureka**: Spring Cloud service discovery (برای Docker Compose)

**مثال با Consul:**

```java
@SpringBootApplication
@EnableDiscoveryClient
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}

// Service Discovery
@Service
public class InventoryServiceClient {
    @Autowired
    private DiscoveryClient discoveryClient;
    
    public void checkInventory(Order order) {
        List<ServiceInstance> instances = discoveryClient.getInstances("inventory-service");
        // Use discovered service
    }
}
```

## الگوهای طراحی برای Loose Coupling

### 1. Publish-Subscribe Pattern

```
Publisher ──> Event Broker ──> Subscribers
```

- Publisher نیازی به دانستن subscribers ندارد
- Multiple subscribers
- Loose coupling

### 2. Message Queue Pattern

```
Producer ──> Queue ──> Consumer
```

- Asynchronous communication
- Decoupling در time
- Load balancing

### 3. API Gateway Pattern

```
Client ──> Gateway ──> Services
```

- Single entry point
- Aggregation
- Transformation

### 4. Backend for Frontend (BFF) Pattern

```
Mobile App ──> Mobile BFF ──> Services
Web App ──> Web BFF ──> Services
```

- Different BFFs for different clients
- Optimized APIs
- Client-specific logic

## Best Practices

### 1. استفاده از Events برای Cross-Service Communication

```java
// ✅ Good - Event-Driven
@Transactional
public void createOrder(Order order) {
    orderRepository.save(order);
    eventPublisher.publish(new OrderCreatedEvent(order));
}

// ❌ Bad - Direct Call
public void createOrder(Order order) {
    orderRepository.save(order);
    inventoryService.reserveItems(order.getItems()); // Tight coupling
}
```

### 2. استفاده از Async Communication

```java
// ✅ Good - Async
@KafkaListener(topics = "order-created")
public void handleOrderCreated(OrderCreatedEvent event) {
    // Process asynchronously
}

// ❌ Bad - Sync
public void createOrder(Order order) {
    orderRepository.save(order);
    notificationService.sendEmail(order); // Blocking call
}
```

### 3. Versioning برای Backward Compatibility

```java
// Event Versioning
@Schema(version = "2.0")
public class OrderCreatedEventV2 extends OrderCreatedEvent {
    private String newField;
}

// Consumer handles multiple versions
@KafkaListener(topics = "order-created")
public void handleOrderCreated(String eventJson) {
    OrderCreatedEvent event = deserializeEvent(eventJson);
    // Handle based on version
}
```

### 4. Circuit Breaker Pattern

```java
@Service
public class ExternalServiceClient {
    @CircuitBreaker(name = "external-service")
    public void callExternalService() {
        // Call external service
    }
}
```

## معیارهای اندازه‌گیری Loose Coupling

### 1. Coupling Metrics

- **Afferent Coupling (Ca)**: تعداد سرویس‌هایی که به این سرویس وابسته‌اند
- **Efferent Coupling (Ce)**: تعداد سرویس‌هایی که این سرویس به آن‌ها وابسته است
- **Instability (I)**: Ce / (Ca + Ce)

### 2. Dependency Metrics

- تعداد direct dependencies
- تعداد transitive dependencies
- Depth of dependency tree

### 3. Change Impact

- تعداد سرویس‌هایی که تحت تأثیر تغییر قرار می‌گیرند
- زمان required برای propagate changes

## چالش‌ها و راه‌حل‌ها

### چالش 1: Eventual Consistency

**مشکل:**
در loose coupling، data consistency ممکن است eventual باشد.

**راه‌حل:**

- پذیرش eventual consistency
- استفاده از Saga Pattern برای distributed transactions
- Compensation logic

### چالش 2: Debugging

**مشکل:**
Debugging در event-driven systems پیچیده‌تر است.

**راه‌حل:**

- Distributed tracing (Jaeger, Zipkin)
- Correlation IDs
- Centralized logging

### چالش 3: Testing

**مشکل:**
Testing سرویس‌های loosely coupled پیچیده‌تر است.

**راه‌حل:**

- Contract testing (Pact)
- Integration testing با Testcontainers
- Event mocking

## پیاده‌سازی در پروژه

### تکنولوژی‌های استفاده شده

- **Apache Kafka / Redpanda**: Event broker (توصیه: Redpanda برای performance بهتر و operational simplicity)
- **Spring Cloud Gateway**: API Gateway (برای Docker Compose)
- **Kubernetes Service Discovery**: DNS-based service discovery (برای Kubernetes)
- **Nginx Ingress Controller**: Load balancing و routing (برای Kubernetes)
- **Confluent Schema Registry / Redpanda Built-in**: Schema management
- **Transactional Outbox Pattern**: Reliable event publishing
- برای مقایسه Kafka و Redpanda، به [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison) مراجعه کنید

### ساختار پیاده‌سازی

```
Services
├── Order Service
│   ├── Own Database
│   └── Publishes: OrderCreated, OrderCancelled
├── Inventory Service
│   ├── Own Database
│   └── Subscribes: OrderCreated
└── Notification Service
    ├── Own Database
    └── Subscribes: OrderCreated, OrderCancelled
```

## لینک‌های مفید

- [Loose Coupling in Microservices](https://microservices.io/patterns/decomposition/decompose-by-business-capability.html)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)
- [Database per Service](https://microservices.io/patterns/data/database-per-service.html)
- [Publish-Subscribe Pattern](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PublishSubscribeChannel.html)
- [Service Discovery](https://microservices.io/patterns/service-registry.html)
- [Contract Testing](https://docs.pact.io/)

---

<div align="center">

[↑ بازگشت به بالا](#loose-coupling-اتصال-سست) | [← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

