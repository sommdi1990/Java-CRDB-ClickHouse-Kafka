# پروژه WorkFlow

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

سیستم مدیریت روندهای کاری (Workflow) و نقش‌های تجاری (Business Role Management System).

## قابلیت‌ها

### 1. Workflow Engine

- پشتیبانی از BPMN 2.0
- تعریف و اجرای workflowها
- مدیریت state workflowها
- History و audit trail

### 2. Business Role Management

- تعریف نقش‌های تجاری
- تخصیص نقش‌ها به کاربران
- مدیریت سلسله مراتب نقش‌ها
- Dynamic role assignment

### 3. Business Rules Engine

- تعریف قواعد تجاری
- اجرای قواعد در workflowها
- Versioning قواعد

## تکنولوژی‌ها

- Spring Boot 4.0.1 (با پشتیبانی از GraalVM Native)
- Camunda BPM (پیشنهادی)
- Drools (برای Business Rules)
- Spring State Machine (جایگزین سبک‌تر)

## API Endpoints

### Workflow

- `POST /api/workflows` - ایجاد workflow جدید
- `GET /api/workflows/{id}` - دریافت workflow
- `POST /api/workflows/{id}/start` - شروع workflow
- `GET /api/workflows/{id}/tasks` - دریافت tasks

### Business Roles

- `GET /api/business-roles` - لیست نقش‌ها
- `POST /api/business-roles` - ایجاد نقش جدید
- `PUT /api/business-roles/{id}` - به‌روزرسانی نقش
- `POST /api/business-roles/{id}/assign` - تخصیص نقش به کاربر

## لینک‌های مفید

- [Camunda BPM Documentation](https://docs.camunda.org/)
- [Camunda BPMN 2.0 Guide](https://docs.camunda.org/manual/latest/reference/bpmn20/)
- [Drools Documentation](https://www.drools.org/learn/documentation.html)
- [Drools Business Rules](https://www.drools.org/learn/businessRules.html)
- [Spring State Machine Documentation](https://docs.spring.io/spring-statemachine/docs/current/reference/html/)
- [BPMN 2.0 Specification](https://www.omg.org/spec/BPMN/2.0/)
- [Workflow Patterns](https://www.workflowpatterns.com/)

---

<div align="center">

[↑ بازگشت به بالا](#پروژه-workflow) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

