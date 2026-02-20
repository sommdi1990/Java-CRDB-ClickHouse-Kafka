# مدیریت دسترسی‌ها

<div align="right">

[← بازگشت به Security](Security-Home) | [← صفحه اصلی](Security-Home)

</div>

---

## هدف

مدیریت دسترسی‌ها و permissions در سیستم.

## قابلیت‌ها

### 1. Role-Based Access Control (RBAC)

- تعریف نقش‌ها
- تخصیص نقش به کاربران
- سلسله مراتب نقش‌ها

### 2. Permission Management

- تعریف permissions
- تخصیص permission به نقش‌ها
- Resource-based permissions

### 3. Access Policies

- Policy definition
- Policy enforcement
- Policy evaluation

## ساختار دسترسی

### Roles

- **Super Admin**: دسترسی کامل
- **Admin**: دسترسی مدیریتی
- **Manager**: دسترسی مدیریتی محدود
- **User**: دسترسی پایه
- **Guest**: دسترسی محدود

### Permissions

```java
public enum Permission {
    USER_READ,
    USER_WRITE,
    USER_DELETE,
    DOCUMENT_READ,
    DOCUMENT_WRITE,
    DOCUMENT_DELETE,
    REPORT_READ,
    REPORT_WRITE,
    // ...
}
```

## Implementation

### Spring Security

```java
@PreAuthorize("hasRole('ADMIN') or hasPermission(#id, 'USER', 'READ')")
public User getUser(Long id) {
    return userRepository.findById(id);
}
```

### Method Security

```java
@Secured("ROLE_ADMIN")
public void deleteUser(Long id) {
    userRepository.deleteById(id);
}
```

## API Security

### Endpoint Protection

```java
@RestController
@RequestMapping("/api/admin")
@PreAuthorize("hasRole('ADMIN')")
public class AdminController {
    // Admin-only endpoints
}
```

## Best Practices

1. **Principle of Least Privilege**: حداقل دسترسی لازم
2. **Role Hierarchy**: سلسله مراتب نقش‌ها
3. **Permission Granularity**: دسترسی‌های دقیق
4. **Audit Logging**: ثبت تمام دسترسی‌ها

## لینک‌های مفید

- [Spring Security Documentation](https://spring.io/projects/spring-security)
- [Spring Security Method Security](https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html)
- [RBAC Pattern](https://en.wikipedia.org/wiki/Role-based_access_control)
- [Principle of Least Privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)
- [Access Control Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

---

<div align="center">

[↑ بازگشت به بالا](#مدیریت-دسترسیها) | [← بازگشت به Security](Security-Home) | [← صفحه اصلی](Security-Home)

</div>

