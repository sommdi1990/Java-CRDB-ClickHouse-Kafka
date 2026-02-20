# Gateway UI

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

Gateway برای APIهای مخصوص رابط کاربری با کمترین business logic.

## مسئولیت‌ها

### 1. API Aggregation

- Aggregation از چندین microservices
- کاهش تعداد requests از client
- بهبود performance

### 2. Response Transformation

- تبدیل response format
- Filtering unnecessary data
- Data enrichment

### 3. Caching

- Caching responses
- کاهش load روی backend services
- بهبود response time

### 4. Authentication & Authorization

- JWT token validation
- Role-based access control
- User context management

## تکنولوژی‌ها

- **Spring Cloud Gateway**: API Gateway framework
- **Spring Security**: امنیت
- **Redis**: Caching
- **Circuit Breaker**: Resilience

## API Endpoints

### Aggregated Endpoints

- `GET /api/ui/dashboard` - Dashboard data aggregation
- `GET /api/ui/user-profile` - User profile with permissions
- `GET /api/ui/notifications` - User notifications

### Proxy Endpoints

- `GET /api/ui/orders` - Proxy to Order Service
- `GET /api/ui/documents` - Proxy to Document Service
- `GET /api/ui/reports` - Proxy to Report Service

## Configuration

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-service
          uri: http://order-service:8080
          predicates:
            - Path=/api/ui/orders/**
        - id: document-service
          uri: http://document-service:8080
          predicates:
            - Path=/api/ui/documents/**
```

## Caching Strategy

- **Cache-Control**: HTTP headers
- **Redis Cache**: برای frequently accessed data
- **TTL Management**: مدیریت expiration

## Security

- **JWT Validation**: در gateway level
- **Rate Limiting**: per user/IP
- **CORS**: Cross-Origin Resource Sharing

## لینک‌های مفید

- [Spring Cloud Gateway Documentation](https://spring.io/projects/spring-cloud-gateway)
- [Spring Cloud Gateway Reference](https://docs.spring.io/spring-cloud-gateway/docs/current/reference/html/)
- [Spring Security Documentation](https://spring.io/projects/spring-security)
- [Redis Documentation](https://redis.io/docs/)
- [Resilience4j Documentation](https://resilience4j.readme.io/) - Circuit Breaker
- [API Gateway Pattern](https://microservices.io/patterns/apigateway.html)
- [CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

---

<div align="center">

[↑ بازگشت به بالا](#gateway-ui) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

