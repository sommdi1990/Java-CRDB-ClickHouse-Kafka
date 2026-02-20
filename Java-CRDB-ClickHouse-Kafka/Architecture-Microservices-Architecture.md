# معماری میکروسرویس‌ها

<div align="right">

[← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

---

## نمای کلی

این پروژه از معماری میکروسرویس استفاده می‌کند که هر سرویس مسئولیت خاص خود را دارد و به صورت مستقل deploy می‌شود.

## اصول معماری میکروسرویس

### 1. Service Independence

- هر سرویس به صورت مستقل deploy می‌شود
- Database per service
- Technology independence

### 2. Loose Coupling

- کاهش وابستگی بین سرویس‌ها
- استفاده از messaging و events به جای direct API calls
- Contract-based communication
- Service discovery برای dynamic service location
- برای جزئیات بیشتر: [Loose Coupling](Architecture-Loose-Coupling)

### 3. Communication

- **Synchronous**: REST API برای request/response
- **Asynchronous**: Kafka برای event-driven communication
- **API Gateway**: Single entry point
- **Event-Driven Architecture**: برای loose coupling و scalability
- برای جزئیات بیشتر: [Event-Driven Architecture](Architecture-Event-Driven-Architecture)

### 4. Data Management

- هر سرویس database خودش را دارد (در این پروژه: shared database با schema separation)
- Event-driven برای data synchronization
- CQRS pattern برای read/write separation

## ساختار سرویس‌ها

### Core Services

1. **Infrastructure Service**
    - امنیت و احراز هویت
    - مدیریت کاربران
    - زیرساخت مشترک

2. **WorkFlow Service**
    - مدیریت روندهای کاری
    - Business Role Management
    - Business Rules Engine

3. **Report Manager Service**
    - مدیریت گزارش‌ها
    - JasperServer + DynamicReports
    - گزارشات حسابداری

### Gateway Services

4. **UI Gateway**
    - APIهای مخصوص UI
    - Aggregation
    - Response transformation

5. **External Gateway**
    - APIهای عمومی
    - Rate limiting
    - API versioning

6. **Input Gateway**
    - سرویس‌های ورودی
    - Webhook management
    - External service integration

### Business Services (DDD)

7. **Accounting Service**
    - سیستم حسابداری
    - اسناد و حساب‌ها
    - دفاتر سالیانه

8. **Domain Services**
    - هر دامنه به صورت مستقل
    - DDD architecture

### Infrastructure Services

9. **GraphQL Service**
    - GraphQL API
    - Query optimization

10. **Messaging Service**
    - SMS, Email, Notifications
    - Template management

11. **Document Archive Service**
    - مدیریت اسناد
    - Full-text search

12. **eSignature Service**
    - امضای دیجیتال
    - Integration با سرویس‌های eSignature

13. **Document Versioning Service**
    - مدیریت نسخه‌های اسناد
    - Version control

14. **ClickHouse Manager Service**
    - مدیریت لاگ‌ها و آمارها
    - Analytics

15. **Schedule & Event Manager Service**
    - مدیریت Scheduleها
    - Job scheduling

## Communication Patterns

### Synchronous Communication

- REST API
- GraphQL
- gRPC (در صورت نیاز)

### Asynchronous Communication

- Apache Kafka / Redpanda (توصیه: Redpanda برای performance بهتر)
- Event-driven architecture
- Pub/Sub pattern
- Transactional Outbox Pattern برای reliable event publishing
- برای مقایسه Kafka و Redpanda، به [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison) مراجعه کنید

## Service Discovery

- **Spring Cloud Gateway**: برای routing در Docker Compose
- **Kubernetes Service Discovery**: DNS-based service discovery در Kubernetes
- **Nginx**: برای load balancing در Docker Compose
- **Nginx Ingress Controller**: برای load balancing و routing در Kubernetes
- **Consul**: برای service discovery (اختیاری)

## Data Consistency

- **Eventual Consistency**: بین سرویس‌ها
- **Transactional Outbox Pattern**: برای reliable event publishing
- **Saga Pattern**: برای distributed transactions

## Deployment

- **Docker**: Containerization
- **Docker Compose**: برای development و local testing
- **Kubernetes**: Container Orchestration برای production و stage environments
    - استفاده از Helm برای package management
    - Ingress Controller (Nginx Ingress) برای routing
    - HPA (Horizontal Pod Autoscaler) برای auto-scaling
    - StatefulSet برای databases و stateful services
    - ConfigMap و Secrets برای configuration management
    - برای جزئیات کامل، به [راهنمای کامل Kubernetes](Kubernetes) مراجعه کنید

## Monitoring

- **Spring Boot Admin**: Application monitoring
- **Prometheus**: Metrics
- **Grafana**: Visualization
- **Jaeger**: Distributed tracing

## لینک‌های مفید

- [Microservices Patterns](https://microservices.io/patterns/)
- [Spring Cloud Documentation](https://spring.io/projects/spring-cloud)
- [Service Discovery](https://microservices.io/patterns/service-registry.html)
- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Distributed Tracing](https://opentracing.io/)

---

<div align="center">

[↑ بازگشت به بالا](#معماری-میکروسرویسها) | [← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

