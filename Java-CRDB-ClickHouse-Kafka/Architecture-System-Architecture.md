# معماری کلی سیستم

<div align="right">

[← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

---

## نمای کلی

سیستم با معماری میکروسرویس طراحی شده است که شامل لایه‌های زیر می‌شود:

### 1. Frontend Layer

- React + TypeScript + Vite
- معماری Micro Frontends
- Redux Toolkit + RTK Query برای state management

### 2. Gateway Layer

- **UI Gateway**: APIهای مخصوص رابط کاربری
- **External Gateway**: APIهای عمومی برای سیستم‌های خارجی
- **Input Gateway**: مدیریت سرویس‌های ورودی و Webhookها

### 3. Business Services Layer

- سرویس‌های دامنه‌محور با معماری DDD
- هر دامنه به صورت مستقل

### 4. Infrastructure Services Layer

- Infrastructure Service
- WorkFlow Service
- Report Manager Service
- ClickHouse Manager Service
- Schedule & Event Manager Service

### 5. Data & Messaging Layer

- CockroachDB (دیتابیس اصلی - Distributed SQL)
- ClickHouse (دیتابیس تحلیلی - Columnar)
- Redis (کش و buffer)
- Kafka/Redpanda (messaging و event streaming)
- Flyway (Database Migration)

### 6. Infrastructure Layer

- Docker & Docker Compose (برای development)
- Kubernetes (برای production و stage)
- Nginx (Load Balancer و Ingress Controller)
- VPN Gateway (OpenVPN/WireGuard)
- VMware ESXi 8.0 (مجازی‌سازی)
- Rocky Linux 9 (سیستم عامل)

## جریان داده

### در محیط Development (Docker Compose)

```
User Request
    ↓
Nginx (Load Balancer)
    ↓
UI Gateway / External Gateway / Input Gateway
    ↓
Business Services / Infrastructure Services
    ↓
CockroachDB / Redis / Kafka
    ↓
Response
```

### در محیط Production/Stage (Kubernetes)

```
User Request
    ↓
Nginx Ingress Controller (Load Balancer)
    ↓
Kubernetes Service (Load Balancing)
    ↓
UI Gateway / External Gateway / Input Gateway (Pods)
    ↓
Business Services / Infrastructure Services (Pods)
    ↓
CockroachDB / Redis / Kafka (StatefulSets)
    ↓
Response
```

## Communication Patterns

- **Synchronous**: REST API برای request/response
- **Asynchronous**: Kafka برای event-driven communication
- **Caching**: Redis برای بهبود performance

## لینک‌های مفید

- [Microservices Architecture](https://microservices.io/)
- [System Design Patterns](https://martinfowler.com/architecture/)
- [REST API Design](https://restfulapi.net/)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Caching Strategies](https://aws.amazon.com/caching/best-practices/)
- [Redis Documentation](https://redis.io/docs/)

---

<div align="center">

[↑ بازگشت به بالا](#معماری-کلی-سیستم) | [← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

