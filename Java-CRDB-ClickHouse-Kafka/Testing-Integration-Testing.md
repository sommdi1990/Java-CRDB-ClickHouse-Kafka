# Integration Testing

<div align="right">

[← بازگشت به Testing](Testing-Home) | [← صفحه اصلی](Testing-Home)

</div>

---

## هدف

تست integration بین components.

## Types

### 1. API Integration

- REST API testing
- GraphQL testing
- Contract testing

### 2. Database Integration

- Repository testing
- Transaction testing
- Data consistency

### 3. Service Integration

- Microservices communication
- Event-driven testing
- Message queue testing

## Testcontainers

### Example

```java
@SpringBootTest
@Testcontainers
class OrderIntegrationTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");
    
    @Test
    void shouldCreateOrder() {
        // Integration test
    }
}
```

## Best Practices

1. **Test Real Integrations**: تست integrations واقعی
2. **Isolate Tests**: جداسازی tests
3. **Fast Execution**: تست‌های سریع
4. **Clean State**: state تمیز

## لینک‌های مفید

- [Testcontainers Documentation](https://www.testcontainers.org/)
- [Integration Testing Best Practices](https://www.guru99.com/integration-testing.html)
- [Contract Testing](https://docs.pact.io/)
- [API Testing](https://www.postman.com/api-testing/)

---

<div align="center">

[↑ بازگشت به بالا](#integration-testing) | [← بازگشت به Testing](Testing-Home) | [← صفحه اصلی](Testing-Home)

</div>

