# راهنمای شروع

<div align="right">

[← بازگشت به Development](Development-Home) | [← صفحه اصلی](Development-Home)

</div>

---

## پیش‌نیازها

### نرم‌افزارهای مورد نیاز

- **Java 21+** - [دانلود](https://adoptium.net/) (برای Spring Boot 4.0.1 و GraalVM Native)
- **Node.js 18+** - [دانلود](https://nodejs.org/)
- **Maven 3.9+** - [دانلود](https://maven.apache.org/)
- **Docker & Docker Compose** - [دانلود](https://www.docker.com/) (برای محیط development)
- **Kubernetes** (برای محیط production و stage)
- **Git** - [دانلود](https://git-scm.com/)

### IDE پیشنهادی

- **IntelliJ IDEA** (برای Backend)
- **VS Code** یا **WebStorm** (برای Frontend)

## راه‌اندازی محیط توسعه

### 1. Clone پروژه

```bash
git clone https://github.com/your-org/Java-CRDB-ClickHouse-Kafka.git
cd Java-CRDB-ClickHouse-Kafka
```

### 2. راه‌اندازی Infrastructure

```bash
# راه‌اندازی دیتابیس‌ها و سرویس‌ها
docker-compose up -d

# بررسی وضعیت
docker-compose ps
```

### 3. راه‌اندازی Backend

```bash
cd backend

# Build همه پروژه‌ها
mvn clean install

# راه‌اندازی Infrastructure Service
cd infrastructure-service
mvn spring-boot:run

# راه‌اندازی سایر سرویس‌ها به صورت مشابه
```

### 4. راه‌اندازی Frontend

```bash
cd frontend

# نصب dependencies
npm install

# راه‌اندازی development server (با Vite)
npm run dev
```

## دسترسی به سرویس‌ها

- **Frontend**: http://localhost:3000
- **Backend APIs**: http://localhost:8080
- **Keycloak**: http://localhost:8080/auth
- **CockroachDB Admin**: http://localhost:8080/admin
- **ClickHouse Admin**: http://localhost:8123
- **Grafana**: http://localhost:3001
- **Spring Boot Admin**: http://localhost:9090

## اجرای تست‌ها

### Backend Tests

```bash
cd backend
mvn test
```

### Frontend Tests

```bash
cd frontend
npm test
```

### E2E Tests

```bash
cd frontend
npm run test:e2e
```

## ساختار پروژه

برای آشنایی با ساختار پروژه، به [README](../README.md) مراجعه کنید.

## مشکلات رایج

### مشکل: Port در حال استفاده است

```bash
# پیدا کردن process
lsof -i :8080

# Kill کردن process
kill -9 <PID>
```

### مشکل: Docker container نمی‌شود

```bash
# بررسی logs
docker-compose logs

# Restart کردن
docker-compose restart
```

## مراحل بعدی

- مطالعه [استانداردهای کدنویسی](./Coding-Standards.md)
- مطالعه [Git Workflow](./Git-Workflow.md)
- مطالعه [API Documentation](./API-Documentation.md)

---

<div align="center">

[↑ بازگشت به بالا](#راهنمای-شروع) | [← بازگشت به Development](Development-Home) | [← صفحه اصلی](Development-Home)

</div>

