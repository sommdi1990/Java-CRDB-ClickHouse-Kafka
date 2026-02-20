# کامپوننت‌های Backend

<div align="right">

[← بازگشت به صفحه اصلی](Home) | [پروپوزال](Proposal)

</div>

---

## فهرست مطالب

### Core Services

- [پروژه Infrastructure](Backend-Infrastructure)
- [پروژه WorkFlow](Backend-WorkFlow)
- [پروژه Report Manager](Backend-Report-Manager)
    - [Document Generator Service (Puppeteer)](Backend-Document-Generator-Service)
- [پروژه Accounting Service](Backend-Accounting-Service)

### Gateway Services

- [Gateway UI](Backend-Gateway-UI)
- [Gateway External](Backend-Gateway-External)
- [Gateway Input](Backend-Gateway-Input)

### Business Services

- [Business Services (DDD)](Backend-Business-Services)
- [GraphQL Service](Backend-GraphQL-Service)

### Infrastructure Services

- [Messaging Service](Backend-Messaging-Service)
- [Document Archive Service](Backend-Document-Archive-Service)
- [eSignature Service](Backend-eSignature-Service)
- [Document Versioning](Backend-Document-Versioning)
- [ClickHouse Manager](Backend-ClickHouse-Manager)
- [Schedule & Event Manager](Backend-Schedule-Event-Manager)
- [ماژول تست](Backend-Testing-Module)

---

## معرفی

این بخش شامل مستندات کامل تمام سرویس‌های backend است که با استفاده از **Spring Boot 4.0.1**، **Java 21**، **GraalVM
Native** و معماری **DDD** پیاده‌سازی شده‌اند.

## تکنولوژی‌های اصلی

- **Spring Boot 4.0.1**: Framework اصلی (با پشتیبانی از GraalVM Native)
- **Java 21**: زبان برنامه‌نویسی
- **Domain-Driven Design (DDD)**: معماری business services
- **Event-Driven Architecture**: ارتباط asynchronous بین سرویس‌ها
- **Kafka / Redpanda**: Event streaming platform

---

<div align="center">

[↑ بازگشت به بالا](#کامپوننتهای-backend)

</div>
