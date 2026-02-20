# SSL/TLS

<div align="right">

[← بازگشت به Nginx](Nginx-Home) | [← صفحه اصلی](Nginx-Home)

</div>

---

## هدف

پیکربندی SSL/TLS در Nginx.

## Configuration

### Basic SSL

```nginx
server {
    listen 443 ssl;
    server_name example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

### SSL Optimization

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;
```

## Let's Encrypt

### Certbot

```bash
certbot --nginx -d example.com
```

### Auto-renewal

```bash
certbot renew --dry-run
```

## Best Practices

1. **TLS 1.2+**: استفاده از TLS 1.2 یا بالاتر
2. **Strong Ciphers**: استفاده از cipherهای قوی
3. **HSTS**: HTTP Strict Transport Security
4. **Certificate Renewal**: auto-renewal

## لینک‌های مفید

- [Nginx SSL/TLS Configuration](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Certbot Documentation](https://eff-certbot.readthedocs.io/)
- [SSL Labs SSL Test](https://www.ssllabs.com/ssltest/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [HSTS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)

---

<div align="center">

[↑ بازگشت به بالا](#ssltls) | [← بازگشت به Nginx](Nginx-Home) | [← صفحه اصلی](Nginx-Home)

</div>

