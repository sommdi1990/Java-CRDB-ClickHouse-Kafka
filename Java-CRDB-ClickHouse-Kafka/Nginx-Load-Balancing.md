# Load Balancing

<div align="right">

[← بازگشت به Nginx](Nginx-Home) | [← صفحه اصلی](Nginx-Home)

</div>

---

## هدف

Load balancing با Nginx.

## Load Balancing Methods

### 1. Round Robin

```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}
```

### 2. Least Connections

```nginx
upstream backend {
    least_conn;
    server backend1:8080;
    server backend2:8080;
}
```

### 3. IP Hash

```nginx
upstream backend {
    ip_hash;
    server backend1:8080;
    server backend2:8080;
}
```

## Health Checks

### Active Health Checks

```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;
    
    health_check;
}
```

## Session Persistence

### Sticky Sessions

```nginx
upstream backend {
    ip_hash;
    server backend1:8080;
    server backend2:8080;
}
```

## Kubernetes Load Balancing

در Kubernetes، load balancing به صورت خودکار توسط Service انجام می‌شود:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
  sessionAffinity: ClientIP  # برای sticky sessions
```

Nginx Ingress Controller نیز load balancing را در لایه HTTP انجام می‌دهد. برای جزئیات بیشتر،
به [راهنمای کامل Kubernetes](Kubernetes) مراجعه کنید.

## لینک‌های مفید

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Nginx Load Balancing](https://nginx.org/en/docs/http/load_balancing.html)
- [Nginx Upstream Module](https://nginx.org/en/docs/http/ngx_http_upstream_module.html)
- [Load Balancing Algorithms](https://www.nginx.com/resources/glossary/load-balancing/)
- [Session Persistence](https://www.nginx.com/products/nginx/load-balancing/#session-persistence)
- [Health Checks in Nginx](https://nginx.org/en/docs/http/ngx_http_upstream_hc_module.html)
- [Kubernetes Service Load Balancing](https://kubernetes.io/docs/concepts/services-networking/service/#load-balancing)
- [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/)

---

<div align="center">

[↑ بازگشت به بالا](#load-balancing) | [← بازگشت به Nginx](Nginx-Home) | [← صفحه اصلی](Nginx-Home)

</div>

