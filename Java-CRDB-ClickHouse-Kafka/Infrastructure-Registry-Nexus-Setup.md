# راه‌اندازی Registry و Nexus – alefba2.ir

## Rocky Linux 10 – Revision 3 (Registry & Nexus Infrastructure)

> **Owner:** Soroush  
> **Scope:** Private Docker Registry و Nexus Repository Manager برای Kubernetes و Development

---

## 1. خلاصه اجرایی

این مستندات راهنمای کامل راه‌اندازی و پیکربندی:

- **Docker Registry** با احراز هویت و UI
- **Nexus Repository Manager** برای k8s-manifests و helm-charts
- **Nexus Repository Manager** برای Development (Git, Jenkins, Maven, K8s)
- مدیریت دامنه‌ها با **CDN ابرآروان**
- **HTTPS** با **certbot**
- **Nginx** برای reverse proxy و routing

---

## 2. معماری کلی

### 2.1. جداسازی دامنه‌ها

| دامنه          | پروژه               | کاربرد                                                         |
|----------------|---------------------|----------------------------------------------------------------|
| `*.alefba4.ir` | Kubernetes Services | سرویس‌های Kubernetes (Jira, Confluence, Grafana, Jenkins, Git) |
| `*.alefba2.ir` | Registry & Nexus    | رجیستری و نکسوس (rr, reg, mn)                                  |

### 2.2. سرورها و IPها

| Hostname | IP             | Role                                  | OS             |
|----------|----------------|---------------------------------------|----------------|
| registry | 192.168.10.160 | Docker Registry + Registry UI + Nexus | Rocky Linux 10 |

---

## 3. Phase 1 – نصب و پیکربندی سرور Registry

### 3.1. آماده‌سازی سرور (192.168.10.160)

**نکته:** تمام دستورات زیر روی سرور `registry` (192.168.10.160) اجرا می‌شوند.

```bash
# SSH به سرور
ssh root@192.168.10.160

# به‌روزرسانی سیستم
dnf update -y

# نصب ابزارهای پایه
dnf install -y curl wget vim git net-tools

# تنظیم hostname
hostnamectl set-hostname registry
echo "192.168.10.160 registry" >> /etc/hosts

# غیرفعال کردن swap
swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# تنظیمات kernel
cat >> /etc/sysctl.conf <<EOF
vm.max_map_count=262144
fs.inotify.max_user_instances=8192
fs.inotify.max_user_watches=524288
net.ipv4.ip_forward=1
EOF

sysctl -p

# فعال کردن IP forwarding
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p
```

---

## 4. Phase 2 – نصب و پیکربندی Docker Registry

### 4.1. نصب containerd و Docker Registry

```bash
# نصب containerd
dnf install -y containerd

# راه‌اندازی containerd
systemctl enable containerd
systemctl start containerd

# ایجاد دایرکتوری برای registry data
mkdir -p /opt/registry/data
chmod 755 /opt/registry/data

# ایجاد فایل htpasswd برای احراز هویت
# نصب htpasswd
dnf install -y httpd-tools

# ایجاد کاربر و رمز عبور
# Username: admin
# Password: <pass>
htpasswd -Bbn admin '<pass>' > /opt/registry/auth/htpasswd
chmod 644 /opt/registry/auth/htpasswd

# Pull کردن registry image
containerd pull docker.io/library/registry:2

# ایجاد فایل config برای registry
cat > /opt/registry/config.yml <<EOF
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
auth:
  htpasswd:
    realm: Registry Realm
    path: /auth/htpasswd
EOF

# راه‌اندازی registry با containerd
cat > /etc/systemd/system/docker-registry.service <<EOF
[Unit]
Description=Docker Registry
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/nerdctl run \\
  --name registry \\
  --restart unless-stopped \\
  -p 5000:5000 \\
  -v /opt/registry/data:/var/lib/registry \\
  -v /opt/registry/auth:/auth \\
  -v /opt/registry/config.yml:/etc/docker/registry/config.yml \\
  -e REGISTRY_AUTH=htpasswd \\
  -e REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm \\
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \\
  docker.io/library/registry:2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable docker-registry.service
systemctl start docker-registry.service
systemctl status docker-registry.service
```

### 4.2. تست Registry

```bash
# تست دسترسی به registry
curl http://localhost:5000/v2/

# تست احراز هویت
curl -u admin:<pass> http://localhost:5000/v2/
```

---

## 5. Phase 3 – نصب و پیکربندی Registry UI (joxit/docker-registry-ui)

### 5.1. راه‌اندازی Registry UI

```bash
# Pull کردن image
nerdctl pull rr.alefba2.ir/joxit/docker-registry-ui:2.6.0

# راه‌اندازی Registry UI
cat > /etc/systemd/system/registry-ui.service <<EOF
[Unit]
Description=Docker Registry UI
After=network.target docker-registry.service
Requires=docker-registry.service

[Service]
Type=simple
ExecStart=/usr/bin/nerdctl run \\
  --name registry-ui \\
  --restart unless-stopped \\
  -p 8080:80 \\
  -e REGISTRY_URL=http://127.0.0.1:5000 \\
  -e REGISTRY_TITLE="Docker Registry UI" \\
  -e REGISTRY_SECURE=false \\
  rr.alefba2.ir/joxit/docker-registry-ui:2.6.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable registry-ui.service
systemctl start registry-ui.service
systemctl status registry-ui.service
```

**نکته:** اگر image در registry موجود نیست، ابتدا باید آن را pull و push کنید:

```bash
# Pull از Docker Hub (یا از جای دیگر)
nerdctl pull joxit/docker-registry-ui:2.6.0

# Tag برای registry محلی
nerdctl tag joxit/docker-registry-ui:2.6.0 rr.alefba2.ir/joxit/docker-registry-ui:2.6.0

# Login به registry
nerdctl login rr.alefba2.ir -u admin -p '<pass>'

# Push به registry
nerdctl push rr.alefba2.ir/joxit/docker-registry-ui:2.6.0
```

---

## 6. Phase 4 – نصب و پیکربندی Nexus Repository Manager

### 6.1. نصب Nexus

```bash
# ایجاد کاربر nexus
useradd -r -s /bin/false nexus

# ایجاد دایرکتوری‌های مورد نیاز
mkdir -p /opt/nexus
mkdir -p /opt/sonatype-work

# دانلود Nexus (نیاز به دسترسی اینترنت یا استفاده از proxy)
cd /tmp
wget https://download.sonatype.com/nexus/3/nexus-3.68.0-02-unix.tar.gz

# Extract
tar -xzf nexus-3.68.0-02-unix.tar.gz -C /opt/nexus --strip-components=1

# تغییر مالکیت
chown -R nexus:nexus /opt/nexus
chown -R nexus:nexus /opt/sonatype-work

# تنظیمات JVM
sed -i 's/-Xms2703m/-Xms1024m/g' /opt/nexus/bin/nexus.vmoptions
sed -i 's/-Xmx2703m/-Xmx2048m/g' /opt/nexus/bin/nexus.vmoptions

# ایجاد systemd service
cat > /etc/systemd/system/nexus.service <<EOF
[Unit]
Description=Nexus Repository Manager
After=network.target

[Service]
Type=forking
LimitNOFILE=65536
ExecStart=/opt/nexus/bin/nexus start
ExecStop=/opt/nexus/bin/nexus stop
User=nexus
Restart=on-abort
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable nexus.service
systemctl start nexus.service

# بررسی لاگ‌ها
tail -f /opt/sonatype-work/nexus3/log/nexus.log
```

**نکته:** پس از راه‌اندازی، admin password در فایل زیر است:

```bash
cat /opt/sonatype-work/nexus3/admin.password
```

### 6.2. پیکربندی اولیه Nexus

1. دسترسی به UI: `http://192.168.10.160:8081`
2. Login با admin و password از فایل بالا
3. تغییر password
4. ایجاد Repositoryها:

#### 6.2.1. ایجاد Repository برای k8s-manifests

1. **Settings** → **Repositories** → **Create repository**
2. **raw (hosted)**
3. تنظیمات:
    - **Name:** `k8s-manifests`
    - **Storage:** `/opt/sonatype-work/nexus3/storage/k8s-manifests`
    - **Blob store:** `default`
4. **Create repository**

#### 6.2.2. ایجاد Repository برای helm-charts

1. **Settings** → **Repositories** → **Create repository**
2. **helm (hosted)**
3. تنظیمات:
    - **Name:** `helm-charts`
    - **Storage:** `/opt/sonatype-work/nexus3/storage/helm-charts`
    - **Blob store:** `default`
4. **Create repository**

### 6.3. ایجاد کاربر برای دسترسی

1. **Settings** → **Users** → **Create user**
2. ایجاد کاربر `k8s-reader`:
    - **User ID:** `k8s-reader`
    - **First Name:** `K8s`
    - **Last Name:** `Reader`
    - **Email:** `k8s-reader@alefba2.ir`
    - **Password:** (رمز عبور مورد نظر)
    - **Roles:** `nx-repository-view-*-*-read`, `nx-repository-view-*-*-browse`
3. ایجاد Token:
    - **Settings** → **Users** → **k8s-reader** → **User Token** → **Generate Token**
    - ذخیره Token برای استفاده در Helm

---

## 7. Phase 5 – نصب و پیکربندی Nginx

### 7.1. نصب Nginx

```bash
# نصب nginx
dnf install -y nginx

# راه‌اندازی nginx
systemctl enable nginx
systemctl start nginx
```

### 7.2. پیکربندی Nginx برای دامنه‌ها

```bash
# ایجاد فایل پیکربندی برای rr.alefba2.ir (Registry)
cat > /etc/nginx/conf.d/rr.alefba2.ir.conf <<EOF
server {
    listen 80;
    server_name rr.alefba2.ir;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # برای Docker Registry
        client_max_body_size 0;
        proxy_request_buffering off;
    }
}
EOF

# ایجاد فایل پیکربندی برای reg.alefba2.ir (Registry UI)
cat > /etc/nginx/conf.d/reg.alefba2.ir.conf <<EOF
server {
    listen 80;
    server_name reg.alefba2.ir;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# ایجاد فایل پیکربندی برای mn.alefba2.ir (Nexus)
cat > /etc/nginx/conf.d/mn.alefba2.ir.conf <<EOF
server {
    listen 80;
    server_name mn.alefba2.ir;

    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # برای Nexus
        client_max_body_size 0;
        proxy_request_buffering off;
    }
}
EOF

# تست پیکربندی
nginx -t

# راه‌اندازی مجدد nginx
systemctl restart nginx
```

---

## 8. Phase 6 – تنظیمات CDN ابرآروان

### 8.1. پیکربندی DNS در ابرآروان

1. ورود به پنل ابرآروان
2. اضافه کردن DNS Records:

| Type | Name | Value          | TTL |
|------|------|----------------|-----|
| A    | rr   | 192.168.10.160 | 300 |
| A    | reg  | 192.168.10.160 | 300 |
| A    | mn   | 192.168.10.160 | 300 |

3. فعال کردن CDN برای هر دامنه (اختیاری)

---

## 9. Phase 7 – نصب و پیکربندی certbot برای HTTPS

### 9.1. نصب certbot

```bash
# نصب certbot و nginx plugin
dnf install -y certbot python3-certbot-nginx

# دریافت certificate برای دامنه‌ها
certbot --nginx -d rr.alefba2.ir --non-interactive --agree-tos --email admin@alefba2.ir
certbot --nginx -d reg.alefba2.ir --non-interactive --agree-tos --email admin@alefba2.ir
certbot --nginx -d mn.alefba2.ir --non-interactive --agree-tos --email admin@alefba2.ir

# تست auto-renewal
certbot renew --dry-run

# فعال کردن auto-renewal
systemctl enable certbot.timer
systemctl start certbot.timer
```

### 9.2. به‌روزرسانی پیکربندی Nginx برای HTTPS

certbot به صورت خودکار فایل‌های nginx را به‌روزرسانی می‌کند. در صورت نیاز می‌توانید به صورت دستی تنظیم کنید:

```bash
# بررسی فایل‌های ایجاد شده
ls -la /etc/nginx/conf.d/
```

---

## 10. Phase 8 – استفاده از Registry

### 10.1. Pull Image از Registry

```bash
# Login به registry
nerdctl login rr.alefba2.ir -u admin -p '<pass>'

# Pull image
nerdctl pull rr.alefba2.ir/joxit/docker-registry-ui:2.6.0

# یا با containerd
sudo ctr images pull \
  --user 'admin:<pass>' \
  rr.alefba2.ir/joxit/docker-registry-ui:2.6.0
```

### 10.2. Push Image به Registry

```bash
# Tag image
nerdctl tag nginx:latest rr.alefba2.ir/nginx:latest

# Push image
nerdctl push rr.alefba2.ir/nginx:latest
```

### 10.3. استفاده در Kubernetes

برای استفاده در Kubernetes، باید containerd را روی هر node پیکربندی کنید:

```bash
# روی هر Kubernetes node
sudo mkdir -p /etc/containerd/certs.d/rr.alefba2.ir

cat > /etc/containerd/certs.d/rr.alefba2.ir/hosts.toml <<EOF
server = "https://rr.alefba2.ir"

[host."https://rr.alefba2.ir"]
  capabilities = ["pull", "resolve"]
  skip_verify = true
EOF

# Restart containerd
sudo systemctl restart containerd
```

---

## 11. Phase 9 – استفاده از Nexus

### 11.1. Push Manifest به Nexus

```bash
# Push deployment.yaml
curl -u admin:PASS \
  --upload-file deployment.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/deployments/app.yaml
```

### 11.2. Pull Manifest از Nexus

```bash
# Pull و apply
kubectl apply -f https://mn.alefba2.ir/repository/k8s-manifests/deployments/app.yaml
```

### 11.3. Push Helm Chart به Nexus

```bash
# Package chart
helm package ./my-chart

# ایجاد index
helm repo index . --url https://mn.alefba2.ir/repository/helm-charts/

# Push chart
curl -u k8s-reader:Token -T ./my-chart-0.1.0.tgz https://mn.alefba2.ir/repository/helm-charts/

# Push index
curl -u k8s-reader:Token -T ./index.yaml https://mn.alefba2.ir/repository/helm-charts/
```

### 11.4. استفاده از Helm Chart در Kubernetes

```bash
# اضافه کردن repo
helm repo add my-nexus https://mn.alefba2.ir/repository/helm-charts/ \
  --username k8s-reader \
  --password <Token>

# Update repo
helm repo update

# Install chart
helm install myapp my-nexus/my-chart
```

---

## 12. Phase 10 – Nexus برای Development

### 12.1. ایجاد Repositoryهای Development

در Nexus UI:

1. **Settings** → **Repositories** → **Create repository**

#### 12.1.1. Maven Repository

- **maven2 (hosted)**
- **Name:** `maven-releases`
- **Version policy:** `Release`
- **Layout policy:** `Strict`

- **maven2 (hosted)**
- **Name:** `maven-snapshots`
- **Version policy:** `Snapshot`
- **Layout policy:** `Permissive`

#### 12.1.2. npm Repository

- **npm (hosted)**
- **Name:** `npm-private`

#### 12.1.3. Docker Repository

- **docker (hosted)**
- **Name:** `docker-private`
- **HTTP Port:** `8082`
- **Enable Docker V1 API:** `true`

### 12.2. پیکربندی Maven

```xml
<!-- settings.xml -->
<settings>
  <servers>
    <server>
      <id>nexus</id>
      <username>admin</username>
      <password>PASSWORD</password>
    </server>
  </servers>
  
  <mirrors>
    <mirror>
      <id>nexus</id>
      <mirrorOf>*</mirrorOf>
      <url>https://mn.alefba2.ir/repository/maven-public/</url>
    </mirror>
  </mirrors>
</settings>
```

---

## 13. Phase 11 – پیکربندی Kubernetes برای استفاده از Registry و Nexus

### 13.1. پیکربندی containerd روی Kubernetes Nodes

**روی هر Kubernetes node (k8s-cp-01, k8s-worker-01, k8s-worker-02, k8s-collab-01):**

```bash
# ایجاد دایرکتوری برای registry config
sudo mkdir -p /etc/containerd/certs.d/rr.alefba2.ir

# ایجاد فایل hosts.toml
cat > /etc/containerd/certs.d/rr.alefba2.ir/hosts.toml <<EOF
server = "https://rr.alefba2.ir"

[host."https://rr.alefba2.ir"]
  capabilities = ["pull", "resolve"]
  skip_verify = true
  [host."https://rr.alefba2.ir".auth]
    username = "admin"
    password = "<pass>"
EOF

# Restart containerd
sudo systemctl restart containerd
```

### 13.2. ایجاد Secret برای Registry در Kubernetes

```bash
# ایجاد secret
kubectl create secret docker-registry registry-secret \
  --docker-server=rr.alefba2.ir \
  --docker-username=admin \
  --docker-password='<pass>' \
  --docker-email=admin@alefba2.ir \
  --namespace=default

# استفاده در Pod
# spec:
#   imagePullSecrets:
#   - name: registry-secret
```

---

## 14. امنیت

### 14.1. Firewall

```bash
# نصب و فعال کردن firewalld
dnf install -y firewalld
systemctl enable firewalld
systemctl start firewalld

# باز کردن پورت‌های مورد نیاز
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --add-port=5000/tcp
firewall-cmd --permanent --add-port=8080/tcp
firewall-cmd --permanent --add-port=8081/tcp
firewall-cmd --reload
```

### 14.2. SELinux

```bash
# بررسی وضعیت SELinux
getenforce

# اگر Enforcing است، تنظیمات لازم را انجام دهید
# یا به صورت موقت:
# setenforce 0
```

---

## 15. Backup و Monitoring

### 15.1. Backup Registry

```bash
# Backup registry data
tar -czf /backup/registry-$(date +%Y%m%d).tar.gz /opt/registry/data

# Backup Nexus
tar -czf /backup/nexus-$(date +%Y%m%d).tar.gz /opt/sonatype-work
```

### 15.2. Monitoring

- مانیتورینگ disk space
- مانیتورینگ registry و nexus logs
- مانیتورینگ nginx logs

---

## 16. Troubleshooting

### 16.1. مشکلات رایج

#### Registry در دسترس نیست

```bash
# بررسی وضعیت service
systemctl status docker-registry.service

# بررسی لاگ‌ها
journalctl -u docker-registry.service -f

# بررسی پورت
netstat -tlnp | grep 5000
```

#### Nexus راه‌اندازی نمی‌شود

```bash
# بررسی لاگ‌ها
tail -f /opt/sonatype-work/nexus3/log/nexus.log

# بررسی memory
free -h

# بررسی disk space
df -h
```

#### مشکل SSL/TLS

```bash
# بررسی certificate
certbot certificates

# Renew certificate
certbot renew
```

---

## 17. خلاصه دستورات مهم

### 17.1. Registry

```bash
# Pull image
sudo ctr images pull --user 'admin:<pass>' rr.alefba2.ir/joxit/docker-registry-ui:2.6.0

# Run container
sudo nerdctl run -d \
  --name registry-ui \
  --restart unless-stopped \
  -p 8080:80 \
  -e REGISTRY_URL=http://127.0.0.1:5000 \
  rr.alefba2.ir/joxit/docker-registry-ui:2.6.0
```

### 17.2. Nexus

```bash
# Push manifest
curl -u admin:PASS --upload-file deployment.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/deployments/app.yaml

# Pull manifest
kubectl apply -f https://mn.alefba2.ir/repository/k8s-manifests/deployments/app.yaml

# Push Helm chart
helm package ./my-chart
helm repo index . --url https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader:Token -T ./my-chart-0.1.0.tgz \
  https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader:Token -T ./index.yaml \
  https://mn.alefba2.ir/repository/helm-charts/

# استفاده در Helm
helm repo add my-nexus https://mn.alefba2.ir/repository/helm-charts/ \
  --username k8s-reader --password <Token>
helm repo update
helm install myapp my-nexus/my-chart
```

---

## 18. نکات مهم

1. **همه images و manifests باید ابتدا در registry/nexus push شوند**
2. **تمام Kubernetes nodes باید از این registry استفاده کنند**
3. **رمزهای عبور را در جای امن نگهداری کنید**
4. **Backup منظم انجام دهید**
5. **مانیتورینگ disk space و performance**

---

## 19. مراجع

- [Docker Registry Documentation](https://docs.docker.com/registry/)
- [Nexus Repository Manager Documentation](https://help.sonatype.com/repomanager3)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Certbot Documentation](https://eff-certbot.readthedocs.io/)

---

❤️ Maintained by Soroush

