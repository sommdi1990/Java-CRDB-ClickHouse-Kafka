# API Documentation

<div align="right">

[← بازگشت به Development](Development-Home) | [← صفحه اصلی](Development-Home)

</div>

---

## هدف

مستندسازی APIها.

## Tools

### OpenAPI/Swagger

- API specification
- Interactive documentation
- Code generation

### SpringDoc

- Spring Boot integration
- Automatic documentation
- Swagger UI

## Documentation Standards

### API Endpoints

- Method و path
- Parameters
- Request/Response
- Examples

### Error Codes

- Error codes
- Error messages
- Handling strategies

## Example

### OpenAPI Spec

```yaml
paths:
  /api/orders:
    post:
      summary: Create order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
      responses:
        '201':
          description: Order created
```

## Best Practices

1. **Keep Updated**: به‌روز نگه داشتن
2. **Examples**: مثال‌های واضح
3. **Error Handling**: مستندسازی errors
4. **Versioning**: version management

## لینک‌های مفید

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger Documentation](https://swagger.io/docs/)
- [SpringDoc Documentation](https://springdoc.org/)
- [API Documentation Best Practices](https://swagger.io/resources/articles/adopting-an-api-first-approach/)
- [REST API Design](https://restfulapi.net/)

---

<div align="center">

[↑ بازگشت به بالا](#api-documentation) | [← بازگشت به Development](Development-Home) | [← صفحه اصلی](Development-Home)

</div>

