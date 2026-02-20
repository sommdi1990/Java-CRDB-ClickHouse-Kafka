# Routing Configuration

<div align="right">

[← بازگشت به Nginx](Nginx-Home) | [← صفحه اصلی](Nginx-Home)

</div>

---

## هدف

Routing configuration در Nginx برای Docker Compose و Kubernetes Ingress.

## Configuration

### Basic Routing

```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend:8080;
    }
}
```

### API Routing

```nginx
location /api/ {
    proxy_pass http://api-gateway:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Frontend Routing

```nginx
location / {
    root /usr/share/nginx/html;
    try_files $uri $uri/ /index.html;
}
```

### Upstream Configuration

```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

### SSL/TLS Configuration

```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

## Kubernetes Ingress

برای Kubernetes، از Nginx Ingress Controller استفاده می‌شود:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: tls-secret
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: gateway-ui
                port:
                  number: 80
```

برای جزئیات بیشتر، به [راهنمای کامل Kubernetes](Kubernetes) مراجعه کنید.

## لینک‌های مفید

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html)
- [Nginx Configuration Guide](https://nginx.org/en/docs/http/ngx_http_core_module.html)
- [Nginx Load Balancing](https://nginx.org/en/docs/http/load_balancing.html)
- [Nginx SSL/TLS](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)

---

<div align="center">

[↑ بازگشت به بالا](#routing-configuration) | [← بازگشت به Nginx](Nginx-Home) | [← صفحه اصلی](Nginx-Home)

</div>
