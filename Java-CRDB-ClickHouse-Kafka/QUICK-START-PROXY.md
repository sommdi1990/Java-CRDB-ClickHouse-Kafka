# راهنمای سریع: تنظیمات Proxy و نصب Calico

<div align="right">

[← بازگشت به صفحه اصلی](Home) | [راهنمای کامل Proxy](Kubernetes-Proxy-Setup)

</div>

---

## خلاصه مراحل

### مرحله 1: روی سرور هلند (141.11.25.11:111)

#### 1.1. راه‌اندازی Docker Registry

```bash
# SSH به سرور هلند
ssh -p 111 user@141.11.25.11

# ایجاد دایرکتوری برای registry
sudo mkdir -p /opt/registry/data

# Pull کردن registry image
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

#### 1.2. دانلود و Push کردن Pause Image

```bash
# دانلود busybox به عنوان pause image
docker pull busybox:latest

# Tag برای registry محلی
docker tag busybox:latest 127.0.0.1:5000/pause:3.10.1

# Push به registry
docker push 127.0.0.1:5000/pause:3.10.1

# بررسی
curl http://127.0.0.1:5000/v2/pause/tags/list
```

#### 1.3. دانلود و Push کردن Calico Images

```bash
# لیست Calico images مورد نیاز
CALICO_IMAGES=(
  "docker.io/calico/cni:v3.26.1"
  "docker.io/calico/node:v3.26.1"
  "docker.io/calico/kube-controllers:v3.26.1"
  "docker.io/calico/pod2daemon-flexvol:v3.26.1"
  "quay.io/tigera/operator:v1.32.0"
  "docker.io/calico/typha:v3.26.1"
)

# دانلود و push هر image
for IMAGE in "${CALICO_IMAGES[@]}"; do
  echo "Processing: $IMAGE"
  
  # Pull image
  docker pull $IMAGE
  
  # Extract image name
  IMAGE_NAME=$(echo $IMAGE | sed 's|.*/||' | cut -d: -f1)
  IMAGE_TAG=$(echo $IMAGE | cut -d: -f2)
  REPO_NAME=$(echo $IMAGE | awk -F'/' '{print $(NF-1)}')
  
  # Tag for local registry
  if [[ $IMAGE == quay.io/* ]]; then
    NEW_TAG="127.0.0.1:5000/tigera/${REPO_NAME}-${IMAGE_NAME}:${IMAGE_TAG}"
  else
    NEW_TAG="127.0.0.1:5000/calico/${REPO_NAME}-${IMAGE_NAME}:${IMAGE_TAG}"
  fi
  
  docker tag $IMAGE $NEW_TAG
  docker push $NEW_TAG
  
  echo "✓ Pushed: $NEW_TAG"
done
```

#### 1.4. دانلود و ویرایش Calico Manifests

```bash
# ایجاد دایرکتوری
mkdir -p /tmp/calico-setup
cd /tmp/calico-setup

# دانلود manifests
curl -o tigera-operator.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml

curl -o custom-resources.yaml \
  https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/custom-resources.yaml

# ویرایش manifests برای استفاده از registry محلی
sed -i 's|docker.io/calico/|127.0.0.1:5000/calico/|g' tigera-operator.yaml
sed -i 's|quay.io/tigera/|127.0.0.1:5000/tigera/|g' tigera-operator.yaml
sed -i 's|docker.io/calico/|127.0.0.1:5000/calico/|g' custom-resources.yaml

# کپی به مکان دائمی
sudo mkdir -p /opt/registry/manifests/calico
sudo cp tigera-operator.yaml /opt/registry/manifests/calico/
sudo cp custom-resources.yaml /opt/registry/manifests/calico/
```

#### 1.5. راه‌اندازی HTTP Server برای Manifests (اختیاری)

```bash
# راه‌اندازی HTTP server روی پورت 8080
cd /opt/registry/manifests/calico
python3 -m http.server 8080 &

# بررسی
curl http://127.0.0.1:8080/tigera-operator.yaml
```

---

### مرحله 2: روی Master Node

#### 2.1. راه‌اندازی SSH Tunnel

```bash
# SSH به Master Node
ssh user@k8s-master

# نصب autossh (اگر نصب نیست)
sudo apt-get install -y autossh  # Ubuntu/Debian
# یا
sudo dnf install -y autossh      # Rocky Linux/RHEL

# ایجاد SSH key (اگر ندارید)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/netherlands_key -N ""

# کپی public key به سرور هلند
ssh-copy-id -i ~/.ssh/netherlands_key.pub -p 111 user@141.11.25.11

# ایجاد systemd service
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

# بررسی
netstat -tlnp | grep 5000
curl http://127.0.0.1:5000/v2/
```

#### 2.2. تنظیمات containerd

```bash
# Backup config
sudo cp /etc/containerd/config.toml /etc/containerd/config.toml.bak

# اگر config وجود ندارد، ایجاد کنید
if [ ! -f /etc/containerd/config.toml ]; then
    containerd config default | sudo tee /etc/containerd/config.toml
fi

# تغییر sandbox_image
sudo sed -i 's|sandbox_image = .*|sandbox_image = "127.0.0.1:5000/pause:3.10.1"|' /etc/containerd/config.toml

# اضافه کردن تنظیمات registry (اگر وجود ندارد)
sudo tee -a /etc/containerd/config.toml > /dev/null <<'EOF'

[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"

[plugins."io.containerd.grpc.v1.cri".registry.mirrors]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."127.0.0.1:5000"]
    endpoint = ["http://127.0.0.1:5000"]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."registry.k8s.io"]
    endpoint = ["http://127.0.0.1:5000", "https://registry.k8s.io"]

[plugins."io.containerd.grpc.v1.cri".registry.configs]
  [plugins."io.containerd.grpc.v1.cri".registry.configs."127.0.0.1:5000".tls]
    insecure_skip_verify = true
EOF

# Restart containerd
sudo systemctl daemon-reload
sudo systemctl restart containerd
sudo systemctl status containerd

# تست pull
sudo crictl pull 127.0.0.1:5000/pause:3.10.1
```

#### 2.3. دانلود Calico Manifests

```bash
# روش 1: از طریق SCP
mkdir -p ~/calico-setup
scp -P 111 user@141.11.25.11:/opt/registry/manifests/calico/*.yaml ~/calico-setup/

# روش 2: از طریق SSH tunnel + HTTP server
# ابتدا SSH tunnel برای port 8080 ایجاد کنید:
ssh -f -N -L 8080:127.0.0.1:8080 -p 111 user@141.11.25.11

# سپس دانلود کنید:
cd ~/calico-setup
curl -o tigera-operator.yaml http://127.0.0.1:8080/tigera-operator.yaml
curl -o custom-resources.yaml http://127.0.0.1:8080/custom-resources.yaml
```

#### 2.4. نصب Calico

```bash
cd ~/calico-setup

# بررسی manifests
cat tigera-operator.yaml | grep -i image

# نصب Tigera Operator
kubectl create -f tigera-operator.yaml

# بررسی وضعیت
kubectl get pods -n tigera-operator-system

# صبر کنید تا operator pod اجرا شود
kubectl get pods -n tigera-operator-system -w

# بعد از اجرای operator، نصب Calico Custom Resources
kubectl create -f custom-resources.yaml

# بررسی وضعیت
kubectl get pods -n calico-system
kubectl get nodes
```

---

### مرحله 3: روی Worker Nodes

#### 3.1. راه‌اندازی SSH Tunnel

```bash
# روی هر Worker Node (k8s-worker1, k8s-worker2)
# تکرار مراحل بخش 2.1 برای هر Worker Node

# SSH به Worker Node
ssh user@k8s-worker1

# نصب autossh
sudo dnf install -y autossh

# ایجاد SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/netherlands_key -N ""

# کپی public key
ssh-copy-id -i ~/.ssh/netherlands_key.pub -p 111 user@141.11.25.11

# ایجاد systemd service
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

# فعال‌سازی
sudo systemctl daemon-reload
sudo systemctl enable registry-tunnel.service
sudo systemctl start registry-tunnel.service

# بررسی
netstat -tlnp | grep 5000
curl http://127.0.0.1:5000/v2/
```

#### 3.2. تنظیمات containerd

```bash
# تکرار مراحل بخش 2.2 برای هر Worker Node

# Backup config
sudo cp /etc/containerd/config.toml /etc/containerd/config.toml.bak

# تغییر sandbox_image
sudo sed -i 's|sandbox_image = .*|sandbox_image = "127.0.0.1:5000/pause:3.10.1"|' /etc/containerd/config.toml

# اضافه کردن تنظیمات registry
sudo tee -a /etc/containerd/config.toml > /dev/null <<'EOF'

[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"

[plugins."io.containerd.grpc.v1.cri".registry.mirrors]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."127.0.0.1:5000"]
    endpoint = ["http://127.0.0.1:5000"]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."registry.k8s.io"]
    endpoint = ["http://127.0.0.1:5000", "https://registry.k8s.io"]

[plugins."io.containerd.grpc.v1.cri".registry.configs]
  [plugins."io.containerd.grpc.v1.cri".registry.configs."127.0.0.1:5000".tls]
    insecure_skip_verify = true
EOF

# Restart containerd
sudo systemctl daemon-reload
sudo systemctl restart containerd

# تست pull
sudo crictl pull 127.0.0.1:5000/pause:3.10.1
```

---

## بررسی وضعیت

### روی Master Node:

```bash
# بررسی nodes
kubectl get nodes

# بررسی Calico pods
kubectl get pods -n calico-system
kubectl get pods -n tigera-operator-system

# بررسی logs در صورت مشکل
kubectl logs -n calico-system -l k8s-app=calico-node

# بررسی events
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -30
```

---

## استفاده از Registry برای Images جدید

### روی سرور هلند:

```bash
# دانلود و push یک image جدید
docker pull docker.io/nginx:latest
docker tag docker.io/nginx:latest 127.0.0.1:5000/nginx:latest
docker push 127.0.0.1:5000/nginx:latest
```

### استفاده در Kubernetes:

```yaml
# در Deployment یا Pod spec
# استفاده از localhost:5000 (از طریق SSH tunnel)
spec:
  containers:
    - name: nginx
      image: 127.0.0.1:5000/nginx:latest
```

---

## Troubleshooting سریع

### مشکل: containerd نمی‌تواند image pull کند

```bash
# بررسی تنظیمات
sudo containerd config dump | grep -A 10 registry

# بررسی SSH tunnel
netstat -tlnp | grep 5000

# تست دستی
sudo crictl pull 127.0.0.1:5000/pause:3.10.1
```

### مشکل: Calico pods در ImagePullBackOff

```bash
# بررسی events
kubectl get events -n calico-system --sort-by='.lastTimestamp'

# بررسی describe
kubectl describe pod <pod-name> -n calico-system

# بررسی image در registry
curl http://127.0.0.1:5000/v2/_catalog
```

### مشکل: دسترسی به Registry

```bash
# بررسی SSH tunnel
sudo systemctl status registry-tunnel.service

# تست از Master Node (از طریق SSH tunnel)
curl http://127.0.0.1:5000/v2/

# اگر tunnel برقرار نیست، راه‌اندازی کنید:
sudo systemctl restart registry-tunnel.service
```

### مشکل: Pause Image Pull نمی‌شود

```bash
# روی سرور هلند - بررسی وجود pause image
curl http://127.0.0.1:5000/v2/pause/tags/list

# اگر موجود نیست، دوباره push کنید:
docker pull busybox:latest
docker tag busybox:latest 127.0.0.1:5000/pause:3.10.1
docker push 127.0.0.1:5000/pause:3.10.1

# روی همه Nodes - بررسی تنظیمات
sudo grep sandbox_image /etc/containerd/config.toml

# Restart containerd
sudo systemctl restart containerd
```

---

## نکات مهم

1. ✅ **مهم**: SSH tunnel باید روی همه Nodes راه‌اندازی شود
2. ✅ Registry فقط روی localhost در دسترس است (از طریق SSH tunnel)
3. ✅ نیازی به باز کردن پورت جدید روی سرور هلند نیست
4. ✅ از proxychains برای دسترسی به اینترنت استفاده می‌شود
5. ✅ Registry محلی insecure است (برای production از TLS استفاده کنید)
6. ✅ به طور منظم images را update کنید
7. ✅ Pause image باید قبل از نصب Calico در registry موجود باشد

---

<div align="center">

[↑ بازگشت به بالا](#راهنمای-سریع-تنظیمات-proxy-و-نصب-calico) | [← بازگشت به صفحه اصلی](Home) | [راهنمای کامل](Kubernetes-Proxy-Setup)

</div>
