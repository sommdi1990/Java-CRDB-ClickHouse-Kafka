# خلاصه معماری Proxy و Registry

<div align="right">

[← بازگشت به صفحه اصلی](Home) | [راهنمای کامل Proxy](Kubernetes-Proxy-Setup)

</div>

---

## معماری کلی

```
┌─────────────────────────────────────────────────────────────┐
│                    سرور هلند (141.11.25.11)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  اینترنت آزاد و استیبل                                │   │
│  │  - Docker Registry (localhost:5000)                   │   │
│  │  - SOCKS5 Proxy (141.11.25.11:1080) ← سرویس‌دهنده    │   │
│  │  - دانلود مستقیم images از اینترنت                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ SSH (Port 111)
                          │ SOCKS5 (Port 1080)
                          │
┌─────────────────────────────────────────────────────────────┐
│              سرور ایران (Kubernetes Nodes)                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  proxychains → 141.11.25.11:1080                     │   │
│  │  SSH Tunnel → localhost:5000 (Registry)              │   │
│  │  - kubectl (با proxychains)                           │   │
│  │  - containerd (از Registry محلی)                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## نقش‌ها

### سرور هلند (141.11.25.11:111)

**نقش**: واسطه بین سرور ایران و اینترنت آزاد

**ویژگی‌ها**:

- ✅ اینترنت آزاد و استیبل
- ✅ SOCKS5 Proxy روی پورت 1080 (سرویس‌دهنده)
- ✅ Docker Registry روی localhost:5000
- ✅ دانلود مستقیم images از اینترنت (بدون proxychains)
- ✅ فقط پورت SSH (111) باز است

**کارها**:

1. راه‌اندازی Docker Registry
2. دانلود images از اینترنت
3. Push images به Registry محلی
4. سرویس‌دهی SOCKS5 proxy به سرور ایران

### سرور ایران (Kubernetes Nodes)

**نقش**: اجرای سرویس‌های Kubernetes

**ویژگی‌ها**:

- ✅ proxychains نصب است
- ✅ proxychains به 141.11.25.11:1080 وصل می‌شود
- ✅ SSH tunnel به Registry سرور هلند
- ✅ containerd از Registry محلی استفاده می‌کند

**کارها**:

1. راه‌اندازی SSH tunnel به Registry
2. تنظیم proxychains برای دسترسی به اینترنت
3. تنظیم containerd برای استفاده از Registry محلی
4. اجرای سرویس‌های Kubernetes

---

## جریان کار

### 1. دانلود Images (روی سرور هلند)

```bash
# روی سرور هلند
docker pull docker.io/calico/node:v3.26.1  # مستقیماً (اینترنت آزاد)
docker tag docker.io/calico/node:v3.26.1 127.0.0.1:5000/calico/node:v3.26.1
docker push 127.0.0.1:5000/calico/node:v3.26.1
```

### 2. دسترسی به Registry (از سرور ایران)

```bash
# روی سرور ایران
# SSH tunnel
ssh -f -N -L 5000:127.0.0.1:5000 -p 111 user@141.11.25.11

# استفاده از Registry
curl http://127.0.0.1:5000/v2/
```

### 3. دانلود Manifests (از سرور ایران)

```bash
# روی سرور ایران
# با استفاده از proxychains (از طریق سرور هلند)
proxychains curl -o tigera-operator.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml
```

---

## نکات مهم

1. ✅ **سرور هلند**: اینترنت آزاد دارد → دانلود مستقیم
2. ✅ **سرور ایران**: proxychains → 141.11.25.11:1080 → اینترنت
3. ✅ **Registry**: فقط روی localhost (از طریق SSH tunnel)
4. ✅ **هیچ پورت جدیدی روی سرور هلند باز نمی‌شود**

---

<div align="center">

[↑ بازگشت به بالا](#خلاصه-معماری-proxy-و-registry) | [← بازگشت به صفحه اصلی](Home) | [راهنمای کامل](Kubernetes-Proxy-Setup)

</div>

