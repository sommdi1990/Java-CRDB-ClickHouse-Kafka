# پروژه Report Manager

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

مدیریت تمام گزارش‌ها شامل نامه‌ها، گزارش‌های هوش تجاری و مدیریتی، و گزارش‌های چاپی. همچنین تولید مستندات چند صفحه‌ای از
HTML با استفاده از Puppeteer.

## استراتژی گزارش‌دهی

### 1. JasperServer

- مدیریت و اجرای گزارش‌های استاندارد
- گزارش‌های از پیش تعریف شده
- Template management
- Report scheduling

### 2. DynamicReports

- تولید گزارش‌های کاملاً پویا
- گزارش‌های موقعیت‌محور
- ترکیب با Jasper reports (jrxml)

### 3. انواع گزارش‌ها

- **نامه‌ها**: گزارش‌های متنی و رسمی
- **گزارش‌های BI**: گزارش‌های تحلیلی و dashboardها
- **گزارش‌های مدیریتی**: گزارش‌های executive
- **گزارش‌های چاپی**: گزارش‌های فرمت‌بندی شده برای چاپ
- **گزارشات حسابداری**:
    - ترازنامه
    - سود و زیان
    - گردش حساب
    - دفتر کل
    - دفتر معین
    - دفتر روزنامه
    - تراز آزمایشی
    - گزارشات مالی دیگر
- **مستندات چند صفحه‌ای**: تولید PDF از HTML با Puppeteer

### 4. Document Generator Service (Puppeteer)

**هدف:**
تولید مستندات چند صفحه‌ای از HTML با استفاده از Puppeteer و تبدیل به PDF.

**قابلیت‌ها:**

- تبدیل HTML به PDF با کیفیت بالا
- پشتیبانی از مستندات چند صفحه‌ای
- پشتیبانی از CSS و JavaScript
- Template-based document generation
- Custom headers و footers
- Page numbering
- Table of contents
- Watermarks
- Metadata management
- Batch processing برای مستندات متعدد

**معماری:**

- **Microservice**: سرویس جداگانه در Report Manager
- **Dockerized**: اجرا در container جداگانه با Node.js
- **REST API**: API endpoints برای تولید مستندات
- **Queue-based**: پردازش async با Kafka

**تکنولوژی:**

- **Node.js**: Runtime environment
- **Puppeteer**: Headless Chrome برای HTML to PDF conversion
- **Express.js**: REST API framework
- **Docker**: Containerization
- **Kafka**: Message queue برای async processing

**استفاده:**

- تولید مستندات پروژه
- تولید گزارش‌های HTML-based
- تبدیل صفحات وب به PDF
- تولید فاکتورها و نامه‌های رسمی

## تکنولوژی‌ها

### Report Generation

- Spring Boot 4.0.1 (با پشتیبانی از GraalVM Native)
- JasperReports Server
- DynamicReports
- Apache POI (برای Excel reports)
- iText (برای PDF reports)

### Document Generator (Puppeteer)

- Node.js 18+
- Puppeteer (Headless Chrome)
- Express.js
- Docker
- Apache Kafka (برای async processing)

## API Endpoints

### Reports

- `GET /api/reports` - لیست گزارش‌ها
- `POST /api/reports` - ایجاد گزارش جدید
- `GET /api/reports/{id}/generate` - تولید گزارش
- `POST /api/reports/{id}/schedule` - زمان‌بندی گزارش

### Templates

- `GET /api/templates` - لیست templateها
- `POST /api/templates` - آپلود template جدید
- `GET /api/templates/{id}` - دریافت template

### Document Generator (Puppeteer Service)

- `POST /api/documents/generate` - تولید مستند PDF از HTML
- `POST /api/documents/generate-async` - تولید async مستند
- `GET /api/documents/{id}/status` - وضعیت تولید مستند
- `GET /api/documents/{id}/download` - دانلود مستند تولید شده
- `POST /api/documents/batch` - تولید batch مستندات
- `GET /api/documents/templates` - لیست HTML templates
- `POST /api/documents/templates` - آپلود HTML template جدید

## معماری Document Generator Service

```
┌─────────────────────────────────────────┐
│      Report Manager Service             │
│         (Spring Boot)                   │
└──────────────┬──────────────────────────┘
               │
               │ REST API
               │
┌──────────────▼──────────────────────────┐
│   Document Generator Service            │
│      (Node.js + Puppeteer)              │
│                                          │
│  ┌────────────────────────────────┐    │
│  │   Express.js REST API          │    │
│  └────────────────────────────────┘    │
│               │                         │
│  ┌────────────▼────────────┐           │
│  │  Puppeteer Service      │           │
│  │  (HTML → PDF)           │           │
│  └─────────────────────────┘           │
│               │                         │
│  ┌────────────▼────────────┐           │
│  │  Template Engine        │           │
│  │  (Handlebars/EJS)       │           │
│  └─────────────────────────┘           │
│               │                         │
│  ┌────────────▼────────────┐           │
│  │  Kafka Consumer         │           │
│  │  (Async Processing)     │           │
│  └─────────────────────────┘           │
└─────────────────────────────────────────┘
```

## Docker Configuration

Document Generator Service به صورت یک container جداگانه اجرا می‌شود:

```yaml
document-generator:
  build:
    context: ./backend/report-manager-service/document-generator
    dockerfile: Dockerfile
  container_name: document-generator
  ports:
    - "3001:3001"
  environment:
    - NODE_ENV=production
    - PORT=3001
    - KAFKA_BROKERS=kafka:9092
    - KAFKA_TOPIC=document-generation-requests
  volumes:
    - document-templates:/app/templates
    - document-output:/app/output
  depends_on:
    - kafka
  networks:
    - app-network
  healthcheck:
    test: [ "CMD", "curl", "-f", "http://localhost:3001/health" ]
    interval: 30s
    timeout: 10s
    retries: 3
```

## لینک‌های مفید

### Reporting Tools

- [JasperReports Documentation](https://community.jaspersoft.com/documentation)
- [JasperReports Server Documentation](https://community.jaspersoft.com/documentation/jasperreports-server)
- [DynamicReports Documentation](https://www.dynamicreports.org/documentation)
- [DynamicReports Examples](https://www.dynamicreports.org/examples)
- [Apache POI Documentation](https://poi.apache.org/)
- [iText Documentation](https://itextpdf.com/en/resources/guides/itext-7)
- [JasperReports Tutorial](https://www.tutorialspoint.com/jasper_reports/index.htm)
- [Report Design Best Practices](https://community.jaspersoft.com/wiki/report-design-best-practices)

### Puppeteer & Document Generation

- [Puppeteer Documentation](https://pptr.dev/)
- [Puppeteer API Reference](https://pptr.dev/api/)
- [Puppeteer GitHub](https://github.com/puppeteer/puppeteer)
- [HTML to PDF with Puppeteer](https://pptr.dev/guides/generating-pdfs)
- [Puppeteer Best Practices](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md)

---

<div align="center">

[↑ بازگشت به بالا](#پروژه-report-manager) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

