# Multi-stage Builds

<div align="right">

[← بازگشت به Docker](Docker-Home) | [← صفحه اصلی](Docker-Home)

</div>

---

## هدف

کاهش اندازه Docker images و افزایش امنیت با multi-stage builds.

## ساختار

### Stage 1: Build

- Maven build
- Compile code
- Run tests
- Package application

### Stage 2: Runtime

- Copy only necessary files
- Use minimal base image
- No build tools

## مثال

### Dockerfile

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
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## مزایا

1. **Smaller Images**: کاهش اندازه image
2. **Security**: عدم وجود build tools در production
3. **Faster Deployment**: imageهای کوچک‌تر
4. **Better Caching**: بهبود layer caching

## Best Practices

1. **Use .dockerignore**: حذف فایل‌های غیرضروری
2. **Layer Ordering**: بهینه‌سازی ترتیب layers
3. **Minimal Base Images**: استفاده از alpine images
4. **Non-root User**: اجرا با user غیر root

## لینک‌های مفید

- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [.dockerignore Documentation](https://docs.docker.com/engine/reference/builder/#dockerignore-file)
- [Alpine Linux](https://alpinelinux.org/) - Minimal base images
- [Distroless Images](https://github.com/GoogleContainerTools/distroless)

---

<div align="center">

[↑ بازگشت به بالا](#multi-stage-builds) | [← بازگشت به Docker](Docker-Home) | [← صفحه اصلی](Docker-Home)

</div>

