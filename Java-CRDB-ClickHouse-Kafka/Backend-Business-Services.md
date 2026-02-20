# Business Services (DDD)

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

سرویس‌های دامنه‌محور که با استفاده از معماری DDD پیاده‌سازی شده‌اند.

## ساختار

هر دامنه به صورت یک microservice مستقل پیاده‌سازی می‌شود:

```
business-services/
├── accounting-service/      # دامنه حسابداری
├── inventory-service/       # دامنه موجودی (مثال)
├── sales-service/           # دامنه فروش (مثال)
└── shared-kernel/          # کد مشترک بین دامنه‌ها
```

## معماری DDD

### Domain Layer

- **Entities**: اشیاء با identity
- **Value Objects**: اشیاء بدون identity
- **Aggregates**: consistency boundaries
- **Domain Services**: منطق دامنه

### Application Layer

- **Application Services**: orchestration
- **Commands**: write operations
- **Queries**: read operations
- **DTOs**: data transfer objects

### Infrastructure Layer

- **Persistence**: JPA repositories
- **Messaging**: Kafka integration
- **External Services**: third-party integrations

### Presentation Layer

- **REST Controllers**: REST API
- **GraphQL Resolvers**: GraphQL API
- **DTOs**: response objects

## مثال: Accounting Service

### Domain Model

```java
@AggregateRoot
public class Document {
    private DocumentId id;
    private DocumentNumber number;
    private DocumentDate date;
    private List<DocumentItem> items;
    
    public void addItem(Account account, Money debit, Money credit) {
        // Business logic
    }
}
```

### Application Service

```java
@Service
public class DocumentApplicationService {
    public void createDocument(CreateDocumentCommand command) {
        Document document = new Document(command.getNumber(), command.getDate());
        command.getItems().forEach(item -> 
            document.addItem(item.getAccount(), item.getDebit(), item.getCredit())
        );
        documentRepository.save(document);
        eventPublisher.publish(new DocumentCreatedEvent(document.getId()));
    }
}
```

## Communication

### Events

- **Domain Events**: برای communication بین aggregates
- **Integration Events**: برای communication بین services
- **Event Sourcing**: در صورت نیاز

### API

- **REST API**: برای synchronous communication
- **GraphQL**: برای flexible queries
- **gRPC**: برای high-performance communication

## Best Practices

1. **One Aggregate per Transaction**: یک transaction فقط یک aggregate را تغییر دهد
2. **Event-Driven**: استفاده از events برای communication
3. **CQRS**: Separation of read and write models
4. **Bounded Context**: هر service یک bounded context است

## Integration

- **Event-Driven**: با سایر services
- **API Gateway**: برای external access
- **Shared Database**: با schema separation

## لینک‌های مفید

- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [DDD Patterns](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Aggregate Pattern](https://martinfowler.com/bliki/DDD_Aggregate.html)
- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)
- [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html)
- [Spring Data JPA Documentation](https://spring.io/projects/spring-data-jpa)
- [GraphQL Documentation](https://graphql.org/learn/)
- [gRPC Documentation](https://grpc.io/docs/)

---

<div align="center">

[↑ بازگشت به بالا](#business-services-ddd) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

