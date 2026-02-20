# ماژول تست

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

ماژول تست برای تست‌های واحد، یکپارچگی و E2E.

## انواع تست

### 1. Unit Tests

- تست واحد برای classes و methods
- Mock dependencies
- Fast execution
- High coverage

### 2. Integration Tests

- تست integration بین components
- Database tests
- API tests
- Testcontainers

### 3. E2E Tests

- تست end-to-end scenarios
- User workflows
- System integration

## تکنولوژی‌ها

### Testing Frameworks

- **JUnit 5**: Testing framework
- **Mockito**: Mocking framework
- **AssertJ**: Fluent assertions
- **Testcontainers**: Integration testing

### Test Utilities

- **WireMock**: HTTP mocking
- **Testcontainers**: Docker-based testing
- **Spring Boot Test**: Spring testing support

## Unit Testing

### Example

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock
    private OrderRepository orderRepository;
    
    @InjectMocks
    private OrderService orderService;
    
    @Test
    void shouldCreateOrder() {
        // Given
        CreateOrderCommand command = new CreateOrderCommand(...);
        Order expectedOrder = new Order(...);
        when(orderRepository.save(any())).thenReturn(expectedOrder);
        
        // When
        Order result = orderService.createOrder(command);
        
        // Then
        assertThat(result).isNotNull();
        verify(orderRepository).save(any());
    }
}
```

## Integration Testing

### Testcontainers Example

```java
@SpringBootTest
@Testcontainers
class OrderIntegrationTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");
    
    @Container
    static GenericContainer<?> kafka = new GenericContainer<>("confluentinc/cp-kafka:latest");
    
    @Test
    void shouldCreateAndPublishOrder() {
        // Integration test
    }
}
```

## E2E Testing

### Example

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
class OrderE2ETest {
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void shouldCreateOrderEndToEnd() throws Exception {
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(orderJson))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").exists());
    }
}
```

## Test Coverage

- **Code Coverage**: حداقل 80%
- **Branch Coverage**: حداقل 75%
- **Mutation Testing**: برای کیفیت تست‌ها

## Best Practices

1. **AAA Pattern**: Arrange, Act, Assert
2. **Test Isolation**: هر تست مستقل باشد
3. **Fast Tests**: تست‌ها باید سریع باشند
4. **Clear Names**: نام‌های واضح برای تست‌ها
5. **Mock External Dependencies**: Mock کردن dependencies خارجی

## لینک‌های مفید

- [JUnit 5 Documentation](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)
- [AssertJ Documentation](https://assertj.github.io/doc/)
- [Testcontainers Documentation](https://www.testcontainers.org/)
- [WireMock Documentation](http://wiremock.org/docs/)
- [Spring Boot Test Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing)
- [Testing Best Practices](https://martinfowler.com/articles/practical-test-pyramid.html)

---

<div align="center">

[↑ بازگشت به بالا](#ماژول-تست) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

