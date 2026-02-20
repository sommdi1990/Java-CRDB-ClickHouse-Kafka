# Document Generator Service (Puppeteer)

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← بازگشت به Report Manager](Backend-Report-Manager) | [← صفحه اصلی](Home)

</div>

---

## هدف

تولید مستندات چند صفحه‌ای با کیفیت بالا از HTML با استفاده از Puppeteer (Headless Chrome) و تبدیل به PDF. این سرویس به
عنوان بخشی از Report Manager Service طراحی شده و به صورت dockerized اجرا می‌شود.

## ویژگی‌ها

### قابلیت‌های اصلی

- ✅ **تبدیل HTML به PDF**: تبدیل HTML و CSS به PDF با کیفیت بالا
- ✅ **مستندات چند صفحه‌ای**: پشتیبانی کامل از صفحات متعدد
- ✅ **پشتیبانی از CSS و JavaScript**: رندر کامل CSS3 و JavaScript
- ✅ **Template-based**: تولید مستندات از templates قابل تنظیم
- ✅ **Headers و Footers**: Header و Footer سفارشی در هر صفحه
- ✅ **Page Numbering**: شماره‌گذاری خودکار صفحات
- ✅ **Table of Contents**: فهرست مطالب خودکار
- ✅ **Watermarks**: اضافه کردن واترمارک به صفحات
- ✅ **Metadata**: مدیریت metadata (title, author, subject, keywords)
- ✅ **Batch Processing**: پردازش دسته‌ای مستندات متعدد
- ✅ **Async Processing**: پردازش ناهمگام با استفاده از Kafka
- ✅ **Dockerized**: اجرا در container جداگانه

### قابلیت‌های پیشرفته

- ✅ **Custom Fonts**: پشتیبانی از فونت‌های فارسی و عربی
- ✅ **RTL Support**: پشتیبانی از راست به چپ (RTL)
- ✅ **Image Support**: پشتیبانی از تصاویر و نمودارها
- ✅ **Print Media Queries**: استفاده از CSS print media queries
- ✅ **Page Breaks**: کنترل break های صفحه
- ✅ **Margin Control**: کنترل حاشیه‌های صفحه
- ✅ **Landscape/Portrait**: پشتیبانی از جهت عمودی و افقی
- ✅ **Custom Paper Sizes**: سایزهای کاغذ سفارشی (A4, Letter, Legal, etc.)

## معماری

### معماری کلی

```
┌─────────────────────────────────────────┐
│      Report Manager Service             │
│         (Spring Boot)                   │
│                                         │
│  ┌──────────────────────────────┐      │
│  │  REST Controller             │      │
│  └──────────┬───────────────────┘      │
│             │                           │
│  ┌──────────▼───────────────────┐      │
│  │  Document Generator Client   │      │
│  └──────────┬───────────────────┘      │
└─────────────┼───────────────────────────┘
              │
              │ HTTP REST API / Kafka
              │
┌─────────────▼───────────────────────────┐
│   Document Generator Service            │
│      (Node.js + Express.js)             │
│                                         │
│  ┌──────────────────────────────┐      │
│  │  Express.js REST API         │      │
│  │  - POST /generate            │      │
│  │  - POST /generate-async      │      │
│  │  - GET /status/{id}          │      │
│  │  - GET /download/{id}        │      │
│  └──────────┬───────────────────┘      │
│             │                           │
│  ┌──────────▼───────────────────┐      │
│  │  Document Service            │      │
│  │  - Template Engine           │      │
│  │  - HTML Processing           │      │
│  └──────────┬───────────────────┘      │
│             │                           │
│  ┌──────────▼───────────────────┐      │
│  │  Puppeteer Service           │      │
│  │  - HTML → PDF Conversion     │      │
│  │  - Page Rendering            │      │
│  └──────────┬───────────────────┘      │
│             │                           │
│  ┌──────────▼───────────────────┐      │
│  │  Storage Service             │      │
│  │  - Template Storage          │      │
│  │  - Generated PDF Storage     │      │
│  └──────────────────────────────┘      │
│                                         │
│  ┌──────────────────────────────┐      │
│  │  Kafka Consumer              │      │
│  │  (Async Processing)          │      │
│  └──────────────────────────────┘      │
└─────────────────────────────────────────┘
```

### Flow Diagram

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ 1. POST /api/documents/generate
       │    { templateId, data, options }
       │
┌──────▼──────────────────────┐
│  Document Generator API     │
└──────┬──────────────────────┘
       │
       │ 2. Load Template
       │ 3. Render HTML with Data
       │
┌──────▼──────────────────────┐
│   Template Engine           │
│   (Handlebars/EJS)          │
└──────┬──────────────────────┘
       │
       │ 4. HTML Content
       │
┌──────▼──────────────────────┐
│   Puppeteer Service         │
│   - Launch Browser          │
│   - Load HTML               │
│   - Wait for Rendering      │
│   - Generate PDF            │
└──────┬──────────────────────┘
       │
       │ 5. PDF File
       │
┌──────▼──────────────────────┐
│   Storage Service           │
│   - Save PDF                │
│   - Return Download URL     │
└──────┬──────────────────────┘
       │
       │ 6. Return Response
       │    { documentId, downloadUrl, status }
       │
┌──────▼──────┐
│   Client    │
└─────────────┘
```

## تکنولوژی‌ها

### Core Technologies

- **Node.js 18+**: Runtime environment
- **Express.js**: REST API framework
- **Puppeteer**: Headless Chrome برای HTML to PDF conversion
- **Handlebars/EJS**: Template engine
- **Docker**: Containerization

### Supporting Libraries

- **kafkajs**: Kafka client برای async processing
- **multer**: File upload handling
- **express-validator**: Request validation
- **winston**: Logging
- **helmet**: Security middleware
- **cors**: CORS support

## API Endpoints

### Document Generation

#### POST /api/documents/generate

تولید همگام مستند PDF از HTML.

**Request Body:**

```json
{
  "templateId": "invoice-template",
  "data": {
    "invoiceNumber": "INV-2024-001",
    "customerName": "شرکت نمونه",
    "items": [
      {
        "name": "محصول ۱",
        "quantity": 2,
        "price": 100000
      }
    ],
    "total": 200000
  },
  "options": {
    "format": "A4",
    "orientation": "portrait",
    "margin": {
      "top": "20mm",
      "right": "15mm",
      "bottom": "20mm",
      "left": "15mm"
    },
    "displayHeaderFooter": true,
    "headerTemplate": "<div style='font-size:10px; text-align:center; width:100%;'>Header Content</div>",
    "footerTemplate": "<div style='font-size:10px; text-align:center; width:100%;'>Page <span class='pageNumber'></span> of <span class='totalPages'></span></div>",
    "printBackground": true,
    "metadata": {
      "title": "Invoice",
      "author": "System",
      "subject": "Invoice Document",
      "keywords": "invoice, billing"
    }
  }
}
```

**Response:**

```json
{
  "success": true,
  "documentId": "doc-12345",
  "downloadUrl": "/api/documents/doc-12345/download",
  "status": "completed",
  "generatedAt": "2024-01-15T10:30:00Z"
}
```

#### POST /api/documents/generate-async

تولید ناهمگام مستند PDF (از طریق Kafka).

**Request Body:** (مشابه generate)

**Response:**

```json
{
  "success": true,
  "documentId": "doc-12345",
  "status": "processing",
  "statusUrl": "/api/documents/doc-12345/status"
}
```

#### GET /api/documents/{documentId}/status

بررسی وضعیت تولید مستند.

**Response:**

```json
{
  "documentId": "doc-12345",
  "status": "completed",
  "progress": 100,
  "downloadUrl": "/api/documents/doc-12345/download",
  "error": null,
  "createdAt": "2024-01-15T10:30:00Z",
  "completedAt": "2024-01-15T10:30:05Z"
}
```

#### GET /api/documents/{documentId}/download

دانلود مستند تولید شده.

**Response:** PDF file (application/pdf)

#### POST /api/documents/generate-from-html

تولید PDF مستقیماً از HTML (بدون template).

**Request Body:**

```json
{
  "html": "<html><body><h1>Hello World</h1></body></html>",
  "options": {
    "format": "A4",
    "orientation": "portrait"
  }
}
```

#### POST /api/documents/batch

تولید batch مستندات متعدد.

**Request Body:**

```json
{
  "documents": [
    {
      "templateId": "invoice-template",
      "data": { ... },
      "options": { ... }
    },
    {
      "templateId": "report-template",
      "data": { ... },
      "options": { ... }
    }
  ]
}
```

**Response:**

```json
{
  "success": true,
  "batchId": "batch-12345",
  "documentIds": ["doc-1", "doc-2"],
  "statusUrl": "/api/documents/batch/batch-12345/status"
}
```

### Template Management

#### GET /api/documents/templates

لیست تمام templates.

#### POST /api/documents/templates

آپلود template جدید.

**Request:** multipart/form-data

- `file`: HTML template file
- `name`: Template name
- `description`: Template description
- `category`: Template category

#### GET /api/documents/templates/{templateId}

دریافت template.

#### PUT /api/documents/templates/{templateId}

به‌روزرسانی template.

#### DELETE /api/documents/templates/{templateId}

حذف template.

## Docker Configuration

### Dockerfile

```dockerfile
FROM node:18-alpine

# Install dependencies for Puppeteer
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    ttf-dejavu \
    ttf-liberation

# Set environment variables
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --production

# Copy application files
COPY . .

# Create directories
RUN mkdir -p /app/templates /app/output /app/logs

# Set permissions
RUN chown -R node:node /app

# Switch to non-root user
USER node

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD node healthcheck.js

# Start application
CMD ["node", "index.js"]
```

### docker-compose.yml

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
    - KAFKA_GROUP_ID=document-generator-group
    - TEMPLATE_DIR=/app/templates
    - OUTPUT_DIR=/app/output
    - LOG_LEVEL=info
    - MAX_CONCURRENT_GENERATIONS=5
    - PDF_TIMEOUT=30000
  volumes:
    - document-templates:/app/templates
    - document-output:/app/output
    - document-logs:/app/logs
  depends_on:
    - kafka
  networks:
    - app-network
  restart: unless-stopped
  healthcheck:
    test: ["CMD", "node", "healthcheck.js"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
```

### Volumes

```yaml
volumes:
  document-templates:
    driver: local
  document-output:
    driver: local
  document-logs:
    driver: local
```

## Configuration

### Environment Variables

```env
# Server Configuration
NODE_ENV=production
PORT=3001

# Kafka Configuration
KAFKA_BROKERS=kafka:9092
KAFKA_TOPIC=document-generation-requests
KAFKA_GROUP_ID=document-generator-group

# Directories
TEMPLATE_DIR=/app/templates
OUTPUT_DIR=/app/output
LOG_DIR=/app/logs

# Puppeteer Configuration
PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
PUPPETEER_HEADLESS=true

# Performance
MAX_CONCURRENT_GENERATIONS=5
PDF_TIMEOUT=30000
PDF_WAIT_FOR_SELECTOR_TIMEOUT=10000

# Storage
STORAGE_TYPE=local
# STORAGE_TYPE=s3
# AWS_S3_BUCKET=documents-bucket
# AWS_S3_REGION=us-east-1

# Logging
LOG_LEVEL=info
LOG_FORMAT=json

# Security
API_KEY=your-api-key-here
CORS_ORIGIN=http://localhost:8080
```

## Integration با Report Manager

### Java Client

```java
@Service
public class DocumentGeneratorClient {
    
    @Value("${document-generator.base-url:http://document-generator:3001}")
    private String baseUrl;
    
    @Value("${document-generator.api-key}")
    private String apiKey;
    
    private final RestTemplate restTemplate;
    
    public DocumentGenerationResponse generateDocument(
            String templateId, 
            Map<String, Object> data, 
            DocumentOptions options) {
        
        DocumentGenerationRequest request = new DocumentGenerationRequest();
        request.setTemplateId(templateId);
        request.setData(data);
        request.setOptions(options);
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("X-API-Key", apiKey);
        
        HttpEntity<DocumentGenerationRequest> entity = 
            new HttpEntity<>(request, headers);
        
        return restTemplate.postForObject(
            baseUrl + "/api/documents/generate",
            entity,
            DocumentGenerationResponse.class
        );
    }
}
```

### Frontend Integration

```typescript
// DocumentGeneratorService.ts
export class DocumentGeneratorService {
  private baseUrl = 'http://document-generator:3001/api';
  
  async generateDocument(
    templateId: string,
    data: any,
    options?: DocumentOptions
  ): Promise<DocumentGenerationResponse> {
    const response = await fetch(`${this.baseUrl}/documents/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': process.env.REACT_APP_DOCUMENT_GENERATOR_API_KEY
      },
      body: JSON.stringify({
        templateId,
        data,
        options
      })
    });
    
    return response.json();
  }
  
  async downloadDocument(documentId: string): Promise<Blob> {
    const response = await fetch(
      `${this.baseUrl}/documents/${documentId}/download`
    );
    return response.blob();
  }
}
```

## Best Practices

### Template Design

1. **استفاده از Print Media Queries**
   ```css
   @media print {
     .no-print {
       display: none;
     }
     
     .page-break {
       page-break-after: always;
     }
   }
   ```

2. **بهینه‌سازی تصاویر**
    - استفاده از فرمت‌های مناسب (PNG, JPG)
    - فشرده‌سازی تصاویر
    - استفاده از lazy loading

3. **فونت‌های فارسی**
    - استفاده از فونت‌های بهینه‌شده برای PDF
    - پیش‌بارگذاری فونت‌ها

4. **RTL Support**
   ```css
   body {
     direction: rtl;
     text-align: right;
   }
   ```

### Performance Optimization

1. **Concurrent Processing**: محدود کردن تعداد concurrent generations
2. **Caching**: کش کردن templates و rendered HTML
3. **Resource Management**: مدیریت حافظه و browser instances
4. **Timeout Handling**: تنظیم timeout مناسب برای operations

### Security

1. **Input Validation**: اعتبارسنجی ورودی‌ها
2. **Template Sandboxing**: محدود کردن دسترسی templates
3. **API Authentication**: استفاده از API keys
4. **Rate Limiting**: محدود کردن تعداد درخواست‌ها

## Monitoring & Logging

### Metrics

- تعداد مستندات تولید شده
- زمان متوسط تولید
- نرخ خطا
- استفاده از حافظه
- تعداد concurrent generations

### Logging

```javascript
logger.info('Document generation started', {
  documentId: 'doc-12345',
  templateId: 'invoice-template',
  userId: 'user-123'
});

logger.error('Document generation failed', {
  documentId: 'doc-12345',
  error: error.message,
  stack: error.stack
});
```

## Troubleshooting

### مشکلات رایج

1. **Chromium Crash**
    - بررسی memory limits
    - بررسی timeout settings
    - بررسی concurrent limits

2. **Font Rendering Issues**
    - نصب فونت‌های لازم در container
    - تنظیم font paths

3. **RTL Issues**
    - بررسی CSS direction
    - بررسی text-align settings

4. **Performance Issues**
    - کاهش concurrent generations
    - بهینه‌سازی templates
    - استفاده از caching

## لینک‌های مفید

- [Puppeteer Documentation](https://pptr.dev/)
- [Puppeteer API Reference](https://pptr.dev/api/)
- [Puppeteer GitHub](https://github.com/puppeteer/puppeteer)
- [HTML to PDF with Puppeteer](https://pptr.dev/guides/generating-pdfs)
- [Puppeteer Best Practices](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md)
- [Express.js Documentation](https://expressjs.com/)
- [Handlebars Documentation](https://handlebarsjs.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

<div align="center">

[↑ بازگشت به بالا](#document-generator-service-puppeteer) | [← بازگشت به Backend](Backend-Home) | [← بازگشت به Report Manager](Backend-Report-Manager) | [← صفحه اصلی](Home)

</div>

