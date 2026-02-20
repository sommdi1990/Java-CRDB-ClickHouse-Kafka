# Gateway External

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

Gateway برای APIهای عمومی که به سیستم‌های خارجی ارائه می‌شود.

## مسئولیت‌ها

### 1. API Versioning

- مدیریت versionهای مختلف API
- Backward compatibility
- Deprecation strategy

### 2. Rate Limiting

- محدودیت تعداد requests
- Per API key
- Per IP address

### 3. API Key Management

- مدیریت API keys
- Key rotation
- Key expiration

### 4. Documentation

- OpenAPI/Swagger documentation
- API examples
- Error codes

## تکنولوژی‌ها

- **Spring Cloud Gateway**: API Gateway
- **API Key Authentication**: برای external clients
- **Rate Limiting**: Spring Cloud Gateway filters
- **OpenAPI**: Documentation

## API Endpoints

### Public APIs

- `GET /api/v1/public/data` - Public data
- `POST /api/v1/public/webhook` - Webhook endpoint
- `GET /api/v1/public/status` - System status

### Authenticated APIs

- `GET /api/v1/external/orders` - با API key
- `POST /api/v1/external/orders` - Create order
- `GET /api/v1/external/documents` - Get documents

## API Key Management

```java
@Entity
public class ApiKey {
    @Id
    private String key;
    private String clientId;
    private LocalDateTime expiresAt;
    private List<String> allowedEndpoints;
    private RateLimit rateLimit;
}
```

## Rate Limiting

- **Per API Key**: محدودیت برای هر key
- **Per IP**: محدودیت برای هر IP
- **Sliding Window**: الگوریتم rate limiting

## Security

- **API Key Authentication**: برای external clients
- **IP Whitelisting**: برای trusted clients
- **Request Signing**: برای sensitive operations

## Monitoring

- **API Usage**: tracking usage per client
- **Error Rates**: monitoring errors
- **Performance**: response times

## لینک‌های مفید

- [Spring Cloud Gateway Documentation](https://spring.io/projects/spring-cloud-gateway)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger Documentation](https://swagger.io/docs/)
- [API Versioning Best Practices](https://restfulapi.net/versioning/)
- [Rate Limiting Strategies](https://konghq.com/blog/how-to-design-a-scalable-rate-limiting-algorithm)
- [API Key Management](https://www.okta.com/identity-101/api-keys/)

---

<div align="center">

[↑ بازگشت به بالا](#gateway-external) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

