# Deployment

<div align="right">

[← بازگشت به CI-CD](Home) | [← صفحه اصلی](Home)

</div>

---

## هدف

استراتژی deployment برای production environment.

## استراتژی‌های Deployment

### 1. Blue-Green Deployment

- دو environment یکسان
- Switch بین environments
- Zero downtime
- Instant rollback

### 2. Canary Deployment

- Gradual rollout
- Traffic splitting
- Monitoring
- Automatic rollback

### 3. Rolling Deployment

- Incremental updates
- Zero downtime
- Health checks
- Automatic rollback

## Docker Deployment

### Production Dockerfile

```dockerfile
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Docker Compose Production

```yaml
version: '3.8'
services:
  app:
    image: myapp:${VERSION}
    restart: always
    environment:
      - SPRING_PROFILES_ACTIVE=production
```

## Kubernetes Deployment

### Deployment Strategy

برای محیط‌های **production** و **stage**، از **Kubernetes** استفاده می‌شود. برای جزئیات کامل،
به [راهنمای کامل Kubernetes](Kubernetes) مراجعه کنید.

### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 5
```

### Helm Charts

برای deployment در Kubernetes، از **Helm Charts** استفاده می‌شود:

```bash
# نصب با Helm
helm install myapp ./helm-charts/myapp \
  --namespace production \
  --set image.tag=v1.0.0 \
  --set replicas=3
```

### ArgoCD (GitOps)

برای GitOps deployment، از **ArgoCD** استفاده می‌شود:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/helm-charts
    path: myapp
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Health Checks

### Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Rollback Strategy

### Automatic Rollback

- Health check failures
- Error rate threshold
- Response time threshold

### Manual Rollback

- Version tagging
- Quick rollback commands
- Database migration rollback

## Best Practices

1. **Versioning**: استفاده از semantic versioning
2. **Health Checks**: health checks برای همه services
3. **Gradual Rollout**: gradual rollout برای production
4. **Monitoring**: monitoring در طول deployment

## لینک‌های مفید

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [راهنمای کامل Kubernetes در پروژه](Kubernetes)
- [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Helm Documentation](https://helm.sh/docs/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Canary Deployment](https://martinfowler.com/bliki/CanaryRelease.html)
- [Health Checks Best Practices](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

---

<div align="center">

[↑ بازگشت به بالا](#deployment) | [← بازگشت به CI-CD](Home) | [← صفحه اصلی](Home)

</div>

