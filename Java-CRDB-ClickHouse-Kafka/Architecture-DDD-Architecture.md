# معماری DDD (Domain-Driven Design)

<div align="right">

[← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

---

## معرفی

این پروژه از معماری Domain-Driven Design (DDD) برای business services استفاده می‌کند.

## مفاهیم اصلی DDD

### 1. Domain

منطقه‌ای از دانش یا فعالیت که در آن منطق کسب‌وکار وجود دارد.

### 2. Bounded Context

مرزهای یک مدل دامنه که در آن مفاهیم و اصطلاحات معنای مشخصی دارند.

### 3. Ubiquitous Language

زبان مشترک بین توسعه‌دهندگان و domain experts.

## الگوهای DDD

### Aggregate

مجموعه‌ای از entities و value objects که به عنوان یک واحد consistency boundary عمل می‌کند.

```java
@AggregateRoot
public class Order {
    private OrderId id;
    private List<OrderItem> items;
    private OrderStatus status;
    
    public void addItem(Product product, Quantity quantity) {
        // Business logic
    }
}
```

### Entity

شیء با identity که در طول زمان تغییر می‌کند.

```java
@Entity
public class Account {
    @Id
    private AccountId id;
    private AccountCode code;
    private AccountName name;
    // ...
}
```

### Value Object

شیء بدون identity که با attributes آن تعریف می‌شود.

```java
@ValueObject
public class Money {
    private BigDecimal amount;
    private Currency currency;
    
    public Money add(Money other) {
        // Immutable operation
    }
}
```

### Repository

Abstraction برای persistence که collection-like interface ارائه می‌دهد.

```java
public interface OrderRepository {
    Order findById(OrderId id);
    void save(Order order);
    List<Order> findByStatus(OrderStatus status);
}
```

### Domain Service

منطق دامنه که به یک entity خاص تعلق ندارد.

```java
@Service
public class PricingService {
    public Money calculatePrice(Order order) {
        // Complex pricing logic
    }
}
```

### Application Service

Orchestration منطق دامنه و coordination بین aggregates.

```java
@Service
public class OrderApplicationService {
    public void createOrder(CreateOrderCommand command) {
        // Orchestrate domain logic
    }
}
```

## ساختار پروژه DDD

```
domain-service/
├── domain/
│   ├── entities/
│   ├── value-objects/
│   ├── aggregates/
│   ├── repositories/
│   └── services/
├── application/
│   ├── services/
│   ├── commands/
│   ├── queries/
│   ├── dto/
│   └── mappers/
├── infrastructure/
│   ├── persistence/
│   │   ├── jpa/
│   │   └── repositories/
│   ├── messaging/
│   └── external/
└── presentation/
    ├── rest/
    ├── graphql/
    └── dto/
```

## مثال: Accounting Domain

### Aggregate Root

```java
@AggregateRoot
public class Document {
    private DocumentId id;
    private DocumentNumber number;
    private DocumentDate date;
    private List<DocumentItem> items;
    
    public void addItem(Account account, Money debit, Money credit) {
        // Business rules
        validateBalance();
        items.add(new DocumentItem(account, debit, credit));
    }
    
    private void validateBalance() {
        Money totalDebit = items.stream()
            .map(DocumentItem::getDebit)
            .reduce(Money.ZERO, Money::add);
        Money totalCredit = items.stream()
            .map(DocumentItem::getCredit)
            .reduce(Money.ZERO, Money::add);
        
        if (!totalDebit.equals(totalCredit)) {
            throw new InvalidDocumentException("Debit and Credit must be equal");
        }
    }
}
```

### Value Objects

```java
@ValueObject
public class DocumentNumber {
    private final String value;
    
    public DocumentNumber(String value) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Document number cannot be empty");
        }
        this.value = value;
    }
}
```

### Repository

```java
public interface DocumentRepository {
    Document findById(DocumentId id);
    void save(Document document);
    List<Document> findByDateRange(LocalDate from, LocalDate to);
}
```

## Best Practices

1. **Keep Aggregates Small**: Aggregates باید کوچک باشند
2. **Protect Invariants**: Business rules باید در aggregate حفظ شوند
3. **Use Value Objects**: برای concepts که identity ندارند
4. **Repository Pattern**: برای abstraction persistence
5. **Domain Events**: برای communication بین aggregates

## Integration با سایر سرویس‌ها

- **Event-Driven**: استفاده از events برای communication
- **CQRS**: Separation of read and write models
- **API Gateway**: برای aggregation

## لینک‌های مفید

- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [DDD Book by Eric Evans](https://www.domainlanguage.com/ddd/)
- [DDD Patterns](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Aggregate Pattern](https://martinfowler.com/bliki/DDD_Aggregate.html)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)
- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)

---

<div align="center">

[↑ بازگشت به بالا](#معماری-ddd-domain-driven-design) | [← بازگشت به Architecture](Architecture-Home) | [← صفحه اصلی](Home)

</div>

