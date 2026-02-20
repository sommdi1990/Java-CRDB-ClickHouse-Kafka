# Java-CRDB-ClickHouse-Kafka

<div align="center">

**یک پلتفرم یکپارچه و مقیاس‌پذیر برای مدیریت سیستم‌های سازمانی بزرگ**

با استفاده از معماری میکروسرویس و تکنولوژی‌های مدرن

[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-4.0.1-brightgreen)](https://spring.io/projects/spring-boot)
[![React](https://img.shields.io/badge/React-18+-blue)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

</div>

---

## 📖 درباره پروژه

این پروژه یک پلتفرم سازمانی کامل است که با استفاده از معماری میکروسرویس و تکنولوژی‌های مدرن، قابلیت‌های زیر را فراهم
می‌کند:

- ✅ مدیریت یکپارچه کاربران و احراز هویت
- ✅ سیستم مدیریت روندهای کاری (Workflow) و نقش‌های تجاری
- ✅ سیستم گزارش‌دهی پیشرفته (JasperServer + DynamicReports)
- ✅ مدیریت دامنه‌های تجاری با معماری DDD
- ✅ سیستم حسابداری کامل با اسناد، حساب‌ها و دفاتر سالیانه
- ✅ مانیتورینگ و لاگینگ پیشرفته
- ✅ قابلیت مقیاس‌پذیری بالا و امنیت
- ✅ GraphQL API برای کوئری‌های پیشرفته
- ✅ امضای دیجیتال و مدیریت نسخه‌های اسناد
- ✅ سیستم ارسال پیام‌ها (SMS, Email, Notification)
- ✅ پشتیبانی از Mobile و PWA

---

## 🚀 شروع سریع

### مستندات اصلی

- 📋 **[پروپوزال اولیه پروژه](Proposal)** - مستندات کامل پروپوزال، معماری، و توجیهات فنی و بیزینسی
- ☸️ **[پروپوزال Kubernetes](Proposal-Kubernetes)** ⭐ - پروپوزال کامل برای راه‌اندازی Kubernetes روی دو سرور فیزیکی با
  VMware ESXi 8
- 🔧 **[راهنمای فنی پیاده‌سازی Kubernetes](Kubernetes-Implementation-Guide)** ⭐ - راهنمای قدم به قدم پیاده‌سازی
  Kubernetes
- 🐳 **[راه‌اندازی Registry و Nexus](Infrastructure-Registry-Nexus-Setup)** ⭐ - راهنمای کامل راه‌اندازی Docker Registry و
  Nexus Repository Manager
- 📦 **[لیست کامل Images و Helm Charts](Complete-Images-Manifests-Helm-Charts-List)** ⭐ - لیست کامل تمام images،
  manifests و Helm charts مورد نیاز
- 🌐 **[راهنمای تنظیمات Proxy و Repository موقت](Kubernetes-Proxy-Setup)** ⭐ - راهنمای کامل برای استفاده از Proxy و
  Registry محلی
- ⚡ **[راهنمای سریع Proxy](QUICK-START-PROXY)** - راهنمای سریع برای تنظیمات Proxy و نصب Calico
- 📅 **[گانت چارت Kubernetes](Gantt-Plan-Kubernetes)** ⭐ - برنامه‌ریزی زمانی برای پیاده‌سازی Kubernetes (4 اسپرینت
  سه‌هفته‌ای)
- 🔗 **[فهرست لینک‌های مفید و مستندات](References)** - فهرست کامل تمام لینک‌های مفید و مستندات رسمی تکنولوژی‌های استفاده
  شده

### راهنماهای سریع

- 📚 **[راهنمای شروع](Development-Getting-Started)** - راهنمای نصب و راه‌اندازی پروژه
- 🏗️ **[معماری سیستم](Architecture-System-Architecture)** - معماری کلی سیستم
- 🔧 **[کامپوننت‌های Backend](Backend-Home)** - تمام سرویس‌های backend
- 🎨 **[کامپوننت‌های Frontend](Frontend-Home)** - تمام کامپوننت‌های frontend

---

## 📚 فهرست مطالب

### 🏗️ معماری سیستم

- [معماری کلی سیستم](Architecture-System-Architecture)
- [معماری میکروسرویس‌ها](Architecture-Microservices-Architecture)
- [معماری DDD](Architecture-DDD-Architecture)
- [معماری امنیت](Architecture-Security-Architecture)
- [Transactional Outbox Pattern](Architecture-Transactional-Outbox-Pattern)

### 🔧 کامپوننت‌های Backend

- [پروژه Infrastructure](Backend-Infrastructure)
- [پروژه WorkFlow](Backend-WorkFlow)
- [پروژه Report Manager](Backend-Report-Manager)
- [پروژه Accounting Service](Backend-Accounting-Service)
- [Gateway UI](Backend-Gateway-UI)
- [Gateway External](Backend-Gateway-External)
- [Gateway Input](Backend-Gateway-Input)
- [Business Services (DDD)](Backend-Business-Services)
- [GraphQL Service](Backend-GraphQL-Service)
- [Messaging Service](Backend-Messaging-Service)
- [Document Archive Service](Backend-Document-Archive-Service)
- [eSignature Service](Backend-eSignature-Service)
- [Document Versioning](Backend-Document-Versioning)
- [ClickHouse Manager](Backend-ClickHouse-Manager)
- [Schedule & Event Manager](Backend-Schedule-Event-Manager)
- [ماژول تست](Backend-Testing-Module)

### 🎨 کامپوننت‌های Frontend

- [معماری Micro Frontends](Frontend-Micro-Frontends)
- [صفحه اصلی سایت](Frontend-Main-Page)
- [پنل کاربران](Frontend-User-Panel)
- [پنل مدیران](Frontend-Admin-Panel)
- [Mobile Application](Frontend-Mobile-Application)
- [Web Responsive & PWA](Frontend-Web-Responsive-PWA)
- [UI Libraries & Tools](Frontend-UI-Libraries-Tools)
- [تست‌های Frontend](Frontend-Testing)

### 🗄️ دیتابیس‌ها

- [CockroachDB](Database-CockroachDB)
- [ClickHouse](Database-ClickHouse)
- [Redis](Database-Redis)

### 🔐 سیستم‌های امنیتی و احراز هویت

- [راهنمای جامع استانداردهای امنیتی OWASP](Security-OWASP-Comprehensive-Guide) ⭐ - راهنمای کامل OWASP Top 10، API
  Security، ASVS، Dependency Check و ZAP
- [Keycloak](Security-Keycloak)
- [مدیریت کاربران](Security-User-Management)
- [مدیریت دسترسی‌ها](Security-Access-Control)

### 📊 مانیتورینگ و لاگینگ

- [Spring Boot Admin](Monitoring-Spring-Boot-Admin)
- [Grafana](Monitoring-Grafana)
- [Prometheus](Monitoring-Prometheus)

### 🐳 Docker و Containerization

- [Docker Compose](Docker-Docker-Compose)
- [Docker Security](Docker-Docker-Security)
- [Multi-stage Builds](Docker-Multi-stage-Builds)

### ☸️ Kubernetes و Orchestration

- [پروپوزال Kubernetes](Proposal-Kubernetes) ⭐ - پروپوزال کامل برای راه‌اندازی Kubernetes
- [راهنمای فنی پیاده‌سازی Kubernetes](Kubernetes-Implementation-Guide) ⭐ - راهنمای قدم به قدم پیاده‌سازی
- [راهنمای کامل Kubernetes - از صفر تا صد](Kubernetes)

### 🚀 GraalVM Native

- [راهنمای کامل GraalVM Native برای Spring Boot 4.0.1](GraalVM-Native) ⭐

### 🚀 CI/CD و DevOps

- [CI/CD Pipeline](CI-CD-Pipeline)
- [نسخه‌گذاری](CI-CD-Versioning)
- [Deployment](CI-CD-Deployment)

### 🔄 Kafka و Messaging

- [راهنمای کامل Redpanda - جایگزین مدرن برای Apache Kafka](Redpanda) ⭐ (توصیه شده)
- [معماری Kafka](Kafka-Architecture)
- [Topic Management](Kafka-Topic-Management)
- [Event Streaming](Kafka-Event-Streaming)

### 🌐 Nginx و Routing

- [Routing Configuration](Nginx-Routing)
- [Load Balancing](Nginx-Load-Balancing)
- [SSL/TLS](Nginx-SSL-TLS)

### 🖥️ زیرساخت و Infrastructure

- [زیرساخت پیشنهادی و عملیاتی](Infrastructure-Setup)
- [VPN Gateway و Routing هوشمند](Infrastructure-VPN-Routing)
- [راه‌اندازی Registry و Nexus](Infrastructure-Registry-Nexus-Setup) ⭐
- [لیست کامل Images و Helm Charts](Complete-Images-Manifests-Helm-Charts-List) ⭐

### 📝 مستندات بیزینسی

- [نیازمندی‌های بیزینسی](Business-Business-Requirements)
- [روندهای کاری](Business-Workflows)
- [قواعد تجاری](Business-Business-Rules)
- [گزارش‌های مدیریتی](Business-Management-Reports)

### 🧪 تست و کیفیت

- [استراتژی تست](Testing-Test-Strategy)
- [Unit Testing](Testing-Unit-Testing)
- [Integration Testing](Testing-Integration-Testing)
- [E2E Testing](Testing-E2E-Testing)

### 📚 راهنماهای توسعه

- [راهنمای شروع](Development-Getting-Started)
- [استانداردهای کدنویسی](Development-Coding-Standards)
- [Git Workflow](Development-Git-Workflow)
- [API Documentation](Development-API-Documentation)

---

## 🛠️ تکنولوژی‌های کلیدی

### Backend

- **Java Spring Boot 4.0.1** - Framework اصلی (با پشتیبانی از GraalVM Native)
- **Spring Security** - امنیت
- **Spring Cloud** - میکروسرویس
- **Spring GraphQL** - GraphQL API
- **Camunda BPM** - Workflow Engine
- **JasperServer + DynamicReports** - گزارش‌دهی
- **Apache Kafka** - Messaging
- **Keycloak** - Identity & Access Management

### Frontend

- **React 18+** - کتابخانه UI
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Redux Toolkit + RTK Query** - State management
- **React Query** - Server state management
- **Micro Frontends** - معماری frontend

### Databases

- **CockroachDB** - دیتابیس اصلی
- **ClickHouse** - دیتابیس تحلیلی
- **Redis** - Cache و Buffer

### Infrastructure

- **Docker** - Containerization
- **Docker Compose** - Orchestration (برای development)
- **Kubernetes** - Container Orchestration (برای production و stage environments)
- **Nginx** - Reverse Proxy, Load Balancer و Ingress Controller
- **Grafana + Prometheus** - Monitoring و Observability
- **Spring Boot Admin** - Application Monitoring
- **VPN Gateway** (OpenVPN/WireGuard) - دسترسی امن از راه دور
- **VMware ESXi 8.0** - مجازی‌سازی و مدیریت VMها
- **Rocky Linux 9** - سیستم عامل سرورها

---

## 📖 مستندات بیشتر

برای اطلاعات بیشتر، به [پروپوزال اولیه](Proposal) و [فهرست لینک‌های مفید](References) مراجعه کنید.

---

## 🤝 مشارکت

برای مشارکت در پروژه، به [Git Workflow](Development-Git-Workflow) و [استانداردهای کدنویسی](Development-Coding-Standards)
مراجعه کنید.

---

## 📞 تماس

برای سوالات و پشتیبانی:

- 📧 Issues: GitHub Issues
- 📖 Wiki: [مستندات کامل](Home)

---

<div align="center">

**نکته**: این مستندات به صورت مداوم به‌روزرسانی می‌شوند.

</div>
