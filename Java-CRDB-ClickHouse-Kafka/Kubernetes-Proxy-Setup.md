# راهنمای تنظیمات Proxy و Repository موقت برای Kubernetes

<div align="right">

[← بازگشت به صفحه اصلی](Home) | [راهنمای Kubernetes](Kubernetes-Implementation-Guide)

</div>

---

## فهرست مطالب

1. [پیش‌نیازها](#1-پیشنیازها)
2. [تنظیمات Proxy روی سرور هلند](#2-تنظیمات-proxy-روی-سرور-هلند)
3. [تنظیمات Proxy برای containerd](#3-تنظیمات-proxy-برای-containerd)
4. [تنظیمات Proxy برای kubectl](#4-تنظیمات-proxy-برای-kubectl)
5. [راه‌اندازی Docker Registry روی سرور هلند](#5-راهاندازی-docker-registry-روی-سرور-هلند)
6. [دانلود و Push کردن Calico Images](#6-دانلود-و-push-کردن-calico-images)
7. [نصب Calico با استفاده از Registry محلی](#7-نصب-calico-با-استفاده-از-registry-محلی)
8. [راه‌حل دائمی برای آینده](#8-راهحل-دائمی-برای-آینده)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. پیش‌نیازها

### 1.1. اطلاعات سرور هلند

- **IP**: 141.11.25.11
- **SSH Port**: 111 (تنها پورت باز)
- **Proxy SOCKS5**: 141.11.25.11:1080 (سرویس‌دهنده proxy برای سرور ایران)
- **اینترنت**: آزاد و استیبل
- **نقش**: واسطه بین سرور ایران و اینترنت آزاد
- **نکته مهم**: فقط پورت SSH (111) باز است. Registry از طریق SSH port forwarding در دسترس خواهد بود.

### 1.2. نرم‌افزارهای مورد نیاز روی سرور هلند

- Docker
- Docker Registry (روی localhost)
- curl, wget
- git
- **نکته**: سرور هلند اینترنت آزاد دارد، نیازی به proxychains نیست

### 1.3. نرم‌افزارهای مورد نیاز روی سرور ایران (Nodes)

- SSH client
- kubectl (روی Master Node)
- containerd (روی همه Nodes)
- **proxychains** (برای اتصال به proxy سرور هلند)
- **نکته**: proxychains روی سرور ایران به 141.11.25.11:1080 وصل می‌شود

---

## 2. تنظیمات روی سرور هلند

### 2.1. بررسی وضعیت SOCKS5 Proxy

```bash
# روی سرور هلند (141.11.25.11)
# بررسی وضعیت SOCKS5 proxy (که به سرور ایران سرویس می‌دهد)
ps aux | grep -E "socks|1080" | grep -v grep
netstat -tlnp | grep 1080

# تست SOCKS5 proxy
curl --socks5 127.0.0.1:1080 https://www.google.com
```

**نکته**: سرور هلند اینترنت آزاد دارد، نیازی به proxychains برای Docker نیست.

### 2.2. تنظیمات Docker Registry (روی localhost)

```bash
# روی سرور هلند
# Registry را روی localhost راه‌اندازی می‌کنیم (نه روی IP عمومی)
sudo mkdir -p /opt/registry/data

# Pull کردن registry image (اینترنت آزاد دارد، نیازی به proxy نیست)
docker pull registry:2

# راه‌اندازی Registry روی localhost:5000
docker run -d \
  --name registry \
  --restart=always \
  -p 127.0.0.1:5000:5000 \
  -v /opt/registry/data:/var/lib/registry \
  -e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 \
  registry:2

# بررسی وضعیت
docker ps | grep registry
curl http://127.0.0.1:5000/v2/
```

**نکته**: Registry فقط روی localhost در دسترس است. از طریق SSH port forwarding به Nodes دسترسی می‌دهیم.

---

## 3. راه‌اندازی SSH Port Forwarding برای دسترسی به Registry

### 3.1. ایجاد SSH Tunnel از سرور ایران به سرور هلند

**روش 1: Port Forwarding موقت (برای تست)**

```bash
# روی سرور ایران (Master Node یا هر Node)
# ایجاد SSH tunnel برای دسترسی به Registry
ssh -f -N -L 5000:127.0.0.1:5000 -p 111 user@141.11.25.11

# بررسی وضعیت
netstat -tlnp | grep 5000
curl http://127.0.0.1:5000/v2/
```

**روش 2: Port Forwarding دائمی با autossh (توصیه می‌شود)**

```bash
# روی سرور ایران
# نصب autossh
sudo apt-get install -y autossh  # Ubuntu/Debian
# یا
sudo dnf install -y autossh      # Rocky Linux/RHEL

# ایجاد SSH key (اگر ندارید)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/netherlands_key -N ""

# کپی کردن public key به سرور هلند
ssh-copy-id -i ~/.ssh/netherlands_key.pub -p 111 user@141.11.25.11

# ایجاد systemd service برای autossh
sudo mkdir -p /etc/systemd/system

cat <<EOF | sudo tee /etc/systemd/system/registry-tunnel.service
[Unit]
Description=SSH Tunnel to Netherlands Registry
After=network.target

[Service]
Type=simple
User=$(whoami)
ExecStart=/usr/bin/autossh -M 0 -f -N -o "ServerAliveInterval 60" -o "ServerAliveCountMax 3" -L 5000:127.0.0.1:5000 -p 111 user@141.11.25.11
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# فعال‌سازی و راه‌اندازی
sudo systemctl daemon-reload
sudo systemctl enable registry-tunnel.service
sudo systemctl start registry-tunnel.service
sudo systemctl status registry-tunnel.service
```

### 3.2. راه‌اندازی SSH Tunnel روی همه Nodes

```bash
# روی هر Node (Master و Worker)
# تکرار مراحل بخش 3.1 برای هر Node

# گام 1: نصب autossh (اگر نصب نیست)
sudo apt-get install -y autossh  # Ubuntu/Debian
# یا
sudo dnf install -y autossh      # Rocky Linux/RHEL

# گام 2: ایجاد SSH key (اگر ندارید)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/netherlands_key -N ""

# گام 3: کپی کردن public key به سرور هلند
ssh-copy-id -i ~/.ssh/netherlands_key.pub -p 111 user@141.11.25.11

# گام 4: ایجاد systemd service برای autossh
sudo mkdir -p /etc/systemd/system

cat <<EOF | sudo tee /etc/systemd/system/registry-tunnel.service
[Unit]
Description=SSH Tunnel to Netherlands Registry
After=network.target

[Service]
Type=simple
User=$(whoami)
ExecStart=/usr/bin/autossh -M 0 -f -N -o "ServerAliveInterval 60" -o "ServerAliveCountMax 3" -L 5000:127.0.0.1:5000 -p 111 user@141.11.25.11
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# گام 5: فعال‌سازی و راه‌اندازی
sudo systemctl daemon-reload
sudo systemctl enable registry-tunnel.service
sudo systemctl start registry-tunnel.service
sudo systemctl status registry-tunnel.service

# گام 6: بررسی وضعیت
netstat -tlnp | grep 5000
curl http://127.0.0.1:5000/v2/
```

---

## 4. تنظیمات Proxy برای containerd

### 4.1. تنظیمات containerd روی Master و Worker Nodes

**مهم**: Registry از طریق SSH tunnel روی localhost:5000 در دسترس است.

```bash
# روی همه Nodes (k8s-master, k8s-worker1, k8s-worker2, k8s-management)
# ابتدا SSH tunnel را راه‌اندازی کنید (بخش 3)

# تنظیمات containerd config.toml برای استفاده از Registry محلی
sudo mkdir -p /etc/containerd

# اگر config.toml وجود ندارد، ایجاد کنید
if [ ! -f /etc/containerd/config.toml ]; then
    containerd config default | sudo tee /etc/containerd/config.toml
fi

# اضافه کردن registry محلی به config.toml (localhost:5000 از طریق SSH tunnel)
sudo sed -i '/\[plugins."io.containerd.grpc.v1.cri".registry.mirrors\]/a\  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."127.0.0.1:5000"]\n    endpoint = ["http://127.0.0.1:5000"]' /etc/containerd/config.toml

# اضافه کردن تنظیمات insecure registry
sudo sed -i '/\[plugins."io.containerd.grpc.v1.cri".registry.configs\]/a\  [plugins."io.containerd.grpc.v1.cri".registry.configs."127.0.0.1:5000".tls]\n    insecure_skip_verify = true' /etc/containerd/config.toml

# برای pull کردن images از اینترنت، از proxychains استفاده می‌کنیم
# containerd به طور مستقیم از SOCKS5 پشتیبانی نمی‌کند
# راه‌حل: استفاده از registry محلی که images را از اینترنت pull می‌کند

# Restart containerd
sudo systemctl daemon-reload
sudo systemctl restart containerd
```

### 4.2. بررسی تنظیمات containerd

```bash
# روی همه Nodes
sudo systemctl status containerd
sudo containerd config dump | grep -A 10 registry

# تست pull از registry محلی (از طریق SSH tunnel)
sudo crictl pull 127.0.0.1:5000/alpine:latest
```

---

## 5. تنظیمات Proxy برای kubectl

### 5.1. تنظیمات Proxy برای kubectl با استفاده از proxychains

**مهم**:

- سرور ایران proxychains نصب دارد و به 141.11.25.11:1080 وصل می‌شود
- از طریق این proxy به اینترنت دسترسی دارد
- kubectl نیاز به دسترسی به اینترنت برای دانلود manifests دارد

```bash
# روی Master Node و Management Node (سرور ایران)
# بررسی نصب proxychains
proxychains --version

# اگر نصب نیست:
sudo apt-get update && sudo apt-get install -y proxychains4  # Ubuntu/Debian
# یا
sudo dnf install -y proxychains-ng  # Rocky Linux/RHEL

# تنظیمات proxychains برای اتصال به سرور هلند
sudo cp /etc/proxychains.conf /etc/proxychains.conf.bak

# اضافه کردن SOCKS5 proxy به proxychains (سرور هلند)
cat <<EOF | sudo tee -a /etc/proxychains.conf
# SOCKS5 Proxy برای دسترسی به اینترنت از طریق سرور هلند
socks5 141.11.25.11 1080
EOF

# تست اتصال
proxychains curl -I https://www.google.com

# استفاده از proxychains با kubectl
# برای دانلود manifests:
proxychains kubectl apply -f https://raw.githubusercontent.com/...
```

### 5.2. استفاده از Manifests محلی (توصیه می‌شود)

به جای دانلود مستقیم، manifests را از سرور هلند دانلود کنید:

```bash
# روی Master Node
# دانلود manifests از سرور هلند (از طریق SSH)
scp -P 111 user@141.11.25.11:/opt/registry/manifests/calico/*.yaml ~/calico-setup/

# یا استفاده از HTTP server روی سرور هلند (از طریق SSH tunnel)
# ابتدا SSH tunnel برای port 8080 ایجاد کنید:
ssh -f -N -L 8080:127.0.0.1:8080 -p 111 user@141.11.25.11

# سپس دانلود کنید:
curl http://127.0.0.1:8080/tigera-operator.yaml
```

### 4.3. تست اتصال kubectl با Proxy

```bash
# روی Master Node
# تست بدون proxy
kubectl get nodes

# تست با proxy (اگر environment variables تنظیم شده)
export HTTP_PROXY=http://141.11.25.11:8123
export HTTPS_PROXY=http://141.11.25.11:8123
kubectl get nodes
```

---

## 6. راه‌اندازی Docker Registry روی سرور هلند (تکمیل شده در بخش 2)

### 5.1. نصب و راه‌اندازی Docker Registry

```bash
# روی سرور هلند (141.11.25.11)
# Pull کردن Docker Registry image
docker pull registry:2

# ایجاد دایرکتوری برای storage
sudo mkdir -p /opt/registry/data

# اجرای Docker Registry
docker run -d \
  --name registry \
  --restart=always \
  -p 5000:5000 \
  -v /opt/registry/data:/var/lib/registry \
  -e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 \
  registry:2

# بررسی وضعیت
docker ps | grep registry
docker logs registry
```

### 5.2. تنظیمات Firewall (اگر فعال است)

```bash
# روی سرور هلند
# برای UFW
sudo ufw allow 5000/tcp

# برای firewalld (Rocky Linux)
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

### 5.3. تست Registry

```bash
# روی سرور هلند
# Pull کردن یک image تست
docker pull alpine:latest

# Tag کردن برای registry محلی
docker tag alpine:latest 141.11.25.11:5000/alpine:latest

# Push کردن به registry محلی
docker push 141.11.25.11:5000/alpine:latest

# Pull کردن از registry محلی
docker pull 141.11.25.11:5000/alpine:latest
```

---

## 7. دانلود و Push کردن Calico Images

### 7.1. شناسایی Images مورد نیاز Calico

```bash
# روی سرور هلند
# دانلود Calico manifests (اینترنت آزاد دارد، نیازی به proxy نیست)
mkdir -p /tmp/calico-setup
cd /tmp/calico-setup

# دانلود manifests مستقیماً (اینترنت آزاد)
curl -o tigera-operator.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml

curl -o custom-resources.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/custom-resources.yaml

# استخراج لیست images از manifests
grep -r "image:" tigera-operator.yaml custom-resources.yaml | grep -v "#" | awk '{print $2}' | sort -u > calico-images.txt

cat calico-images.txt
```

### 7.2. دانلود و Push کردن Images

```bash
# روی سرور هلند
# تنظیمات
REGISTRY="127.0.0.1:5000"  # localhost چون از SSH tunnel استفاده می‌کنیم

# لیست images Calico (نسخه 3.26.1)
IMAGES=(
  "docker.io/calico/cni:v3.26.1"
  "docker.io/calico/node:v3.26.1"
  "docker.io/calico/kube-controllers:v3.26.1"
  "docker.io/calico/pod2daemon-flexvol:v3.26.1"
  "quay.io/tigera/operator:v1.32.0"
  "docker.io/calico/typha:v3.26.1"
)

echo "Starting download and push process..."

for IMAGE in "${IMAGES[@]}"; do
  echo "Processing: $IMAGE"
  
  # Extract image name and tag
  IMAGE_NAME=$(echo $IMAGE | sed 's|.*/||' | cut -d: -f1)
  IMAGE_TAG=$(echo $IMAGE | cut -d: -f2)
  REPO_NAME=$(echo $IMAGE | awk -F'/' '{print $(NF-1)}')
  
  # Pull image مستقیماً (اینترنت آزاد دارد)
  echo "  Pulling $IMAGE..."
  docker pull $IMAGE
  
  # Tag for local registry
  if [[ $IMAGE == quay.io/* ]]; then
    NEW_TAG="${REGISTRY}/tigera/${REPO_NAME}-${IMAGE_NAME}:${IMAGE_TAG}"
  else
    NEW_TAG="${REGISTRY}/calico/${REPO_NAME}-${IMAGE_NAME}:${IMAGE_TAG}"
  fi
  echo "  Tagging as $NEW_TAG..."
  docker tag $IMAGE $NEW_TAG
  
  # Push to local registry
  echo "  Pushing $NEW_TAG..."
  docker push $NEW_TAG
  
  echo "  ✓ Done: $NEW_TAG"
  echo ""
done

echo "All images downloaded and pushed successfully!"
```

### 7.3. دانلود دستی Images (اگر اسکریپت کار نکرد)

```bash
# روی سرور هلند
# دانلود Calico images مستقیماً (اینترنت آزاد دارد)
docker pull docker.io/calico/cni:v3.26.1
docker pull docker.io/calico/node:v3.26.1
docker pull docker.io/calico/kube-controllers:v3.26.1
docker pull docker.io/calico/pod2daemon-flexvol:v3.26.1
docker pull quay.io/tigera/operator:v1.32.0
docker pull docker.io/calico/typha:v3.26.1

# Tag و Push (استفاده از localhost:5000)
docker tag docker.io/calico/cni:v3.26.1 127.0.0.1:5000/calico/cni:v3.26.1
docker tag docker.io/calico/node:v3.26.1 127.0.0.1:5000/calico/node:v3.26.1
docker tag docker.io/calico/kube-controllers:v3.26.1 127.0.0.1:5000/calico/kube-controllers:v3.26.1
docker tag docker.io/calico/pod2daemon-flexvol:v3.26.1 127.0.0.1:5000/calico/pod2daemon-flexvol:v3.26.1
docker tag quay.io/tigera/operator:v1.32.0 127.0.0.1:5000/tigera/operator:v1.32.0
docker tag docker.io/calico/typha:v3.26.1 127.0.0.1:5000/calico/typha:v3.26.1

# Push
docker push 127.0.0.1:5000/calico/cni:v3.26.1
docker push 127.0.0.1:5000/calico/node:v3.26.1
docker push 127.0.0.1:5000/calico/kube-controllers:v3.26.1
docker push 127.0.0.1:5000/calico/pod2daemon-flexvol:v3.26.1
docker push 127.0.0.1:5000/tigera/operator:v1.32.0
docker push 127.0.0.1:5000/calico/typha:v3.26.1
```

### 7.4. دانلود و ویرایش Manifests

```bash
# روی سرور هلند
cd /tmp/calico-setup

# دانلود manifests مستقیماً (اینترنت آزاد)
curl -o tigera-operator.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml

curl -o custom-resources.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/custom-resources.yaml

# ویرایش manifests برای استفاده از registry محلی (localhost:5000)
# جایگزینی image URLs
sed -i 's|docker.io/calico/|127.0.0.1:5000/calico/|g' tigera-operator.yaml
sed -i 's|quay.io/tigera/|127.0.0.1:5000/tigera/|g' tigera-operator.yaml
sed -i 's|docker.io/calico/|127.0.0.1:5000/calico/|g' custom-resources.yaml

# کپی کردن manifests به یک مکان دائمی
sudo mkdir -p /opt/registry/manifests/calico
sudo cp tigera-operator.yaml /opt/registry/manifests/calico/
sudo cp custom-resources.yaml /opt/registry/manifests/calico/
```

---

## 8. نصب Calico با استفاده از Registry محلی

### 8.1. کپی کردن Manifests به Master Node

```bash
# روی Master Node
# دانلود manifests از سرور هلند با استفاده از SCP
mkdir -p ~/calico-setup
cd ~/calico-setup

# کپی از سرور هلند
scp -P 111 user@141.11.25.11:/opt/registry/manifests/calico/*.yaml .

# یا استفاده از SSH tunnel + HTTP server
# ابتدا روی سرور هلند HTTP server را راه‌اندازی کنید:
# cd /opt/registry/manifests/calico
# python3 -m http.server 8080 &

# سپس روی Master Node SSH tunnel ایجاد کنید:
# ssh -f -N -L 8080:127.0.0.1:8080 -p 111 user@141.11.25.11

# و دانلود کنید:
# curl -o tigera-operator.yaml http://127.0.0.1:8080/tigera-operator.yaml
# curl -o custom-resources.yaml http://127.0.0.1:8080/custom-resources.yaml
```

### 8.2. نصب Calico Operator

```bash
# روی Master Node
cd ~/calico-setup

# بررسی manifests قبل از اعمال
cat tigera-operator.yaml | grep -i image

# اعمال manifests
kubectl create -f tigera-operator.yaml

# بررسی وضعیت
kubectl get pods -n tigera-operator-system
```

### 8.3. نصب Calico Custom Resources

```bash
# روی Master Node
cd ~/calico-setup

# بررسی custom-resources.yaml
cat custom-resources.yaml

# اعمال custom resources
kubectl create -f custom-resources.yaml

# بررسی وضعیت
kubectl get pods -n calico-system
kubectl get nodes
```

### 8.4. بررسی نصب Calico

```bash
# روی Master Node
# بررسی pods
kubectl get pods -n calico-system
kubectl get pods -n tigera-operator-system

# بررسی nodes
kubectl get nodes

# بررسی Calico pods
kubectl get pods -n calico-system -o wide

# بررسی logs در صورت مشکل
kubectl logs -n calico-system -l k8s-app=calico-node
```

---

## 9. راه‌حل دائمی برای آینده

### 8.1. دانلود Images جدید به صورت دستی

```bash
# روی سرور هلند
# برای دانلود و push یک image جدید:

# تنظیمات
REGISTRY="127.0.0.1:5000"
SOURCE_IMAGE="docker.io/nginx:latest"  # مثال
TARGET_NAME="nginx:latest"  # یا هر نام دیگری

# Pull image
echo "Pulling $SOURCE_IMAGE..."
docker pull $SOURCE_IMAGE

# Tag برای registry محلی
TARGET_IMAGE="${REGISTRY}/${TARGET_NAME}"
echo "Tagging as $TARGET_IMAGE..."
docker tag $SOURCE_IMAGE $TARGET_IMAGE

# Push به registry
echo "Pushing $TARGET_IMAGE..."
docker push $TARGET_IMAGE

echo "✓ Image available at: $TARGET_IMAGE"

# مثال کامل:
# docker pull docker.io/nginx:latest
# docker tag docker.io/nginx:latest 127.0.0.1:5000/nginx:latest
# docker push 127.0.0.1:5000/nginx:latest
```

### 8.2. راه‌اندازی Harbor (راه‌حل Enterprise)

```bash
# روی سرور هلند
# Harbor یک Docker Registry enterprise-grade است
# با UI و features بیشتر

# دانلود Harbor installer
cd /tmp
curl --proxy http://127.0.0.1:8123 \
  -o harbor-offline-installer.tgz \
  https://github.com/goharbor/harbor/releases/download/v2.9.0/harbor-offline-installer-v2.9.0.tgz

tar xvf harbor-offline-installer.tgz
cd harbor

# ویرایش harbor.yml
# تنظیم hostname: 141.11.25.11
# تنظیم port: 5000 یا 80
# تنظیمات proxy در harbor.yml

# نصب Harbor
sudo ./install.sh
```

### 8.3. تنظیمات Registry Mirror در containerd (همه Nodes)

```bash
# روی همه Nodes
# اضافه کردن به /etc/containerd/config.toml
sudo cat >> /etc/containerd/config.toml <<EOF

[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"

[plugins."io.containerd.grpc.v1.cri".registry.mirrors]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
    endpoint = ["http://141.11.25.11:5000", "https://registry-1.docker.io"]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."quay.io"]
    endpoint = ["http://141.11.25.11:5000", "https://quay.io"]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."141.11.25.11:5000"]
    endpoint = ["http://141.11.25.11:5000"]

[plugins."io.containerd.grpc.v1.cri".registry.configs."141.11.25.11:5000".tls]
  insecure_skip_verify = true
EOF

# Restart containerd
sudo systemctl restart containerd
```

### 8.4. Pull و Push خودکار Images (با استفاده از Loop)

```bash
# روی سرور هلند
# لیست images مورد نیاز
REGISTRY="127.0.0.1:5000"

# ایجاد لیست images
IMAGE_LIST=(
  "docker.io/nginx:latest"
  "docker.io/redis:7-alpine"
  "docker.io/postgres:15-alpine"
  "docker.io/mysql:8.0"
  "quay.io/prometheus/prometheus:latest"
  "docker.io/grafana/grafana:latest"
)

# پردازش هر image
for IMAGE in "${IMAGE_LIST[@]}"; do
  if [ -z "$IMAGE" ] || [[ "$IMAGE" =~ ^# ]]; then
    continue
  fi
  
  echo "Processing: $IMAGE"
  
  # Extract components
  IMAGE_NAME=$(echo $IMAGE | sed 's|.*/||')
  REPO_PATH=$(echo $IMAGE | sed 's|:[^:]*$||' | sed 's|^[^/]*/||')
  
  # Pull
  docker pull $IMAGE || {
    echo "Failed to pull $IMAGE"
    continue
  }
  
  # Tag
  TARGET_IMAGE="${REGISTRY}/${REPO_PATH}"
  docker tag $IMAGE $TARGET_IMAGE
  
  # Push
  docker push $TARGET_IMAGE || {
    echo "Failed to push $TARGET_IMAGE"
    continue
  }
  
  echo "✓ Synced: $IMAGE -> $TARGET_IMAGE"
done

echo "Sync completed!"
```

### 8.5. Cron Job برای Sync منظم

```bash
# روی سرور هلند
# برای استفاده از cron job، باید دستورات را در یک فایل قرار دهید
# یا مستقیماً در crontab قرار دهید

# روش 1: استفاده از فایل script (توصیه می‌شود)
# ابتدا دستورات بخش 8.4 را در یک فایل قرار دهید:
# nano /opt/registry/sync-images.sh
# سپس chmod +x /opt/registry/sync-images.sh

# اضافه کردن به crontab
crontab -l > /tmp/crontab.bak 2>/dev/null || true
echo "0 2 * * * /opt/registry/sync-images.sh >> /var/log/registry-sync.log 2>&1" >> /tmp/crontab.bak
crontab /tmp/crontab.bak

# یا روش 2: مستقیماً در crontab (بدون فایل script)
# crontab -e
# سپس اضافه کنید:
# 0 2 * * * cd /opt/registry && [دستورات بخش 8.4] >> /var/log/registry-sync.log 2>&1
```

---

## 10. Troubleshooting

### 9.1. مشکل: containerd نمی‌تواند images را pull کند

```bash
# بررسی تنظیمات containerd
sudo containerd config dump | grep -A 20 registry

# بررسی logs
sudo journalctl -u containerd -f

# تست pull دستی
sudo crictl pull 141.11.25.11:5000/calico/cni:v3.26.1
```

### 9.2. مشکل: kubectl نمی‌تواند manifests را دانلود کند

```bash
# بررسی proxy settings
echo $HTTP_PROXY
echo $HTTPS_PROXY

# تست دسترسی
curl --proxy http://141.11.25.11:8123 https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml

# استفاده از manifests محلی
kubectl create -f /path/to/local/tigera-operator.yaml
```

### 9.3. مشکل: Calico pods در حالت ImagePullBackOff

```bash
# بررسی events
kubectl get events -n calico-system --sort-by='.lastTimestamp'

# بررسی describe pod
kubectl describe pod <pod-name> -n calico-system

# بررسی image pull secrets
kubectl get secrets -n calico-system

# اگر image در registry محلی موجود نیست، دوباره push کنید
# روی سرور هلند
docker push 141.11.25.11:5000/calico/cni:v3.26.1
```

### 9.3.0. مشکل: Failed to pull image "registry.k8s.io/pause:3.10.1" - 403 Forbidden

**علت**: containerd نمی‌تواند pause image را از registry.k8s.io pull کند. این image برای sandbox pods ضروری است.

**راه‌حل**:

```bash
# گام 1: دانلود pause image روی سرور هلند و push به registry محلی
# روی سرور هلند (141.11.25.11)
docker pull registry.k8s.io/pause:3.10.1
# یا از docker.io
docker pull docker.io/registry.k8s.io/pause:3.10.1
# یا از gcr.io
docker pull gcr.io/google-containers/pause:3.10

# Tag برای registry محلی
docker tag registry.k8s.io/pause:3.10.1 127.0.0.1:5000/pause:3.10.1
# یا
docker tag docker.io/registry.k8s.io/pause:3.10.1 127.0.0.1:5000/pause:3.10.1
# یا
docker tag gcr.io/google-containers/pause:3.10 127.0.0.1:5000/pause:3.10

# Push به registry محلی
docker push 127.0.0.1:5000/pause:3.10.1

# گام 2: تنظیمات containerd برای استفاده از registry محلی برای pause image
# روی همه Nodes (Master و Worker)
sudo mkdir -p /etc/containerd

# Backup config فعلی
sudo cp /etc/containerd/config.toml /etc/containerd/config.toml.bak

# اگر config وجود ندارد، ایجاد کنید
if [ ! -f /etc/containerd/config.toml ]; then
    containerd config default | sudo tee /etc/containerd/config.toml
fi

# ویرایش config.toml برای تنظیم pause image و registry
sudo tee -a /etc/containerd/config.toml > /dev/null <<EOF

[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"

[plugins."io.containerd.grpc.v1.cri".registry.mirrors]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."127.0.0.1:5000"]
    endpoint = ["http://127.0.0.1:5000"]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."registry.k8s.io"]
    endpoint = ["http://127.0.0.1:5000", "https://registry.k8s.io"]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
    endpoint = ["http://127.0.0.1:5000", "https://registry-1.docker.io"]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."gcr.io"]
    endpoint = ["http://127.0.0.1:5000", "https://gcr.io"]

[plugins."io.containerd.grpc.v1.cri".registry.configs]
  [plugins."io.containerd.grpc.v1.cri".registry.configs."127.0.0.1:5000".tls]
    insecure_skip_verify = true

[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "127.0.0.1:5000/pause:3.10.1"
EOF

# یا اگر می‌خواهید فقط sandbox_image را تغییر دهید:
sudo sed -i 's|sandbox_image = .*|sandbox_image = "127.0.0.1:5000/pause:3.10.1"|' /etc/containerd/config.toml

# Restart containerd
sudo systemctl daemon-reload
sudo systemctl restart containerd
sudo systemctl status containerd

# گام 3: بررسی تنظیمات
sudo containerd config dump | grep -A 5 "sandbox_image"
sudo containerd config dump | grep -A 20 "registry"

# گام 4: تست pull pause image
sudo crictl pull 127.0.0.1:5000/pause:3.10.1

# گام 5: حذف pods مشکل‌دار و اجازه دهید دوباره ایجاد شوند
# روی Master Node
kubectl delete pod -n tigera-operator-system --all
kubectl delete pod -n kube-system --all

# بررسی مجدد
kubectl get pods --all-namespaces
```

**نکته مهم**: اگر pause image با tag متفاوت در registry موجود است، از همان tag استفاده کنید.

### 9.3.1. مشکل: هیچ Pod در calico-system یا tigera-operator-system وجود ندارد

**علت**: معمولاً tigera-operator pod اجرا نشده یا نمی‌تواند images را pull کند.

**راه‌حل گام به گام**:

```bash
# گام 1: بررسی وضعیت tigera-operator
kubectl get pods --all-namespaces | grep tigera
kubectl get pods -n tigera-operator-system

# گام 2: بررسی events برای خطاها
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -50
kubectl get events -n tigera-operator-system --sort-by='.lastTimestamp'

# گام 3: بررسی deployments و replicasets
kubectl get deployments -n tigera-operator-system
kubectl get replicasets -n tigera-operator-system
kubectl get daemonsets -n tigera-operator-system

# گام 4: بررسی describe برای operator deployment
kubectl describe deployment tigera-operator -n tigera-operator-system

# گام 5: بررسی SSH tunnel به registry
# روی Master Node
netstat -tlnp | grep 5000
curl http://127.0.0.1:5000/v2/

# اگر SSH tunnel کار نمی‌کند:
# بررسی وضعیت autossh service
sudo systemctl status registry-tunnel.service

# یا ایجاد دستی SSH tunnel
ssh -f -N -L 5000:127.0.0.1:5000 -p 111 user@141.11.25.11

# گام 6: بررسی تنظیمات containerd برای registry
sudo containerd config dump | grep -A 30 registry

# گام 7: تست pull image از registry محلی
sudo crictl pull 127.0.0.1:5000/tigera/operator:v1.32.0

# گام 8: بررسی logs containerd برای خطاهای pull
sudo journalctl -u containerd -n 100 | grep -i "pull\|error\|registry"

# گام 9: بررسی اینکه images در registry هلند موجود هستند
# روی سرور هلند
docker images | grep tigera
docker images | grep calico
curl http://127.0.0.1:5000/v2/_catalog

# گام 10: اگر operator pod وجود دارد اما CrashLoopBackOff است
kubectl get pods -n tigera-operator-system
kubectl logs -n tigera-operator-system -l name=tigera-operator --tail=100
kubectl describe pod -n tigera-operator-system -l name=tigera-operator

# گام 11: حذف و نصب مجدد operator (اگر لازم باشد)
kubectl delete -f tigera-operator.yaml
# بررسی و اصلاح manifests
kubectl create -f tigera-operator.yaml

# گام 12: بررسی custom-resources
kubectl get installation -n default
kubectl get apiserver -n default
kubectl describe installation default
kubectl describe apiserver default
```

**مشکلات رایج و راه‌حل**:

1. **SSH Tunnel کار نمی‌کند**:
   ```bash
   # بررسی و راه‌اندازی مجدد
   sudo systemctl restart registry-tunnel.service
   sudo systemctl status registry-tunnel.service
   ```

2. **Images در registry موجود نیستند**:
   ```bash
   # روی سرور هلند - دوباره push کنید
   # تکرار مراحل بخش 7.2 برای دانلود و push images
   ```

3. **containerd نمی‌تواند به registry دسترسی پیدا کند**:
   ```bash
   # بررسی config.toml
   sudo cat /etc/containerd/config.toml | grep -A 10 "127.0.0.1:5000"
   
   # اگر تنظیمات ناقص است، دوباره تنظیم کنید (بخش 4.1)
   sudo systemctl restart containerd
   ```

4. **Operator pod در حالت ImagePullBackOff**:
   ```bash
   # بررسی image در manifest
   kubectl get deployment tigera-operator -n tigera-operator-system -o yaml | grep image
   
   # اگر image به registry محلی اشاره نمی‌کند، manifest را اصلاح کنید
   ```

### 9.4. مشکل: دسترسی به Registry از Nodes

```bash
# روی همه Nodes
# تست دسترسی به registry
curl http://141.11.25.11:5000/v2/

# بررسی firewall
sudo firewall-cmd --list-all

# تست pull از registry
sudo crictl pull 141.11.25.11:5000/alpine:latest
```

### 9.5. مشکل: Proxy Connection Timeout

```bash
# روی سرور هلند
# بررسی وضعیت socat
ps aux | grep socat
netstat -tlnp | grep 8123

# Restart socat
pkill socat
nohup socat TCP-LISTEN:8123,fork SOCKS4A:127.0.0.1:$(grep socks /etc/proxychains.conf | head -1 | awk '{print $2}'):$(grep socks /etc/proxychains.conf | head -1 | awk '{print $3}'),socksport=1080 > /tmp/socat.log 2>&1 &

# بررسی logs
tail -f /tmp/socat.log
```

---

## خلاصه مراحل

### روی سرور هلند (141.11.25.11):

1. ✅ تنظیمات Proxy (SOCKS5 و HTTP)
2. ✅ راه‌اندازی Docker Registry
3. ✅ دانلود Calico images و push به registry محلی
4. ✅ دانلود و ویرایش Calico manifests
5. ✅ راه‌اندازی HTTP server برای دسترسی به manifests

### روی Master Node:

1. ✅ تنظیمات Proxy برای containerd
2. ✅ تنظیمات Registry Mirror در containerd
3. ✅ دانلود Calico manifests از سرور هلند
4. ✅ نصب Calico با استفاده از manifests محلی

### روی Worker Nodes:

1. ✅ تنظیمات Proxy برای containerd
2. ✅ تنظیمات Registry Mirror در containerd

---

## نکات مهم

1. **امنیت**: Registry محلی شما insecure است. برای production از TLS استفاده کنید.
2. **Backup**: به طور منظم registry را backup کنید.
3. **Monitoring**: فضای دیسک registry را مانیتور کنید.
4. **Updates**: به طور منظم images را update کنید.

---

<div align="center">

[↑ بازگشت به بالا](#راهنمای-تنظیمات-proxy-و-repository-موقت-برای-kubernetes) | [← بازگشت به صفحه اصلی](Home) | [راهنمای Kubernetes](Kubernetes-Implementation-Guide)

</div>

