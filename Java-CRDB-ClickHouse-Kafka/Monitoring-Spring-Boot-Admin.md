# Spring Boot Admin

<div align="right">

[← بازگشت به Monitoring](Monitoring-Home) | [← صفحه اصلی](Monitoring-Home)

</div>

---

## هدف

مانیتورینگ و مدیریت Spring Boot applications.

## قابلیت‌ها

### 1. Application Monitoring

- Health status
- Metrics
- Logs
- Threads

### 2. Management

- JMX beans
- Environment variables
- Configuration properties
- Log level management

### 3. Notifications

- Email notifications
- Slack notifications
- Custom notifications

## Setup

### Server Configuration

```yaml
spring:
  boot:
    admin:
      server:
        url: http://localhost:9090
```

### Client Configuration

```yaml
spring:
  boot:
    admin:
      client:
        url: http://localhost:9090
        instance:
          name: ${spring.application.name}
```

## Features

### Health Monitoring

- Application health
- Database health
- Disk space
- Memory usage

### Metrics

- JVM metrics
- HTTP metrics
- Custom metrics
- Performance metrics

### Logs

- Real-time logs
- Log level management
- Log filtering
- Log download

## Security

- **Authentication**: Basic auth یا OAuth
- **Authorization**: Role-based access
- **HTTPS**: SSL/TLS encryption

## لینک‌های مفید

- [Spring Boot Admin Documentation](https://codecentric.github.io/spring-boot-admin/current/)
- [Spring Boot Admin GitHub](https://github.com/codecentric/spring-boot-admin)
- [Spring Boot Actuator Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)
- [JMX Documentation](https://docs.oracle.com/javase/tutorial/jmx/)
- [Application Monitoring Best Practices](https://www.datadoghq.com/knowledge-center/monitoring/)

---

<div align="center">

[↑ بازگشت به بالا](#spring-boot-admin) | [← بازگشت به Monitoring](Monitoring-Home) | [← صفحه اصلی](Monitoring-Home)

</div>

