# Java-CRDB-ClickHouse-Kafka

یک پلتفرم یکپارچه و مقیاس‌پذیر برای مدیریت سیستم‌های سازمانی بزرگ با استفاده از معماری میکروسرویس و تکنولوژی‌های مدرن.

## 📋 فهرست مطالب

- [معرفی پروژه](#معرفی-پروژه)
- [معماری سیستم](#معماری-سیستم)
- [تکنولوژی‌های استفاده شده](#تکنولوژی‌های-استفاده-شده)
- [ساختار پروژه](#ساختار-پروژه)
- [شروع سریع](#شروع-سریع)
- [مستندات](#مستندات)
- [CI/CD](#cicd)
- [مشارکت](#مشارکت)

## 🎯 معرفی پروژه

این پروژه یک پلتفرم سازمانی کامل است که شامل:

- ✅ مدیریت یکپارچه کاربران و احراز هویت
- ✅ سیستم مدیریت روندهای کاری (Workflow) و نقش‌های تجاری
- ✅ سیستم گزارش‌دهی پیشرفته (JasperServer + DynamicReports)
- ✅ Document Generator Service (Puppeteer) برای تولید مستندات چند صفحه‌ای از HTML به PDF
- ✅ مدیریت دامنه‌های تجاری با معماری DDD
- ✅ سیستم حسابداری کامل با اسناد، حساب‌ها و دفاتر سالیانه
- ✅ مانیتورینگ و لاگینگ پیشرفته
- ✅ قابلیت مقیاس‌پذیری بالا و امنیت
- ✅ GraphQL API برای کوئری‌های پیشرفته
- ✅ امضای دیجیتال و مدیریت نسخه‌های اسناد
- ✅ سیستم ارسال پیام‌ها (SMS, Email, Notification)
- ✅ پشتیبانی از Mobile و PWA
- ✅ سیستم مدیریت اسناد یکپارچه (Mayan EDMS)
- ✅ سیستم تقویم پیشرفته با پشتیبانی از تقویم شمسی و میلادی
- ✅ Transactional Outbox Pattern برای حل مشکل Dual-Write

## 📋 صورت مسئله و چالش‌ها

### چالش‌های موجود

این پروژه برای حل چالش‌های زیر طراحی شده است:

1. **نیاز به سیستم یکپارچه برای مدیریت چندین دامنه تجاری**
    - مدیریت چندین دامنه تجاری در یک پلتفرم
    - جداسازی منطقی دامنه‌ها با حفظ یکپارچگی
    - استفاده از معماری DDD برای مدیریت پیچیدگی

2. **نیاز به گزارش‌دهی پویا و انعطاف‌پذیر**
    - گزارش‌های استاندارد با JasperServer
    - گزارش‌های کاملاً پویا با DynamicReports
    - گزارش‌های حسابداری (ترازنامه، سود و زیان، گردش حساب، دفتر کل، دفتر معین)
    - GraphQL API برای کوئری‌های پیشرفته

3. **نیاز به مقیاس‌پذیری و کارایی بالا**
    - معماری میکروسرویس برای مقیاس‌پذیری افقی
    - استفاده از CockroachDB برای distributed SQL
    - استفاده از ClickHouse برای تحلیل لاگ‌ها و آمارها
    - Redis برای caching و بهبود عملکرد

4. **نیاز به امنیت و مدیریت دسترسی پیشرفته**
    - Keycloak برای Identity & Access Management
    - OAuth 2.0 و OpenID Connect
    - مدیریت نقش‌ها و دسترسی‌ها
    - امنیت در سطح API و سرویس

5. **نیاز به مانیتورینگ و تحلیل لاگ‌ها**
    - Grafana + Prometheus برای metrics
    - Spring Boot Admin برای application monitoring
    - ClickHouse برای تحلیل لاگ‌ها
    - Centralized logging

6. **نیاز به مدیریت اسناد و فایل‌ها**
    - سیستم آرشیو اسناد و فایل‌ها
    - Mayan EDMS برای مدیریت اسناد یکپارچه
    - Document Versioning برای مدیریت نسخه‌های اسناد
    - eSignature برای امضای دیجیتال

7. **نیاز به سیستم تقویم و مدیریت رویدادها**
    - سیستم تقویم پیشرفته شبیه Google Calendar
    - پشتیبانی از تقویم شمسی (Persian/Jalali) و میلادی (Gregorian)
    - مدیریت رویدادها و یادآوری‌ها
    - تقویم‌های اشتراکی و گروهی

8. **نیاز به سیستم حسابداری کامل**
    - مدیریت اسناد حسابداری (سند، فاکتور، چک، و غیره)
    - مدیریت حساب‌ها (کل، معین، تفصیلی)
    - دفاتر سالیانه (دفتر کل، معین، روزنامه)
    - گزارشات مالی و حسابداری

9. **نیاز به حل مشکل Dual-Write در میکروسرویس‌ها**
    - Transactional Outbox Pattern برای reliable event publishing
    - حل مشکل inconsistency بین database و message queue
    - تضمین ارسال events (at-least-once delivery)

10. **نیاز به سیستم ارسال پیام‌ها**
    - ارسال SMS از طریق gatewayهای مختلف
    - ارسال Email با template management
    - Push Notifications و In-app Notifications
    - Delivery tracking و retry mechanism

11. **نیاز به پشتیبانی از Mobile و Web Responsive**
    - Mobile Application (React Native یا PWA)
    - Web Responsive (Mobile-first design)
    - PWA (Progressive Web App) با offline capability

### راه‌حل پیشنهادی

پیاده‌سازی یک پلتفرم مبتنی بر میکروسرویس با استفاده از:

- **Backend**: Java Spring Boot 4.0.1 با معماری DDD و پشتیبانی از GraalVM Native
- **Frontend**: React + TypeScript با معماری Micro Frontends
- **Database**: CockroachDB (اصلی) + ClickHouse (تحلیلی) + Redis (کش)
- **Database Migration**: Flyway برای مدیریت schema و migrations
- **Messaging**: Apache Kafka با Transactional Outbox Pattern
- **Security**: Keycloak برای Identity & Access Management
- **Monitoring**: Grafana + Prometheus + Spring Boot Admin
- **Infrastructure**: Docker + Docker Compose + Kubernetes (برای production و stage) + Nginx
- **Kubernetes Infrastructure**: دو سرور فیزیکی (64GB RAM هر کدام) با VMware ESXi 8، Rocky Linux 10، و Kubernetes
  Cluster مرکزی
- **Document Management**: Mayan EDMS برای مدیریت اسناد یکپارچه
- **Calendar System**: سیستم تقویم پیشرفته با پشتیبانی از تقویم شمسی و میلادی
- **Accounting**: سیستم حسابداری کامل با گزارشات مالی

برای جزئیات کامل، به [پروپوزال اولیه پروژه](./Java-CRDB-ClickHouse-Kafka.wiki/Proposal.md) مراجعه کنید.

## 🏗️ معماری سیستم

سیستم با معماری میکروسرویس طراحی شده است:

```
Frontend (React + TypeScript)
    ↓
Gateway Layer (UI / External / Input)
    ↓
Business Services (DDD) + Infrastructure Services
    ↓
Data Layer (CockroachDB / ClickHouse / Redis / Kafka)
```

برای جزئیات بیشتر، به [مستندات معماری](./Java-CRDB-ClickHouse-Kafka.wiki/Architecture-Home.md) مراجعه کنید.

## 🛠️ تکنولوژی‌های استفاده شده

### Backend

- **Java Spring Boot 4.0.1** - Framework اصلی (با پشتیبانی از GraalVM Native)
- **Spring Security** - امنیت
- **Spring Cloud** - میکروسرویس
- **Spring GraphQL** - GraphQL API
- **Camunda BPM** - Workflow Engine
- **JasperServer + DynamicReports** - گزارش‌دهی
- **Puppeteer** - Document Generator Service (HTML to PDF)
- **Apache Kafka / Redpanda** - Messaging (توصیه: Redpanda برای performance بهتر)
- **Keycloak** - Identity & Access Management
- **Accounting Service** - سیستم حسابداری کامل
- **Transactional Outbox Pattern** - حل مشکل Dual-Write
- **Messaging Service** - SMS, Email, Notifications
- **Document Archive** - مدیریت اسناد و فایل‌ها
- **eSignature** - امضای دیجیتال
- **Document Versioning** - مدیریت نسخه‌های اسناد

### Frontend

- **React 18+** - کتابخانه UI
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Redux Toolkit + RTK Query** - State management
- **React Query** - Server state management
- **React Hook Form** - Form management
- **AG Grid / TanStack Table** - Data tables
- **Recharts / Chart.js** - Charts & visualization
- **Storybook** - Component development
- **Micro Frontends** - معماری frontend
- **PWA** - Progressive Web App
- **React Native** - Mobile Application (اختیاری)

### Databases

- **CockroachDB** - دیتابیس اصلی (Distributed SQL)
- **ClickHouse** - دیتابیس تحلیلی (لاگ‌ها و آمارها)
- **Redis** - Cache و Buffer

### Infrastructure

- **Docker** - Containerization
- **Docker Compose** - Orchestration (برای development)
- **Kubernetes** - Container Orchestration (برای production و stage environments)
- **Nginx** - Reverse Proxy, Load Balancer & Ingress Controller
- **Grafana + Prometheus** - Monitoring و Observability
- **Spring Boot Admin** - Application Monitoring
- **VPN Gateway** (OpenVPN/WireGuard) - دسترسی امن از راه دور
- **VMware ESXi 8.0** - مجازی‌سازی و مدیریت VMها
- **Rocky Linux 10** - سیستم عامل سرورها (برای Kubernetes Cluster)
- **Rocky Linux 9** - سیستم عامل سرورها (برای سایر محیط‌ها)

### Testing

- **JUnit 5** - Unit testing
- **Mockito** - Mocking
- **Testcontainers** - Integration testing
- **Jest + React Testing Library** - Frontend testing
- **Cypress** - E2E testing

## 📁 ساختار پروژه

```
Java-CRDB-ClickHouse-Kafka/
├── backend/
│   ├── infrastructure-service/      # زیرساخت و امنیت
│   ├── workflow-service/            # مدیریت روندهای کاری
│   ├── report-manager-service/      # مدیریت گزارش‌ها
│   │   └── document-generator/      # Document Generator Service (Puppeteer)
│   ├── gateway-ui/                  # Gateway برای UI
│   ├── gateway-external/            # Gateway برای APIهای خارجی
│   ├── gateway-input/               # Gateway برای سرویس‌های ورودی
│   ├── business-services/           # سرویس‌های دامنه (DDD)
│   │   ├── domain-1/
│   │   ├── domain-2/
│   │   └── shared-kernel/
│   ├── graphql-service/             # GraphQL API
│   ├── messaging-service/           # SMS, Email, Notifications
│   ├── document-archive-service/    # آرشیو اسناد و فایل‌ها
│   ├── esignature-service/          # امضای دیجیتال
│   ├── document-versioning-service/ # مدیریت نسخه‌های اسناد
│   ├── clickhouse-manager-service/  # مدیریت ClickHouse
│   ├── schedule-event-service/      # مدیریت Schedule و Event
│   └── testing-module/             # ماژول تست
├── frontend/
│   ├── shell/                      # Micro Frontend Shell
│   ├── main-page/                  # صفحه اصلی
│   ├── user-panel/                 # پنل کاربران
│   ├── admin-panel/                # پنل مدیران
│   └── mobile/                     # Mobile App (React Native یا PWA)
├── docker/
│   ├── docker-compose.yml          # Docker Compose configuration
│   └── Dockerfile.*                # Dockerfiles
├── docs/                           # مستندات اضافی
├── .github/
│   └── workflows/                  # CI/CD workflows
└── Java-CRDB-ClickHouse-Kafka.wiki/ # مستندات ویکی
```

## 🚀 شروع سریع

### پیش‌نیازها

- Java 17+
- Node.js 18+
- Docker & Docker Compose
- Maven 3.9+

### نصب و راه‌اندازی

1. **Clone پروژه:**

```bash
git clone https://github.com/your-org/Java-CRDB-ClickHouse-Kafka.git
cd Java-CRDB-ClickHouse-Kafka
```

2. **راه‌اندازی دیتابیس‌ها و سرویس‌های زیرساخت:**

```bash
docker-compose up -d
```

3. **راه‌اندازی Backend Services:**

```bash
cd backend
mvn clean install
# راه‌اندازی هر سرویس به صورت جداگانه
```

4. **راه‌اندازی Frontend:**

```bash
cd frontend
npm install
npm run dev
```

برای راهنمای کامل، به [مستندات راهنمای شروع](./Java-CRDB-ClickHouse-Kafka.wiki/Development-Getting-Started.md) مراجعه
کنید.

## 📚 مستندات

تمام مستندات پروژه در پوشه [Java-CRDB-ClickHouse-Kafka.wiki](./Java-CRDB-ClickHouse-Kafka.wiki/) قرار دارد:

### مستندات کلیدی

- 📋 **[پروپوزال اولیه پروژه](./Java-CRDB-ClickHouse-Kafka.wiki/Proposal.md)** - مستندات کامل پروپوزال، معماری، و توجیهات
  فنی و بیزینسی
- ☸️ **[پروپوزال Kubernetes](./Java-CRDB-ClickHouse-Kafka.wiki/Proposal-Kubernetes.md)** ⭐ - پروپوزال کامل برای
  راه‌اندازی Kubernetes روی دو سرور فیزیکی با VMware ESXi 8
- 🔧 **[راهنمای فنی پیاده‌سازی Kubernetes](./Java-CRDB-ClickHouse-Kafka.wiki/Kubernetes-Implementation-Guide.md)** ⭐ -
  راهنمای قدم به قدم پیاده‌سازی Kubernetes
- 🐳 **[راه‌اندازی Registry و Nexus](./Java-CRDB-ClickHouse-Kafka.wiki/Infrastructure-Registry-Nexus-Setup.md)** ⭐ -
  راهنمای کامل راه‌اندازی Docker Registry و Nexus Repository Manager
- 📅 **[گانت چارت Kubernetes](./Java-CRDB-ClickHouse-Kafka.wiki/Gantt-Plan-Kubernetes.md)** ⭐ - برنامه‌ریزی زمانی برای
  پیاده‌سازی Kubernetes (4 اسپرینت سه‌هفته‌ای)
- 🏗️ **[معماری سیستم](./Java-CRDB-ClickHouse-Kafka.wiki/Architecture-Home.md)** - معماری کلی، میکروسرویس‌ها، DDD، امنیت
- ☸️ **[راهنمای کامل Kubernetes](./Java-CRDB-ClickHouse-Kafka.wiki/Kubernetes.md)** - از صفر تا صد Kubernetes برای
  production و stage
- 🖥️ **[زیرساخت و Infrastructure](./Java-CRDB-ClickHouse-Kafka.wiki/Infrastructure-Setup.md)** - VMware ESXi، VPN
  Gateway، مدیریت از راه دور
- 🔗 **[فهرست لینک‌های مفید](./Java-CRDB-ClickHouse-Kafka.wiki/References.md)** - تمام لینک‌های مستندات رسمی

### مستندات اصلی

- [📋 پروپوزال اولیه پروژه](./Java-CRDB-ClickHouse-Kafka.wiki/Proposal.md) - مستندات کامل پروپوزال و توجیهات
- [☸️ پروپوزال Kubernetes](./Java-CRDB-ClickHouse-Kafka.wiki/Proposal-Kubernetes.md) ⭐ - پروپوزال کامل برای راه‌اندازی
  Kubernetes
- [🔧 راهنمای فنی پیاده‌سازی Kubernetes](./Java-CRDB-ClickHouse-Kafka.wiki/Kubernetes-Implementation-Guide.md) ⭐ -
  راهنمای قدم به قدم
- [📅 گانت چارت Kubernetes](./Java-CRDB-ClickHouse-Kafka.wiki/Gantt-Plan-Kubernetes.md) ⭐ - برنامه‌ریزی زمانی

### مستندات فنی

- [🏗️ معماری سیستم](./Java-CRDB-ClickHouse-Kafka.wiki/Architecture-Home.md)
- [🔧 کامپوننت‌های Backend](./Java-CRDB-ClickHouse-Kafka.wiki/Backend-Home.md)
- [🚀 راهنمای کامل GraalVM Native](./Java-CRDB-ClickHouse-Kafka.wiki/GraalVM-Native.md) ⭐
- [🎨 کامپوننت‌های Frontend](./Java-CRDB-ClickHouse-Kafka.wiki/Frontend-Home.md)
- [🗄️ دیتابیس‌ها](./Java-CRDB-ClickHouse-Kafka.wiki/Database-Home.md)
- [🔐 سیستم‌های امنیتی](./Java-CRDB-ClickHouse-Kafka.wiki/Security-Home.md)
- [📊 مانیتورینگ و لاگینگ](./Java-CRDB-ClickHouse-Kafka.wiki/Monitoring-Home.md)
- [🐳 Docker](./Java-CRDB-ClickHouse-Kafka.wiki/Docker-Home.md)
- [🔄 Kafka و Messaging](./Java-CRDB-ClickHouse-Kafka.wiki/Kafka-Home.md)
- [☸️ Kubernetes و Orchestration](./Java-CRDB-ClickHouse-Kafka.wiki/Kubernetes.md)
- [🌐 Nginx و Routing](./Java-CRDB-ClickHouse-Kafka.wiki/Nginx-Home.md)

### مستندات بیزینسی

- [📝 مستندات بیزینسی](./Java-CRDB-ClickHouse-Kafka.wiki/Business-Home.md)

### راهنماهای توسعه

- [🧪 تست و کیفیت](./Java-CRDB-ClickHouse-Kafka.wiki/Testing-Home.md)
- [💻 راهنماهای توسعه](./Java-CRDB-ClickHouse-Kafka.wiki/Development-Home.md)

## 🔄 CI/CD

پروژه از CI/CD pipeline برای:

- ✅ Automated testing
- ✅ Security scanning
- ✅ Docker image building
- ✅ Automated deployment
- ✅ Version management

برای جزئیات بیشتر، به [مستندات CI/CD](./Java-CRDB-ClickHouse-Kafka.wiki/CI-CD-Home.md) مراجعه کنید.

## 🔒 امنیت

- استفاده از Docker Secrets برای مدیریت اطلاعات حساس
- Multi-stage builds برای کاهش اندازه و افزایش امنیت imageها
- Non-root user در containers
- Security scanning با Trivy و Snyk

برای جزئیات بیشتر، به [مستندات امنیت Docker](./Java-CRDB-ClickHouse-Kafka.wiki/Docker-Docker-Security.md) مراجعه کنید.

## 📊 مانیتورینگ

- **Spring Boot Admin**: مانیتورینگ applicationها
- **Grafana**: Visualization و dashboards
- **Prometheus**: Metrics collection
- **ClickHouse**: تحلیل لاگ‌ها و آمارها

## 🤝 مشارکت

برای مشارکت در پروژه:

1. Fork کنید
2. یک branch جدید ایجاد کنید (`git checkout -b feature/AmazingFeature`)
3. تغییرات را commit کنید (`git commit -m 'Add some AmazingFeature'`)
4. Push کنید (`git push origin feature/AmazingFeature`)
5. یک Pull Request باز کنید

برای جزئیات بیشتر، به [Git Workflow](./Java-CRDB-ClickHouse-Kafka.wiki/Development-Git-Workflow.md) مراجعه کنید.

## 📄 لایسنس

این پروژه تحت لایسنس [MIT License](LICENSE) منتشر شده است.

## 👥 تیم

- **Project Lead**: [نام]
- **Backend Team**: [نام‌ها]
- **Frontend Team**: [نام‌ها]
- **DevOps Team**: [نام‌ها]

## 📞 تماس

برای سوالات و پشتیبانی:

- 📧 Email: [email]
- 💬 Issues: [GitHub Issues](https://github.com/your-org/Java-CRDB-ClickHouse-Kafka/issues)
- 📖 Wiki: [مستندات کامل](./Java-CRDB-ClickHouse-Kafka.wiki/Home.md)

---

**نکته**: این پروژه در حال توسعه است. برای آخرین تغییرات، به [Changelog](./CHANGELOG.md) مراجعه کنید.
