# Keycloak

<div align="right">

[← بازگشت به Security](Security-Home) | [← صفحه اصلی](Security-Home)

</div>

---

## معرفی

Keycloak یک راه‌حل open-source برای Identity and Access Management است.

## ویژگی‌ها

- **Single Sign-On (SSO)**
- **OAuth 2.0 / OpenID Connect**
- **SAML 2.0**
- **Social Login** (Google, Facebook, etc.)
- **User Federation** (LDAP, Active Directory)
- **Two-Factor Authentication (2FA)**

## Integration با Spring Boot

### Dependency

```xml
<dependency>
    <groupId>org.keycloak</groupId>
    <artifactId>keycloak-spring-boot-starter</artifactId>
</dependency>
```

### Configuration

```yaml
keycloak:
  realm: your-realm
  auth-server-url: http://localhost:8080/auth
  resource: your-client
  credentials:
    secret: your-secret
```

## جایگزین‌های پیشنهادی

### 1. Auth0

- **نوع**: Cloud-based (SaaS)
- **مزایا**: Managed service، پشتیبانی عالی
- **معایب**: هزینه بالا برای enterprise

### 2. Okta

- **نوع**: Enterprise-grade
- **مزایا**: Enterprise features، امنیت بالا
- **معایب**: هزینه بسیار بالا

### 3. Ory Hydra

- **نوع**: Open-source، Cloud-native
- **مزایا**: Lightweight، Kubernetes-native
- **معایب**: نیاز به setup بیشتر

### 4. Zitadel

- **نوع**: Open-source، Modern
- **مزایا**: UI مدرن، قابلیت‌های پیشرفته
- **معایب**: جامعه کوچک‌تر

## توصیه

- **Keycloak**: برای پروژه‌های open-source و self-hosted
- **Auth0**: اگر بودجه دارید و نیاز به managed service
- **Okta**: برای سازمان‌های بزرگ enterprise

## Setup

```bash
docker run -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest \
  start-dev
```

## Integration با سیستم

- Synchronization با Infrastructure Service
- User management integration
- Role-based access control (RBAC)

## لینک‌های مفید

- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [Keycloak Guides](https://www.keycloak.org/guides)
- [Keycloak Server Administration](https://www.keycloak.org/docs/latest/server_admin/)
- [Keycloak Securing Apps](https://www.keycloak.org/docs/latest/securing_apps/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [OpenID Connect Specification](https://openid.net/connect/)
- [SAML 2.0 Specification](https://www.oasis-open.org/standards#samlv2.0)
- [JWT.io](https://jwt.io/) - JWT Token Debugger

---

<div align="center">

[↑ بازگشت به بالا](#keycloak) | [← بازگشت به Security](Security-Home) | [← صفحه اصلی](Security-Home)

</div>

