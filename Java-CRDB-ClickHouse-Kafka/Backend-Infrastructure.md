# پروژه Infrastructure

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

پروژه زیرساخت که امنیت و مدیریت کاربران و زیرساخت پروژه را بر عهده دارد.

## مسئولیت‌ها

### 1. امنیت

- Integration با Keycloak
- مدیریت JWT tokens
- Security policies
- Rate limiting

### 2. مدیریت کاربران

- Synchronization با Keycloak
- User profile management
- User preferences

### 3. زیرساخت مشترک

- Logging configuration
- Configuration management
- Health checks
- Metrics collection

## تکنولوژی‌ها

- Spring Boot 4.0.1 (با پشتیبانی از GraalVM Native)
- Spring Security
- Spring Cloud Config
- Micrometer (برای metrics)

## API Endpoints

### Security

- `POST /api/auth/login`
- `POST /api/auth/logout`
- `POST /api/auth/refresh`

### User Management

- `GET /api/users/{id}`
- `PUT /api/users/{id}`
- `GET /api/users/me`

## لینک‌های مفید

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Spring Security Documentation](https://spring.io/projects/spring-security)
- [Spring Cloud Config Documentation](https://spring.io/projects/spring-cloud-config)
- [Micrometer Documentation](https://micrometer.io/docs)
- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [JWT.io](https://jwt.io/) - JWT Token Debugger
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [OpenID Connect Specification](https://openid.net/connect/)

---

<div align="center">

[↑ بازگشت به بالا](#پروژه-infrastructure) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

