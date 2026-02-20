# Unit Testing

<div align="right">

[← بازگشت به Testing](Testing-Home) | [← صفحه اصلی](Testing-Home)

</div>

---

## هدف

تست‌های واحد برای classes و methods.

## Best Practices

### 1. AAA Pattern

- **Arrange**: Setup test data
- **Act**: Execute method
- **Assert**: Verify results

### 2. Test Isolation

- Independent tests
- No shared state
- Clean setup/teardown

### 3. Naming Convention

- Descriptive names
- Should/When/Then format
- Clear intent

## Example

```java
@Test
void shouldCalculateTotalPrice_WhenItemsAdded() {
    // Arrange
    Order order = new Order();
    Product product = new Product("Item", new Money(100));
    
    // Act
    order.addItem(product, new Quantity(2));
    
    // Assert
    assertThat(order.getTotal()).isEqualTo(new Money(200));
}
```

## Coverage

- **Line Coverage**: حداقل 80%
- **Branch Coverage**: حداقل 75%
- **Mutation Testing**: برای کیفیت

## لینک‌های مفید

- [JUnit 5 Documentation](https://junit.org/junit5/docs/current/user-guide/)
- [AAA Pattern](https://medium.com/@pjbgf/title-testing-code-ocd-and-the-aaa-pattern-d4533dcc5e89)
- [Test Isolation](https://martinfowler.com/bliki/UnitTest.html)
- [Test Naming Conventions](https://dzone.com/articles/7-popular-unit-test-naming)

---

<div align="center">

[↑ بازگشت به بالا](#unit-testing) | [← بازگشت به Testing](Testing-Home) | [← صفحه اصلی](Testing-Home)

</div>

