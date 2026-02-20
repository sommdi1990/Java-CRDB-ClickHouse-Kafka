# Docker Security

<div align="right">

[← بازگشت به Docker](Docker-Home) | [← صفحه اصلی](Docker-Home)

</div>

---

## Best Practices

### 1. Base Images

- استفاده از official images
- استفاده از slim/alpine variants
- **عدم استفاده از tag `latest`**
- مثال: `openjdk:17-jdk-slim` به جای `openjdk:latest`

### 2. Multi-stage Builds

```dockerfile
# Stage 1: Build
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 3. Secrets Management

- **Docker Secrets** (برای Docker Swarm)
- **Kubernetes Secrets** (برای K8s)
- **HashiCorp Vault** (برای enterprise)
- **عدم hardcode کردن secrets در Dockerfile**

### 4. Non-root User

- اجرای container با user غیر root
- استفاده از `USER` directive

### 5. Security Scanning

- **Trivy**: برای scan vulnerabilities
- **Snyk**: برای dependency scanning
- **Docker Bench Security**: برای security audit

### 6. Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 7. Read-only Filesystem

```dockerfile
RUN chmod -R 755 /app
# در docker-compose.yml
read_only: true
```

### 8. Network Security

- استفاده از internal networks
- محدود کردن exposed ports
- استفاده از reverse proxy (Nginx)

## لینک‌های مفید

- [Docker Documentation](https://docs.docker.com/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Bench Security](https://github.com/docker/docker-bench-security)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [Snyk Documentation](https://docs.snyk.io/)
- [OWASP Docker Security](https://owasp.org/www-project-docker-top-10/)

---

<div align="center">

[↑ بازگشت به بالا](#docker-security) | [← بازگشت به Docker](Docker-Home) | [← صفحه اصلی](Docker-Home)

</div>

