# Docker Compose

<div align="right">

[← بازگشت به Docker](Docker-Home) | [← صفحه اصلی](Docker-Home)

</div>

---

## هدف

Orchestration تمام services با Docker Compose.

## ساختار

### Services

- **Backend Services**: تمام Spring Boot services
- **Frontend**: React application
- **Databases**: CockroachDB, ClickHouse, Redis
- **Message Queue**: Kafka
- **Monitoring**: Grafana, Prometheus
- **Security**: Keycloak
- **Gateway**: Nginx
- **Document Management**: Mayan EDMS (به عنوان بخشی از کانتینر یکپارچه)
- **Document Generator**: Puppeteer-based service برای تولید PDF از HTML

## Configuration

### docker-compose.yml

```yaml
version: '3.8'

services:
  cockroachdb:
    image: cockroachdb/cockroach:latest
    ports:
      - "26257:26257"
    environment:
      - COCKROACH_DATABASE=app_db
  
  clickhouse:
    image: clickhouse/clickhouse-server:latest
    ports:
      - "8123:8123"
      - "9000:9000"
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  
  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
  
  keycloak:
    image: quay.io/keycloak/keycloak:latest
    ports:
      - "8080:8080"
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
  
  # Mayan EDMS - Document Management System
  mayan-edms-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: mayan
      POSTGRES_USER: mayan
      POSTGRES_PASSWORD: ${MAYAN_EDMS_DB_PASSWORD}
    volumes:
      - mayan-edms-db-data:/var/lib/postgresql/data
    networks:
      - app-network
  
  mayan-edms-redis:
    image: redis:alpine
    volumes:
      - mayan-edms-redis-data:/data
    networks:
      - app-network
  
  mayan-edms:
    image: mayanedms/mayanedms:latest
    depends_on:
      - mayan-edms-db
      - mayan-edms-redis
    ports:
      - "8000:8000"
    environment:
      MAYAN_DATABASE_ENGINE: django.db.backends.postgresql
      MAYAN_DATABASE_NAME: mayan
      MAYAN_DATABASE_USER: mayan
      MAYAN_DATABASE_PASSWORD: ${MAYAN_EDMS_DB_PASSWORD}
      MAYAN_DATABASE_HOST: mayan-edms-db
      MAYAN_DATABASE_PORT: 5432
      MAYAN_REDIS_HOST: mayan-edms-redis
      MAYAN_REDIS_PORT: 6379
      MAYAN_SECRET_KEY: ${MAYAN_EDMS_SECRET_KEY}
      MAYAN_ALLOWED_HOSTS: "*"
    volumes:
      - mayan-edms-media:/var/lib/mayan
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  # Document Generator Service (Puppeteer)
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
      - API_KEY=${DOCUMENT_GENERATOR_API_KEY}
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

## Networking

### Network Configuration

```yaml
networks:
  app-network:
    driver: bridge
```

## Volumes

### Data Persistence

```yaml
volumes:
  cockroachdb-data:
  clickhouse-data:
  redis-data:
  kafka-data:
  mayan-edms-db-data:
  mayan-edms-redis-data:
  mayan-edms-media:
  document-templates:
  document-output:
  document-logs:
```

## Environment Variables

### .env File

```env
POSTGRES_PASSWORD=password
REDIS_PASSWORD=password
KEYCLOAK_ADMIN_PASSWORD=admin
MAYAN_EDMS_DB_PASSWORD=mayan_password
MAYAN_EDMS_SECRET_KEY=your-secret-key-here
DOCUMENT_GENERATOR_API_KEY=your-document-generator-api-key-here
```

## Commands

### Start Services

```bash
docker-compose up -d
```

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f [service-name]
```

### Scale Services

```bash
docker-compose up -d --scale service-name=3
```

## Mayan EDMS Integration

### Configuration

Mayan EDMS به عنوان بخشی از کانتینر یکپارچه Docker اجرا می‌شود و از طریق REST API به سرویس‌های Java و Frontend متصل
می‌شود.

### Access

- **Web UI**: http://localhost:8000
- **REST API**: http://localhost:8000/api/
- **API Documentation**: http://localhost:8000/api/docs/

### Initial Setup

پس از اولین اجرا، باید یک superuser ایجاد کنید:

```bash
docker-compose exec mayan-edms mayan-edms.py createsuperuser
```

### API Authentication

برای استفاده از API، باید یک API token ایجاد کنید:

```bash
# از طریق Web UI: Settings > API > REST API > Tokens
# یا از طریق command line
```

### Integration با Java Services

Java services می‌توانند از طریق REST API به Mayan EDMS متصل شوند:

```java
@Configuration
public class MayanEDMSConfig {
    @Value("${mayan-edms.base-url:http://mayan-edms:8000}")
    private String baseUrl;
    
    @Value("${mayan-edms.api-token}")
    private String apiToken;
    
    @Bean
    public RestTemplate mayanEDMSRestTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getInterceptors().add((request, body, execution) -> {
            request.getHeaders().add("Authorization", "Token " + apiToken);
            return execution.execute(request, body);
        });
        return restTemplate;
    }
}
```

### Integration با Frontend

Frontend می‌تواند مستقیماً به Mayan EDMS API متصل شود یا از طریق Backend Gateway:

```typescript
// Option 1: Direct API call (if CORS enabled)
const response = await fetch('http://mayan-edms:8000/api/documents/', {
  headers: {
    'Authorization': `Token ${apiToken}`
  }
});

// Option 2: Through Backend Gateway (recommended)
const response = await fetch('/api/documents/', {
  headers: {
    'Authorization': `Bearer ${jwtToken}`
  }
});
```

## Document Generator Service

### Configuration

Document Generator Service به صورت یک container جداگانه با Node.js و Puppeteer اجرا می‌شود و مسئول تبدیل HTML به PDF
است.

### Access

- **REST API**: http://localhost:3001/api
- **Health Check**: http://localhost:3001/health

### Environment Variables

```env
DOCUMENT_GENERATOR_API_KEY=your-api-key-here
```

### Integration با Java Services

Java services می‌توانند از طریق REST API به Document Generator متصل شوند:

```java
@Configuration
public class DocumentGeneratorConfig {
    @Value("${document-generator.base-url:http://document-generator:3001}")
    private String baseUrl;
    
    @Value("${document-generator.api-key}")
    private String apiKey;
    
    @Bean
    public RestTemplate documentGeneratorRestTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.getInterceptors().add((request, body, execution) -> {
            request.getHeaders().add("X-API-Key", apiKey);
            return execution.execute(request, body);
        });
        return restTemplate;
    }
}
```

### Integration با Frontend

Frontend می‌تواند از طریق Backend Gateway به Document Generator دسترسی داشته باشد:

```typescript
// Through Backend Gateway (recommended)
const response = await fetch('/api/documents/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${jwtToken}`
  },
  body: JSON.stringify({
    templateId: 'invoice-template',
    data: { ... },
    options: { ... }
  })
});
```

برای جزئیات بیشتر، به [مستندات Document Generator Service](Backend-Document-Generator-Service) مراجعه کنید.

## لینک‌های مفید

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Networking](https://docs.docker.com/network/)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Mayan EDMS

- [Mayan EDMS Official Documentation](https://docs.mayan-edms.com/)
- [Mayan EDMS Installation Guide](https://docs.mayan-edms.com/topics/installation.html)
- [Mayan EDMS Docker Installation](https://docs.mayan-edms.com/topics/installation_docker.html)
- [Mayan EDMS Docker Image](https://hub.docker.com/r/mayanedms/mayanedms)
- [Mayan EDMS REST API](https://docs.mayan-edms.com/topics/api.html)
- [Mayan EDMS GitHub Repository](https://github.com/mayan-edms/mayan-edms)
- [Mayan EDMS Configuration](https://docs.mayan-edms.com/topics/configuration.html)

---

<div align="center">

[↑ بازگشت به بالا](#docker-compose) | [← بازگشت به Docker](Docker-Home) | [← صفحه اصلی](Docker-Home)

</div>

