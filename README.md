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
- ✅ مدیریت دامنه‌های تجاری با معماری DDD
- ✅ سیستم حسابداری کامل با اسناد، حساب‌ها و دفاتر سالیانه
- ✅ مانیتورینگ و لاگینگ پیشرفته
- ✅ قابلیت مقیاس‌پذیری بالا و امنیت
- ✅ GraphQL API برای کوئری‌های پیشرفته
- ✅ امضای دیجیتال و مدیریت نسخه‌های اسناد
- ✅ سیستم ارسال پیام‌ها (SMS, Email, Notification)
- ✅ پشتیبانی از Mobile و PWA

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

برای جزئیات بیشتر، به [مستندات معماری](./Java-CRDB-ClickHouse-Kafka.wiki/Architecture/Home.md) مراجعه کنید.

## 🛠️ تکنولوژی‌های استفاده شده

### Backend

- **Java Spring Boot 3.2.x** - Framework اصلی
- **Spring Security** - امنیت
- **Spring Cloud** - میکروسرویس
- **Spring GraphQL** - GraphQL API
- **Camunda BPM** - Workflow Engine
- **JasperServer + DynamicReports** - گزارش‌دهی
- **Apache Kafka** - Messaging
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
- **Docker Compose** - Orchestration
- **Nginx** - Reverse Proxy & Load Balancer
- **Grafana + Prometheus** - Monitoring
- **Spring Boot Admin** - Application Monitoring

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

برای راهنمای کامل، به [مستندات راهنمای شروع](./Java-CRDB-ClickHouse-Kafka.wiki/Development/Getting-Started.md) مراجعه
کنید.

## 📚 مستندات

تمام مستندات پروژه در پوشه [Java-CRDB-ClickHouse-Kafka.wiki](./Java-CRDB-ClickHouse-Kafka.wiki/) قرار دارد:

### مستندات اصلی

- [📋 پروپوزال اولیه پروژه](./Java-CRDB-ClickHouse-Kafka.wiki/Proposal.md) - مستندات کامل پروپوزال و توجیهات

### مستندات فنی

- [🏗️ معماری سیستم](./Java-CRDB-ClickHouse-Kafka.wiki/Architecture/Home.md)
- [🔧 کامپوننت‌های Backend](./Java-CRDB-ClickHouse-Kafka.wiki/Backend/Home.md)
- [🎨 کامپوننت‌های Frontend](./Java-CRDB-ClickHouse-Kafka.wiki/Frontend/Home.md)
- [🗄️ دیتابیس‌ها](./Java-CRDB-ClickHouse-Kafka.wiki/Database/Home.md)
- [🔐 سیستم‌های امنیتی](./Java-CRDB-ClickHouse-Kafka.wiki/Security/Home.md)
- [📊 مانیتورینگ و لاگینگ](./Java-CRDB-ClickHouse-Kafka.wiki/Monitoring/Home.md)
- [🐳 Docker](./Java-CRDB-ClickHouse-Kafka.wiki/Docker/Home.md)
- [🔄 Kafka و Messaging](./Java-CRDB-ClickHouse-Kafka.wiki/Kafka/Home.md)
- [🌐 Nginx و Routing](./Java-CRDB-ClickHouse-Kafka.wiki/Nginx/Home.md)

### مستندات بیزینسی

- [📝 مستندات بیزینسی](./Java-CRDB-ClickHouse-Kafka.wiki/Business/Home.md)

### راهنماهای توسعه

- [🧪 تست و کیفیت](./Java-CRDB-ClickHouse-Kafka.wiki/Testing/Home.md)
- [💻 راهنماهای توسعه](./Java-CRDB-ClickHouse-Kafka.wiki/Development/Home.md)

## 🔄 CI/CD

پروژه از CI/CD pipeline برای:

- ✅ Automated testing
- ✅ Security scanning
- ✅ Docker image building
- ✅ Automated deployment
- ✅ Version management

برای جزئیات بیشتر، به [مستندات CI/CD](./Java-CRDB-ClickHouse-Kafka.wiki/CI-CD/Home.md) مراجعه کنید.

## 🔒 امنیت

- استفاده از Docker Secrets برای مدیریت اطلاعات حساس
- Multi-stage builds برای کاهش اندازه و افزایش امنیت imageها
- Non-root user در containers
- Security scanning با Trivy و Snyk

برای جزئیات بیشتر، به [مستندات امنیت Docker](./Java-CRDB-ClickHouse-Kafka.wiki/Docker/Docker-Security.md) مراجعه کنید.

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

برای جزئیات بیشتر، به [Git Workflow](./Java-CRDB-ClickHouse-Kafka.wiki/Development/Git-Workflow.md) مراجعه کنید.

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
