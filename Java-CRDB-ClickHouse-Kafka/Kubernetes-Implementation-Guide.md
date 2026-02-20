# راهنمای فنی پیاده‌سازی Kubernetes - قدم به قدم

<div align="right">

[← بازگشت به صفحه اصلی](Home) | [پروپوزال Kubernetes](Proposal-Kubernetes) | [لینک‌های مفید](References)

</div>

---

## فهرست مطالب

0. [تنظیمات اولیه Registry و Nexus](#0-تنظیمات-اولیه-registry-و-nexus) ⭐
1. [پیش‌نیازها و آماده‌سازی](#1-پیشنیازها-و-آمادهسازی)
2. [نصب و راه‌اندازی VMware ESXi 8](#2-نصب-و-راهاندازی-vmware-esxi-8)
3. [نصب Rocky Linux 10 روی VMها](#3-نصب-rocky-linux-10-روی-vmها)
4. [راه‌اندازی Kubernetes Cluster](#4-راهاندازی-kubernetes-cluster)
5. [نصب CNI Plugin و Networking](#5-نصب-cni-plugin-و-networking)
6. [نصب Ingress Controller](#6-نصب-ingress-controller)
7. [راه‌اندازی Monitoring Stack](#7-راهاندازی-monitoring-stack)
8. [Deploy Backend Services](#8-deploy-backend-services)
9. [Deploy Frontend Services](#9-deploy-frontend-services)
10. [Deploy Databases](#10-deploy-databases)
11. [Deploy Messaging (Kafka/Redpanda)](#11-deploy-messaging-kafkaredpanda)
12. [راه‌اندازی Infrastructure Tools](#12-راهاندازی-infrastructure-tools)
13. [راه‌اندازی Security و RBAC](#13-راهاندازی-security-و-rbac)
14. [راه‌اندازی Backup و Disaster Recovery](#14-راهاندازی-backup-و-disaster-recovery)
15. [تنظیمات Port و Networking](#15-تنظیمات-port-و-networking)
16. [بهینه‌سازی و Performance Tuning](#16-بهینهسازی-و-performance-tuning)

---

## ⚠ نکات مهم و راهنمای استفاده

### مشخصات Infrastructure

- **Registry**: `rr.alefba2.ir` - تمام Docker images در این registry هستند
- **Nexus**: `mn.alefba2.ir` - Helm charts و Kubernetes manifests در این repository هستند
- **احراز هویت Registry**: `admin:<pass>`
- **احراز هویت Nexus**: `k8s-reader:<Token>`

### Baseline نسخه‌ها (بر اساس موجودی Registry در تاریخ 2026-02-10)

> این راهنما طوری version-pinning شده که **با موجودی فعلی رجیستری شما** هم‌خوان باشد. اگر بعداً موجودی تغییر کرد،
> این بخش را هم به‌روزرسانی کنید.

- **Kubernetes images (kubeadm)**: `v1.29.7` (repo: `rr.alefba2.ir/k8s`)
- **pause**: `rr.alefba2.ir/k8s/pause:3.10`
- **Calico/Tigera**: `tigera/operator:v1.40.3` + `quay/calico/*:v3.31.3` (در موجودی شما موجود است)
- **Ingress NGINX**: `rr.alefba2.ir/ingress-nginx/controller:v1.10.1`
- **Metrics Server**: `rr.alefba2.ir/k8s/metrics-server:v0.8.1`
- **CockroachDB**: `rr.alefba2.ir/cockroachdb/cockroach:v24.3.25`
- **Redis**: `rr.alefba2.ir/library/redis:8.4.0`
- **ClickHouse**: `rr.alefba2.ir/clickhouse/clickhouse-operator:0.26.0` +
  `rr.alefba2.ir/clickhouse/clickhouse-server:25.12.5`
- **Redpanda**: `rr.alefba2.ir/redpandadata/redpanda:v25.3.6`
- **Strimzi**: `rr.alefba2.ir/strimzi/operator:0.50.0` + `rr.alefba2.ir/strimzi/kafka:0.50.0-kafka-4.1.1`
- **Keycloak**: `rr.alefba2.ir/keycloak/keycloak:26.5.2`
- **Velero**: `rr.alefba2.ir/velero/velero:v1.17.2` + `rr.alefba2.ir/velero/velero-plugin-for-aws:v1.13.0`

### راهنمای خواندن دستورات

در تمام دستورات، مشخص شده که:

- **روی Control Plane (k8s-cp-01)**: برای دستورات kubectl و مدیریت cluster
- **روی Worker Nodes (k8s-worker-01, k8s-worker-02)**: برای join کردن به cluster
- **روی Collaboration Node (k8s-collab-01)**: برای Jira, Confluence, Nextcloud
- **روی Registry Node (registry)**: برای مدیریت Registry و Nexus

### استفاده از Registry و Nexus

**مهم:** تمام images، manifests و charts باید از registry و Nexus محلی استفاده شوند. هیچ image یا manifest مستقیم از
اینترنت استفاده نمی‌شود.

---

## 0. تنظیمات اولیه Registry و Nexus

**⚠ مهم**: این بخش باید قبل از نصب Kubernetes انجام شود.

### 0.1. پیکربندی containerd برای استفاده از Registry محلی

**روی همه Kubernetes nodes (k8s-cp-01, k8s-worker-01, k8s-worker-02, k8s-collab-01):**

```bash
# ایجاد دایرکتوری برای registry config
sudo mkdir -p /etc/containerd/certs.d/rr.alefba2.ir

# ایجاد فایل hosts.toml
cat > /tmp/hosts.toml <<EOF
server = "https://rr.alefba2.ir"

[host."https://rr.alefba2.ir"]
  capabilities = ["pull", "resolve"]
  skip_verify = true
  [host."https://rr.alefba2.ir".auth]
    username = "admin"
    password = "<pass>"
EOF

sudo mv /tmp/hosts.toml /etc/containerd/certs.d/rr.alefba2.ir/hosts.toml

# Restart containerd
sudo systemctl restart containerd
sudo systemctl enable containerd
```

### 0.2. تست اتصال به Registry

```bash
# روی هر Kubernetes node
# تست pull image
sudo ctr images pull --user 'admin:<pass>' rr.alefba2.ir/k8s/pause:3.10

# بررسی image
sudo ctr images list | grep rr.alefba2.ir
```

### 0.3. پیکربندی Helm برای استفاده از Nexus

**روی Control Plane یا Management Node:**

```bash
# اضافه کردن Nexus Helm repository
helm repo add my-nexus https://mn.alefba2.ir/repository/helm-charts/ \
  --username k8s-reader \
  --password '<Token>'

# Update repositories
helm repo update

# بررسی charts موجود
helm search repo my-nexus
```

---

## 1. پیش‌نیازها و آماده‌سازی

### 1.1. الزامات سخت‌افزاری

#### سرور فیزیکی 1

- **RAM**: 64GB
- **CPU**: حداقل 8 cores (16 threads توصیه می‌شود)
- **Storage**: حداقل 1TB SSD (برای OS و VM storage)
- **Network**: حداقل 2x 1Gbps NIC (10Gbps توصیه می‌شود)
- **iDRAC/iLO**: برای مدیریت از راه دور

#### سرور فیزیکی 2

- **RAM**: 64GB
- **CPU**: حداقل 8 cores (16 threads توصیه می‌شود)
- **Storage**: حداقل 1TB SSD (برای OS و VM storage)
- **Network**: حداقل 2x 1Gbps NIC (10Gbps توصیه می‌شود)
- **iDRAC/iLO**: برای مدیریت از راه دور

### 1.2. الزامات نرم‌افزاری

- **VMware ESXi 8.0**: مجازی‌سازی
- **Rocky Linux 10**: سیستم عامل پایه
- **Kubernetes**: نسخه `v1.29.7` (پیشنهادی بر اساس موجودی رجیستری)
- **Container Runtime**: containerd یا CRI-O
- **CNI Plugin**: Calico یا Flannel
- **Helm**: نسخه 3.12+

### 1.3. الزامات شبکه

- **Network Connectivity**: اتصال پایدار بین دو سرور
- **DNS**: DNS server برای name resolution
- **Load Balancer**: MetalLB یا external load balancer
- **VPN Gateway**: برای دسترسی امن از راه دور

### 1.4. آماده‌سازی اولیه

#### 1.4.1. تنظیمات BIOS/UEFI

```bash
# فعال‌سازی Virtualization
- Intel VT-x / AMD-V: Enabled
- Hyper-Threading: Enabled
- NUMA: Enabled (در صورت پشتیبانی)
```

#### 1.4.2. تنظیمات iDRAC/iLO

```bash
# تنظیم IP Static برای iDRAC/iLO
- IP Address: 192.168.10.10 (Server-55)
- IP Address: 192.168.10.11 (Server-50)
- Subnet Mask: 255.255.255.0
- Gateway: 192.168.10.1
- DNS: 8.8.8.8, 8.8.4.4
```

---

## 2. نصب و راه‌اندازی VMware ESXi 8

### 2.1. نصب ESXi از راه دور

#### 2.1.1. دسترسی به iDRAC/iLO

1. اتصال به iDRAC/iLO از طریق مرورگر: `https://192.168.10.10` (Server-55) یا `https://192.168.10.11` (Server-50)
2. Login با credentials
3. دسترسی به Remote Console (KVM over IP)

#### 2.1.2. Mount ISO ESXi

1. در iDRAC/iLO، به بخش **Virtual Media** بروید
2. **Mount ISO** را انتخاب کنید
3. ISO VMware ESXi 8.0 را mount کنید

#### 2.1.3. Boot از ISO

1. در Remote Console، VM را **Power On** کنید
2. Boot از Virtual Media را انتخاب کنید
3. نصب ESXi را شروع کنید

#### 2.1.4. نصب ESXi

```bash
# مراحل نصب ESXi
1. انتخاب Keyboard Layout
2. تایید License Agreement
3. انتخاب Disk برای نصب
4. تنظیم Root Password
5. تنظیم Network Configuration:
   - IP Address: 192.168.10.20 (Server-55)
   - IP Address: 192.168.10.21 (Server-50)
   - Subnet Mask: 255.255.255.0
   - Gateway: 192.168.10.1
   - DNS: 8.8.8.8, 8.8.4.4
6. تایید و شروع نصب
```

### 2.2. تنظیمات اولیه ESXi

#### 2.2.1. دسترسی به ESXi

```bash
# دسترسی از طریق vSphere Client یا Web Client
URL: https://192.168.10.20 (Server-55)
URL: https://192.168.10.21 (Server-50)
Username: root
Password: [password set during installation]
```

#### 2.2.2. تنظیمات Storage

```bash
# در vSphere Client
1. به بخش Storage بروید
2. Datastore جدید ایجاد کنید
3. نام: datastore1
4. Type: VMFS 6
```

#### 2.2.3. تنظیمات Network

```bash
# در vSphere Client
1. به بخش Networking بروید
2. Virtual Switch ایجاد کنید:
   - Name: vSwitch0
   - Type: Standard Switch
3. Port Group ایجاد کنید:
   - Name: VM Network
   - VLAN ID: (در صورت نیاز)
```

---

## 3. نصب Rocky Linux 10 روی VMها

### 3.1. ایجاد VM Template

#### 3.1.1. ایجاد VM برای Template

```bash
# در vSphere Client
1. Right-click روی ESXi Host
2. New Virtual Machine
3. Configuration:
   - Name: rocky-linux-10-template
   - Compatibility: ESXi 8.0
   - Guest OS: Linux
   - Version: Red Hat Enterprise Linux 10 (64-bit)
4. Storage:
   - Datastore: datastore1
   - Disk: 50GB (Thin Provision)
5. Network:
   - Adapter: VMXNET3
   - Network: VM Network
6. CPU: 2 vCPU
7. Memory: 4GB RAM
```

#### 3.1.2. نصب Rocky Linux 10

```bash
# Mount ISO Rocky Linux 10
1. در vSphere Client، VM را انتخاب کنید
2. به بخش CD/DVD بروید
3. ISO Rocky Linux 10 را mount کنید
4. VM را Power On کنید
5. Boot از CD/DVD را انتخاب کنید
```

#### 3.1.3. نصب OS

```bash
# مراحل نصب Rocky Linux 10
1. انتخاب Language: English (یا Persian)
2. Installation Summary:
   - Keyboard: English (US)
   - Language Support: English, Persian
   - Time & Date: Asia/Tehran
   - Installation Source: Local media
   - Software Selection: Minimal Install (یا Server)
   - Installation Destination: 
     - Automatic partitioning (یا Custom)
     - /boot: 1GB
     - /: باقی فضا
     - Swap: 4GB (در صورت نیاز)
3. Network & Host Name:
   - Hostname: rocky-linux-10-template
   - Network: Enable
   - IPv4 Settings: Manual
     - Address: 192.168.10.100
     - Netmask: 255.255.255.0
     - Gateway: 192.168.10.1
     - DNS: 8.8.8.8, 8.8.4.4
4. Root Password: تنظیم password قوی
5. User Creation: ایجاد user با sudo access
6. شروع نصب
```

#### 3.1.4. تنظیمات پس از نصب

```bash
# Login به VM
ssh root@192.168.10.100

# Update system
dnf update -y

# نصب ابزارهای پایه
dnf install -y vim git curl wget net-tools htop

# تنظیمات Firewall
firewall-cmd --permanent --add-service=ssh
firewall-cmd --reload

# تنظیمات SELinux (در صورت نیاز)
# setenforce 0  # برای testing
# یا تنظیم SELinux به permissive mode
```

#### 3.1.5. ایجاد Template

```bash
# در vSphere Client
1. VM را Shutdown کنید
2. Right-click روی VM
3. Template > Convert to Template
4. نام: rocky-linux-10-template
```

### 3.2. ایجاد VMها از Template

**⚠ مهم:** طبق ساختار جدید
در [New-Proposal-Kubernates-Enterprise-Architecure](New-Proposal-Kubernates-Enterprise-Architecure)، IP addresses باید
در محدوده `192.168.10.151-199` باشند.

#### 3.2.1. VM Control Plane (k8s-cp-01) - Server-55

```bash
# در vSphere Client
1. Right-click روی Template
2. Deploy Virtual Machine from Template
3. Configuration:
   - Name: k8s-cp-01
   - Location: Server-55 ESXi
   - CPU: 8 vCPU
   - Memory: 16GB RAM
   - Disk: 200GB
4. Customize:
   - Hostname: k8s-cp-01
   - IP Address: 192.168.10.151
   - Netmask: 255.255.255.0
   - Gateway: 192.168.10.1
   - DNS: 8.8.8.8, 8.8.4.4
5. Power On VM
```

#### 3.2.2. VM Worker Node 1 (k8s-worker-01) - Server-55

```bash
# در vSphere Client
1. Right-click روی Template
2. Deploy Virtual Machine from Template
3. Configuration:
   - Name: k8s-worker-01
   - Location: Server-55 ESXi
   - CPU: 16 vCPU
   - Memory: 32GB RAM
   - Disk: 800GB
4. Customize:
   - Hostname: k8s-worker-01
   - IP Address: 192.168.10.152
   - Netmask: 255.255.255.0
   - Gateway: 192.168.10.1
   - DNS: 8.8.8.8, 8.8.4.4
5. Power On VM
```

#### 3.2.3. VM Worker Node 2 (k8s-worker-02) - Server-50

```bash
# در vSphere Client
1. Right-click روی Template
2. Deploy Virtual Machine from Template
3. Configuration:
   - Name: k8s-worker-02
   - Location: Server-50 ESXi
   - CPU: 16 vCPU
   - Memory: 32GB RAM
   - Disk: 800GB
4. Customize:
   - Hostname: k8s-worker-02
   - IP Address: 192.168.10.153
   - Netmask: 255.255.255.0
   - Gateway: 192.168.10.1
   - DNS: 8.8.8.8, 8.8.4.4
5. Power On VM
```

#### 3.2.4. VM Collaboration Node (k8s-collab-01) - Server-50

```bash
# در vSphere Client
1. Right-click روی Template
2. Deploy Virtual Machine from Template
3. Configuration:
   - Name: k8s-collab-01
   - Location: Server-50 ESXi
   - CPU: 12 vCPU
   - Memory: 24GB RAM
   - Disk: 700GB
4. Customize:
   - Hostname: k8s-collab-01
   - IP Address: 192.168.10.154
   - Netmask: 255.255.255.0
   - Gateway: 192.168.10.1
   - DNS: 8.8.8.8, 8.8.4.4
5. Power On VM
```

#### 3.2.5. VM Monitoring Node (monitoring) - Server-50

```bash
# در vSphere Client
1. Right-click روی Template
2. Deploy Virtual Machine from Template
3. Configuration:
   - Name: monitoring
   - Location: Server-50 ESXi
   - CPU: 8 vCPU
   - Memory: 16GB RAM
   - Disk: 600GB
4. Customize:
   - Hostname: monitoring
   - IP Address: 192.168.10.155
   - Netmask: 255.255.255.0
   - Gateway: 192.168.10.1
   - DNS: 8.8.8.8, 8.8.4.4
5. Power On VM
```

#### 3.2.6. VM Registry Node (registry) - Server-50

```bash
# در vSphere Client
1. Right-click روی Template
2. Deploy Virtual Machine from Template
3. Configuration:
   - Name: registry
   - Location: Server-50 ESXi
   - CPU: 8 vCPU
   - Memory: 16GB RAM
   - Disk: 500GB+
4. Customize:
   - Hostname: registry
   - IP Address: 192.168.10.160
   - Netmask: 255.255.255.0
   - Gateway: 192.168.10.1
   - DNS: 8.8.8.8, 8.8.4.4
5. Power On VM
```

---

## 4. راه‌اندازی Kubernetes Cluster

### 4.1. تنظیمات اولیه (همه Nodes)

#### 4.1.1. غیرفعال کردن Swap

```bash
# روی همه Nodes
proxychains sudo dnf update -y
sudo reboot

sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

#### 4.1.2. تنظیمات Kernel

```bash
# روی همه Nodes
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```

#### 4.1.3. تنظیمات Firewall

```bash
# روی همه Nodes
sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --permanent --add-port=2379-2380/tcp
sudo firewall-cmd --permanent --add-port=10250/tcp
sudo firewall-cmd --permanent --add-port=10251/tcp
sudo firewall-cmd --permanent --add-port=10252/tcp
sudo firewall-cmd --permanent --add-port=10255/tcp
sudo firewall-cmd --permanent --add-port=30000-32767/tcp
sudo firewall-cmd --reload


sudo nft flush ruleset

sudo nft add table inet k8s
sudo nft add chain inet k8s input { type filter hook input priority 0 \; policy accept \; }
sudo nft add chain inet k8s forward { type filter hook forward priority 0 \; policy accept \; }
sudo nft add chain inet k8s output { type filter hook output priority 0 \; policy accept \; }

sudo nft add rule inet k8s input iif lo accept

sudo nft add rule inet k8s input ct state established,related accept
sudo nft add rule inet k8s forward ct state established,related accept
sudo nft add rule inet k8s output ct state established,related accept

sudo nft add rule inet k8s input tcp dport 22 accept

sudo nft add rule inet k8s input tcp dport 9090 accept

sudo nft add rule inet k8s input ip daddr 10.96.0.1 tcp dport 443 accept
sudo nft add rule inet k8s output ip saddr 10.96.0.1 tcp sport 443 accept

sudo nft add rule inet k8s input udp dport 53 accept
sudo nft add rule inet k8s output udp sport 53 accept

sudo nft add rule inet k8s input tcp dport 179 accept

sudo nft add rule inet k8s input tcp dport 10250 accept

sudo nft add rule inet k8s input tcp dport 30000-32767 accept
sudo nft add rule inet k8s input udp dport 30000-32767 accept

sudo nft add rule inet k8s input udp dport 4789 accept

sudo nft add rule inet k8s input tcp dport 5473 accept

sudo nft add rule inet k8s input ip saddr 192.168.10.0/24 accept
sudo nft add rule inet k8s forward ip saddr 192.168.10.0/24 accept
sudo nft add rule inet k8s output ip daddr 192.168.10.0/24 accept

sudo nft chain inet k8s input { policy drop \; }
sudo nft chain inet k8s forward { policy drop \; }
sudo nft chain inet k8s output { policy accept \; }

sudo nft list ruleset | sudo tee /etc/nftables.conf > /dev/null
sudo systemctl enable nftables
sudo systemctl restart nftables

```

### 4.2. نصب Container Runtime (containerd)

#### 4.2.1. نصب containerd

```bash
# روی همه Kubernetes Nodes (k8s-cp-01, k8s-worker-01, k8s-worker-02, k8s-collab-01)
# اضافه کردن Docker repository
#sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
#sudo dnf install -y containerd.io

sudo dnf remove containerd -y
curl -LO https://github.com/containerd/containerd/releases/download/v1.7.30/containerd-1.7.30-linux-amd64.tar.gz
sudo tar -C /usr/local -xzf containerd-1.7.30-linux-amd64.tar.gz
sudo nano /etc/systemd/system/containerd.service

[Unit]
Description=containerd container runtime
Documentation=https://containerd.io
After=network.target

[Service]
ExecStart=/usr/local/bin/containerd
Type=notify
Delegate=yes
KillMode=process
Restart=always
RestartSec=5
LimitNOFILE=1048576
LimitNPROC=infinity
LimitCORE=infinity

[Install]
WantedBy=multi-user.target


sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

sudo systemctl daemon-reload
sudo systemctl enable --now containerd
sudo systemctl status containerd
sudo crictl info


# ⚠ اگر کلاستر شما air-gapped است، این repo باید از طریق Nexus/YUM mirror داخلی تامین شود.

#sudo mkdir -p /etc/containerd
#containerd config default | sudo tee /etc/containerd/config.toml

# تنظیم SystemdCgroup
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl enable containerd


# Download the latest stable runc binary (v1.1.12)
wget https://github.com/opencontainers/runc/releases/download/v1.1.12/runc.amd64

# Install it to /usr/local/sbin
sudo install -m 755 runc.amd64 /usr/local/sbin/runc

# Verify installation
which runc
runc --version
```

### 4.3. نصب kubeadm, kubelet, kubectl

#### 4.3.1. اضافه کردن Kubernetes Repository

```bash
# روی همه Kubernetes Nodes (k8s-cp-01, k8s-worker-01, k8s-worker-02, k8s-collab-01)
# اضافه کردن Kubernetes repository
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
EOF

proxychains sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo systemctl enable --now kubelet

```

### 4.4. Initialize Control Plane Node

#### 4.4.1. Initialize Cluster

**⚠ مهم**: قبل از initialize، باید containerd را برای استفاده از registry محلی پیکربندی کرده باشید (بخش 0.1).

**استفاده از Registry محلی (rr.alefba2.ir):**

```bash
# روی Control Plane Node (k8s-cp-01)
# بررسی اتصال به registry
sudo ctr images pull --user 'admin:<pass>' rr.alefba2.ir/k8s/pause:3.10

# Initialize cluster با استفاده از registry محلی
sudo kubeadm init \
  --pod-network-cidr=192.168.0.0/16 \
  --apiserver-advertise-address=192.168.10.151 \
  --control-plane-endpoint=192.168.10.151:6443 \
  --image-repository=rr.alefba2.ir/k8s \
  --kubernetes-version=v1.29.7 \
  --cri-socket=unix:///var/run/containerd/containerd.sock

# خروجی شامل join command برای worker nodes است
# این command را ذخیره کنید
# مثال:
# kubeadm join 192.168.10.151:6443 --token <token> \
#   --discovery-token-ca-cert-hash sha256:<hash>
```

#### 4.4.2. تنظیم kubeconfig

```bash
# روی Control Plane Node (k8s-cp-01)
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# بررسی
kubectl get nodes
# باید Control Plane Node را با status NotReady ببینید (تا CNI plugin نصب نشود)
```

### 4.5. Join Worker Nodes

#### 4.5.1. Join Worker Node 1

```bash
# روی Worker Node 1 (k8s-worker-01)
# اطمینان از پیکربندی containerd برای registry (بخش 0.1)

# از join command که از Control Plane دریافت کردید استفاده کنید
sudo kubeadm join 192.168.10.151:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

#### 4.5.2. Join Worker Node 2

```bash
# روی Worker Node 2 (k8s-worker-02)
# اطمینان از پیکربندی containerd برای registry (بخش 0.1)

# از join command که از Control Plane دریافت کردید استفاده کنید
sudo kubeadm join 192.168.10.151:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

#### 4.5.3. Join Collaboration Node

```bash
# روی Collaboration Node (k8s-collab-01)
# اطمینان از پیکربندی containerd برای registry (بخش 0.1)

# از join command که از Control Plane دریافت کردید استفاده کنید
sudo kubeadm join 192.168.10.151:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>

# بعد از join، label و taint اضافه کنید
# (این کار بعد از نصب CNI انجام می‌شود)
```

#### 4.5.4. بررسی Nodes

```bash
# روی Control Plane Node (k8s-cp-01)
kubectl get nodes
# باید همه nodes را ببینید (هنوز NotReady هستند تا CNI plugin نصب شود)
```

---

## 5. نصب CNI Plugin و Networking

### 5.1. نصب Calico CNI (با Network Policy) ⭐ توصیه می‌شود

**⚠ مهم**: Calico images باید در registry محلی (`rr.alefba2.ir`) موجود باشند. برای لیست کامل images
به [Complete-Images-Manifests-Helm-Charts-List](Complete-Images-Manifests-Helm-Charts-List) مراجعه کنید.

#### 5.1.1. نصب Calico با Helm (از Nexus)

```bash
# روی Control Plane Node (k8s-cp-01)
# اطمینان از پیکربندی Helm برای Nexus (بخش 0.3)

# نصب Calico از Nexus
helm install calico my-nexus/tigera-operator \
  --namespace tigera-operator \
  --create-namespace \
  --set installation.registry=rr.alefba2.ir \
  --set installation.imagePath=quay \
  --set installation.imagePrefix=calico \
  --set installation.calicoNetwork.ipPools[0].cidr=192.168.0.0/16


# یا اگر chart در Nexus نیست، از منبع اصلی pull کنید و به Nexus push کنید
# (به Complete-Images-Manifests-Helm-Charts-List مراجعه کنید)
```

#### 5.1.2. نصب Calico با Manifest (از Nexus)

```bash
# روی Control Plane Node (k8s-cp-01)
# دانلود manifest از Nexus
curl -u k8s-reader \
  https://mn.alefba2.ir/repository/k8s-manifests/networking/calico/tigera-operator.yaml \
  -o tigera-operator.yaml

curl -u k8s-reader \
  https://mn.alefba2.ir/repository/k8s-manifests/networking/calico/custom-resources.yaml \
  -o custom-resources.yaml
  
curl -u k8s-reader \
  https://mn.alefba2.ir/repository/k8s-manifests/networking/calico/operator-crds.yaml \
  -o operator-crds.yaml

# ویرایش manifests برای استفاده از registry محلی
# (اگر image references در manifest هستند، باید به rr.alefba2.ir تغییر یابند)

# نصب Calico
kubectl create -f tigera-operator.yaml
kubectl create -f custom-resources.yaml
```

#### 5.1.3. بررسی Status

```bash
# روی Control Plane Node (k8s-cp-01)
kubectl get pods -n calico-system
# باید همه pods Running باشند

kubectl get pods -n tigera-operator
# باید operator running باشد

kubectl get nodes
# باید همه nodes Ready باشند
```

#### 5.1.4. Label و Taint برای Collaboration Node

```bash
# روی Control Plane Node (k8s-cp-01)
# بعد از نصب CNI و Ready شدن nodes

# Label برای Collaboration Node
kubectl label node k8s-collab-01 node-role.kubernetes.io/collab=true

# Taint برای Collaboration Node (اختیاری - برای isolation)
kubectl taint node k8s-collab-01 collab=true:NoSchedule
```

---

## 6. نصب Ingress Controller

### 6.1. نصب Nginx Ingress Controller

**⚠ مهم**: Ingress NGINX images باید در registry محلی (`rr.alefba2.ir`) موجود باشند.

#### 6.1.1. نصب با Helm از Nexus (توصیه می‌شود)

```bash
# روی Control Plane Node (k8s-cp-01)
# اطمینان از پیکربندی Helm برای Nexus (بخش 0.3)

# نصب Ingress NGINX از Nexus
helm install ingress-nginx my-nexus/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.image.registry=rr.alefba2.ir \
  --set controller.image.image=ingress-nginx/controller \
  --set controller.image.tag=v1.10.0 \
  --set controller.image.digest="" \
  --set controller.admissionWebhooks.patch.image.registry=rr.alefba2.ir \
  --set controller.admissionWebhooks.patch.image.image=ingress-nginx/kube-webhook-certgen \
  --set controller.admissionWebhooks.patch.image.tag=v1.4.0 \
  --set controller.admissionWebhooks.patch.image.digest="" \
  --set controller.service.type=NodePort

# یا اگر chart در Nexus نیست، از منبع اصلی pull کنید و به Nexus push کنید
```

#### 6.1.2. بررسی Status

```bash
# روی Control Plane Node (k8s-cp-01)
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

---

## 7. راه‌اندازی Monitoring Stack

### 7.1. نصب Helm

#### 7.1.1. نصب Helm روی Control Plane Node

```bash
# روی Control Plane Node (k8s-cp-01)
# دانلود Helm
curl -L https://get.helm.sh/helm-v3.15.3-linux-amd64.tar.gz -o helm.tar.gz
tar -xzf helm.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
rm -rf linux-amd64 helm.tar.gz

helm version
```

**⚠ نکته air-gapped:** اگر اینترنت ندارید، فایل `helm-v3.15.3-linux-amd64.tar.gz` را در Nexus (raw repository) نگه دارید
و از همانجا دانلود کنید.

#### 7.1.2. پیکربندی Helm برای استفاده از Nexus

```bash
# روی Control Plane Node (k8s-cp-01)
# اضافه کردن Nexus Helm repository (بخش 0.3)
helm repo add my-nexus https://mn.alefba2.ir/repository/helm-charts/ \
  --username k8s-reader \
  --password '<Token>'

helm repo update
```

### 7.2. نصب Metrics Server

#### 7.2.1. نصب Metrics Server از Nexus

```bash
# روی Control Plane Node (k8s-cp-01)
# دانلود manifest از Nexus
curl -u k8s-reader \
  https://mn.alefba2.ir/repository/k8s-manifests/core/metrics-server.yaml \
  -o metrics-server.yaml

# بررسی و ویرایش image reference در manifest (اگر نیاز باشد)
# مثال (پیشنهادی بر اساس موجودی شما):
# sed -i 's|registry.k8s.io/metrics-server/metrics-server:.*|rr.alefba2.ir/k8s/metrics-server:v0.8.1|g' metrics-server.yaml

# نصب Metrics Server
kubectl apply -f metrics-server.yaml
```

#### 7.2.2. بررسی Status

```bash
# روی Control Plane Node (k8s-cp-01)
kubectl get pods -n kube-system | grep metrics-server
kubectl top nodes
```

### 7.3. نصب Prometheus Stack (اختیاری - بعد از Infrastructure Tools)

**⚠ توجه**: این بخش را بعد از نصب Jira, Confluence, Nextcloud انجام دهید.

#### 7.3.1. نصب Prometheus Stack از Nexus

```bash
# روی Control Plane Node (k8s-cp-01)
# نصب Prometheus Stack از Nexus
helm install prometheus my-nexus/kube-prometheus-stack \
  --version 82.1.0 \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set grafana.adminPassword=admin \
  --set prometheus.service.type=NodePort \
  --set prometheus.service.nodePort=30090 \
  --set grafana.service.type=NodePort \
  --set grafana.service.nodePort=30091 \
  --set global.imageRegistry=rr.alefba2.ir \
 --set prometheus.image.registry=rr.alefba2.ir \
 --set grafana.image.registry=rr.alefba2.ir \
 --set prometheus.image.registry=rr.alefba2.ir \
 --set grafana.image.registry=rr.alefba2.ir
# یا تنظیم image registry برای هر component
```

#### 7.3.2. بررسی Status

```bash
# روی Control Plane Node (k8s-cp-01)
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

#### 7.3.3. دسترسی به Grafana

```bash
# روی Control Plane Node (k8s-cp-01)
# Port forward
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# یا از طریق NodePort
# http://192.168.10.151:30091
# Username: admin
# Password: admin
```

---

## 8. Deploy Backend Services

### 8.1. ایجاد Namespaces

#### 8.1.1. ایجاد Namespaces برای Environments

```bash
# روی Master Node (سرور ایران)
kubectl create namespace dev
kubectl create namespace stage
kubectl create namespace production
kubectl create namespace infrastructure
```

### 8.2. Deploy Infrastructure Service

#### 8.2.1. ایجاد ConfigMap

```bash
# روی Master Node (سرور ایران)
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: infrastructure-config
  namespace: production
data:
  database_url: "jdbc:postgresql://cockroachdb.production.svc.cluster.local:26257/app_db"
  log_level: "INFO"
  spring_profiles_active: "production"
EOF
```

#### 8.2.2. ایجاد Secret

```bash
# روی Master Node
kubectl create secret generic infrastructure-secrets \
  --namespace=production \
  --from-literal=database_password='your-secure-password' \
  --from-literal=jwt_secret='your-jwt-secret'
```

#### 8.2.3. ایجاد Deployment

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: infrastructure-service
  namespace: production
  labels:
    app: infrastructure-service
    env: production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: infrastructure-service
  template:
    metadata:
      labels:
        app: infrastructure-service
        env: production
    spec:
      containers:
        - name: infrastructure-service
          image: rr.alefba2.ir/my-app/infrastructure-service:v1.0.0
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              name: http
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                configMapKeyRef:
                  name: infrastructure-config
                  key: database_url
            - name: DATABASE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: infrastructure-secrets
                  key: database_password
          resources:
            requests:
              cpu: 1000m
              memory: 1Gi
            limits:
              cpu: 2000m
              memory: 2Gi
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
            timeoutSeconds: 3
            failureThreshold: 30
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - infrastructure-service
                topologyKey: kubernetes.io/hostname
EOF
```

#### 8.2.4. ایجاد Service

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: infrastructure-service
  namespace: production
spec:
  selector:
    app: infrastructure-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
EOF
```

#### 8.2.5. ایجاد HPA (Horizontal Pod Autoscaler)

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: infrastructure-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: infrastructure-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 2
          periodSeconds: 15
      selectPolicy: Max
EOF
```

### 8.3. Deploy سایر Backend Services

#### 8.3.1. استفاده از Helm Charts (توصیه می‌شود)

```bash
# روی Management Node
# ایجاد Helm Chart برای هر service
helm create infrastructure-service
helm create workflow-service
helm create report-manager-service
# ... و غیره

# Deploy با Helm
helm install infrastructure-service ./infrastructure-service \
  --namespace production \
  --set image.tag=v1.0.0 \
  --set replicaCount=3
```

---

## 9. Deploy Frontend Services

### 9.1. Deploy Frontend (React)

#### 9.1.1. ایجاد Deployment

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: production
  labels:
    app: frontend
    env: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        env: production
    spec:
      containers:
        - name: frontend
          image: rr.alefba2.ir/my-app/frontend:v1.0.0
          ports:
            - containerPort: 80
              name: http
          env:
            - name: API_URL
              value: "http://gateway-ui.production.svc.cluster.local"
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 10
            periodSeconds: 5
EOF
```

#### 9.1.2. ایجاد Service

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: production
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
EOF
```

---

## 10. Deploy Databases

### 10.1. Deploy CockroachDB

#### 10.1.1. ایجاد StatefulSet

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: cockroachdb-public
  namespace: production
  labels:
    app: cockroachdb
spec:
  ports:
    - port: 26257
      targetPort: 26257
      name: grpc
    - port: 8080
      targetPort: 8080
      name: http
  clusterIP: None
  selector:
    app: cockroachdb
---
apiVersion: v1
kind: Service
metadata:
  name: cockroachdb
  namespace: production
  labels:
    app: cockroachdb
spec:
  ports:
    - port: 26257
      targetPort: 26257
      name: grpc
  selector:
    app: cockroachdb
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cockroachdb
  namespace: production
spec:
  serviceName: cockroachdb-public
  replicas: 3
  selector:
    matchLabels:
      app: cockroachdb
  template:
    metadata:
      labels:
        app: cockroachdb
    spec:
      containers:
        - name: cockroachdb
          image: rr.alefba2.ir/cockroachdb/cockroach:v24.3.25
          ports:
            - containerPort: 26257
              name: grpc
            - containerPort: 8080
              name: http
          command:
            - /cockroach/cockroach
            - start
            - --join
            - cockroachdb-public
            - --advertise-addr
            - \$(hostname).cockroachdb-public
            - --http-addr
            - 0.0.0.0
            - --cache
            - 25%
            - --max-sql-memory
            - 25%
          resources:
            requests:
              cpu: 2000m
              memory: 4Gi
            limits:
              cpu: 4000m
              memory: 8Gi
          volumeMounts:
            - name: datadir
              mountPath: /cockroach/cockroach-data
          livenessProbe:
            httpGet:
              path: /health?ready=1
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          readinessProbe:
            httpGet:
              path: /health?ready=1
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
  volumeClaimTemplates:
    - metadata:
        name: datadir
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 100Gi
        storageClassName: standard
EOF
```

### 10.2. Deploy ClickHouse

#### 10.2.1. استفاده از Helm Chart

```bash
# روی Management Node
# ⚠ air-gapped: chart باید داخل Nexus باشد
# helm search repo my-nexus | grep -i clickhouse

# نصب ClickHouse Operator از Nexus + استفاده از images رجیستری محلی
# (کلیدهای دقیق values ممکن است بسته به chart شما متفاوت باشد؛ در صورت نیاز values.yaml را تنظیم کنید)
helm install clickhouse-operator my-nexus/clickhouse-operator \
  --namespace production \
  --create-namespace \
  --set operator.image.registry=rr.alefba2.ir \
  --set operator.image.repository=clickhouse/clickhouse-operator \
  --set operator.image.tag=0.26.0 \
  --set clickhouse.image.registry=rr.alefba2.ir \
  --set clickhouse.image.repository=clickhouse/clickhouse-server \
  --set clickhouse.image.tag=25.12.5
```

### 10.3. Deploy Redis

#### 10.3.1. ایجاد Deployment

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: rr.alefba2.ir/library/redis:8.4.0
          ports:
            - containerPort: 6379
              name: redis
          command:
            - redis-server
            - --appendonly yes
            - --requirepass \$(REDIS_PASSWORD)
          env:
            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: redis-secrets
                  key: password
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 2Gi
          volumeMounts:
            - name: redis-data
              mountPath: /data
      volumes:
        - name: redis-data
          persistentVolumeClaim:
            claimName: redis-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: production
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
  type: ClusterIP
EOF
```

---

## 11. Deploy Messaging (Kafka/Redpanda)

### 11.1. Deploy Redpanda (توصیه می‌شود)

#### 11.1.1. استفاده از Helm Chart

```bash
# روی Management Node
# ⚠ air-gapped: chart باید داخل Nexus باشد
# helm search repo my-nexus | grep -i redpanda

helm install redpanda my-nexus/redpanda \
  --namespace production \
  --create-namespace \
  --set statefulset.replicas=3 \
  --set storage.size=200Gi \
  --set image.registry=rr.alefba2.ir \
  --set image.repository=redpandadata/redpanda \
  --set image.tag=v25.3.6
```

### 11.2. Deploy Kafka (جایگزین)

#### 11.2.1. استفاده از Strimzi Operator

```bash
# روی Master Node
kubectl create namespace kafka

# ⚠ air-gapped: manifest نصب Strimzi باید از Nexus خوانده شود (نه اینترنت)
curl -u k8s-reader \
  https://mn.alefba2.ir/repository/k8s-manifests/messaging/strimzi/strimzi-install.yaml \
  -o strimzi-install.yaml

# مطمئن شوید image ها به رجیستری محلی اشاره می‌کنند:
# - rr.alefba2.ir/strimzi/operator:0.50.0
# - rr.alefba2.ir/strimzi/kafka:0.50.0-kafka-4.1.1

kubectl apply -f strimzi-install.yaml -n kafka

# ایجاد Kafka Cluster
cat <<EOF | kubectl apply -f -
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: production
spec:
  kafka:
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 200Gi
          deleteClaim: false
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 100Gi
      deleteClaim: false
EOF
```

---

## 12. راه‌اندازی Infrastructure Tools (اولویت: Jira, Confluence, Nextcloud)

**⚠ مهم**: این بخش با اولویت نصب Jira, Confluence و Nextcloud انجام می‌شود. تمام این سرویس‌ها باید روی Collaboration
Node (`k8s-collab-01`) deploy شوند.

### 12.1. ایجاد Namespace و تنظیمات اولیه

```bash
# روی Control Plane Node (k8s-cp-01)
# ایجاد namespace برای Infrastructure Tools
kubectl create namespace infrastructure

# ایجاد ResourceQuota برای namespace
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: infrastructure-quota
  namespace: infrastructure
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    persistentvolumeclaims: "10"
EOF
```

### 12.2. Deploy Jira Data Center (اولویت 1)

**⚠ مهم**: Jira images باید در registry محلی (`rr.alefba2.ir`) موجود باشند.

#### 12.2.1. نصب Jira از Nexus

```bash
# روی Control Plane Node (k8s-cp-01)
# نصب Jira از Nexus
helm install jira my-nexus/jira \
  --namespace infrastructure \
  --set image.registry=rr.alefba2.ir \
  --set image.repository=atlassian/jira-software \
  --set image.tag=9.12.0 \
  --set replicaCount=1 \
  --set nodeSelector."node-role\.kubernetes\.io/collab"=true \
  --set tolerations[0].key=collab \
  --set tolerations[0].operator=Equal \
  --set tolerations[0].value="true" \
  --set tolerations[0].effect=NoSchedule \
  --set persistence.size=200Gi \
  --set service.type=ClusterIP \
  --set ingress.enabled=true \
  --set ingress.hostname=jira.alefba2.ir \
  --set ingress.tls[0].hosts[0]=jira.alefba2.ir

# یا اگر chart در Nexus نیست، از منبع اصلی pull کنید و به Nexus push کنید
```

#### 12.2.2. بررسی Status

```bash
# روی Control Plane Node (k8s-cp-01)
kubectl get pods -n infrastructure -l app=jira
kubectl get svc -n infrastructure -l app=jira
kubectl get ingress -n infrastructure
```

### 12.3. Deploy Confluence Data Center (اولویت 2)

**⚠ مهم**: Confluence images باید در registry محلی (`rr.alefba2.ir`) موجود باشند.

#### 12.3.1. نصب Confluence از Nexus

```bash
# روی Control Plane Node (k8s-cp-01)
# نصب Confluence از Nexus
helm install confluence my-nexus/confluence \
  --namespace infrastructure \
  --set image.registry=rr.alefba2.ir \
  --set image.repository=atlassian/confluence \
  --set replicaCount=1 \
  --set-string nodeSelector."node-role\.kubernetes\.io/collab"=true \
  --set tolerations[0].key=collab \
  --set tolerations[0].operator=Equal \
  --set-string tolerations[0].value=true \
  --set tolerations[0].effect=NoSchedule \
  --set persistence.size=200Gi \
  --set service.type=ClusterIP \
  --set ingress.enabled=true \
  --set ingress.hostname=confluence.alefba2.ir \
  --set ingress.tls[0].hosts[0]=confluence.alefba2.ir \
  --set test.resources.requests.cpu=100m \
  --set test.resources.requests.memory=256Mi \
  --set test.resources.limits.cpu=200m \
  --set test.resources.limits.memory=512Mi


```

#### 12.3.2. بررسی Status

```bash
# روی Control Plane Node (k8s-cp-01)
kubectl get pods -n infrastructure -l app=confluence
kubectl get svc -n infrastructure -l app=confluence
```

### 12.4. Deploy Nextcloud (اولویت 3)

**⚠ مهم**: Nextcloud images باید در registry محلی (`rr.alefba2.ir`) موجود باشند.

#### 12.4.1. نصب Nextcloud از Nexus

```bash
# روی Control Plane Node (k8s-cp-01)
# نصب Nextcloud از Nexus
helm install nextcloud my-nexus/nextcloud \
  --namespace infrastructure \
  --set image.registry=rr.alefba2.ir \
  --set image.repository=library/nextcloud \
  --set replicaCount=1 \
  --set-string nodeSelector."node-role\.kubernetes\.io/collab"=true \
  --set tolerations[0].key=collab \
  --set tolerations[0].operator=Equal \
  --set-string tolerations[0].value=true \
  --set tolerations[0].effect=NoSchedule \
  --set persistence.size=300Gi \
  --set service.type=ClusterIP \
  --set ingress.enabled=true \
  --set ingress.hostname=cloud.alefba2.ir \
  --set ingress.tls[0].hosts[0]=cloud.alefba2.ir \
  --set test.resources.requests.cpu=100m \
  --set test.resources.requests.memory=256Mi \
  --set test.resources.limits.cpu=200m \
  --set test.resources.limits.memory=512Mi
```

#### 12.4.2. بررسی Status

```bash
# روی Control Plane Node (k8s-cp-01)
kubectl get pods -n infrastructure -l app=nextcloud
kubectl get svc -n infrastructure -l app=nextcloud
```

### 12.5. Deploy GitLab (اختیاری - بعد از اولویت‌ها)

#### 12.5.1. نصب GitLab از Nexus

```bash
# روی Control Plane Node (k8s-cp-01)
helm install gitlab my-nexus/gitlab \
  --namespace infrastructure \
  --set global.hosts.domain=git.alefba2.ir \
  --set global.imageRegistry=rr.alefba2.ir
```

### 12.6. Deploy Jenkins (اختیاری - بعد از اولویت‌ها)

#### 12.6.1. نصب Jenkins از Nexus

```bash
# روی Control Plane Node (k8s-cp-01)
helm install jenkins my-nexus/jenkins \
  --namespace infrastructure \
  --set controller.image.registry=rr.alefba2.ir \
  --set controller.serviceType=NodePort \
  --set controller.serviceNodePort=30092
```

---

## 13. راه‌اندازی Security و RBAC

### 13.1. راه‌اندازی Keycloak

#### 13.1.1. استفاده از Helm Chart

```bash
# روی Management Node
# ⚠ air-gapped: chart باید داخل Nexus باشد (به جای repo اینترنتی)
# helm search repo my-nexus | grep -i keycloak

helm install keycloak my-nexus/keycloak \
  --namespace infrastructure \
  --create-namespace \
  --set replicaCount=2 \
  --set image.registry=rr.alefba2.ir \
  --set image.repository=keycloak/keycloak \
  --set image.tag=26.5.2 \
  --set postgresql.enabled=true \
  --set postgresql.image.registry=rr.alefba2.ir \
  --set postgresql.image.repository=library/postgres \
  --set postgresql.image.tag=16-alpine
```

### 13.2. تنظیم RBAC

#### 13.2.1. ایجاد Role

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: developer-role
rules:
  - apiGroups: [ "" ]
    resources: [ "pods", "services" ]
    verbs: [ "get", "list", "watch" ]
  - apiGroups: [ "apps" ]
    resources: [ "deployments" ]
    verbs: [ "get", "list", "create", "update" ]
EOF
```

#### 13.2.2. ایجاد RoleBinding

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: production
subjects:
  - kind: User
    name: developer@example.com
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer-role
  apiGroup: rbac.authorization.k8s.io
EOF
```

### 13.3. تنظیم Network Policies

#### 13.3.1. ایجاد Network Policy

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: gateway-ui
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: cockroachdb
      ports:
        - protocol: TCP
          port: 26257
EOF
```

### 13.4. راه‌اندازی ابزارهای امنیتی OWASP

**⚠ مهم**: این ابزارها برای امنیت Kubernetes cluster ضروری هستند. برای جزئیات کامل،
به [راهنمای جامع OWASP](Security-OWASP-Comprehensive-Guide) مراجعه کنید.

#### 13.4.1. نصب Trivy Operator (Vulnerability Scanning)

**⚠ مهم**: Trivy Operator images باید در registry محلی (`rr.alefba2.ir`) موجود باشند.

```bash
# روی Control Plane Node (k8s-cp-01)
# اطمینان از پیکربندی Helm برای Nexus (بخش 0.3)

# نصب Trivy Operator از Nexus
helm install trivy-operator my-nexus/trivy-operator \
  --namespace trivy-system \
  --create-namespace \
  --set image.registry=rr.alefba2.ir \
  --set image.repository=aquasec/trivy-operator \
  --set image.tag=0.29.0

# بررسی Status
kubectl get pods -n trivy-system
kubectl get vulnerabilityreports -A
```

#### 13.4.2. نصب Falco (Runtime Security Monitoring)

**⚠ مهم**: Falco images باید در registry محلی (`rr.alefba2.ir`) موجود باشند.

```bash
# روی Control Plane Node (k8s-cp-01)
# نصب Falco از Nexus
helm install falco my-nexus/falco \
  --namespace falco-system \
  --create-namespace \
  --set image.registry=rr.alefba2.ir \
  --set image.repository=falcosecurity/falco \
  --set image.tag=0.43.0 \
  --set falcosidekick.enabled=true \
  --set falcosidekick.image.registry=rr.alefba2.ir \
  --set falcosidekick.image.repository=falcosecurity/falcosidekick \
  --set falcosidekick.image.tag=2.32.0

# بررسی Status
kubectl get pods -n falco-system
```

#### 13.4.3. نصب OPA Gatekeeper یا Kyverno (Policy Enforcement)

**⚠ مهم**: انتخاب یکی از این دو ابزار. Kyverno ساده‌تر است و برای شروع توصیه می‌شود.

##### گزینه 1: Kyverno (توصیه می‌شود)

```bash
# روی Control Plane Node (k8s-cp-01)
# نصب Kyverno از Nexus
helm install kyverno my-nexus/kyverno \
  --namespace kyverno \
  --create-namespace \
  --set image.registry=rr.alefba2.ir \
  --set image.repository=kyverno/kyverno \
  --set image.tag=v1.17.0 \
  --set initImage.registry=rr.alefba2.ir \
  --set initImage.repository=kyverno/kyvernopre \
  --set initImage.tag=v1.17.0

# بررسی Status
kubectl get pods -n kyverno

# ایجاد Policy نمونه: جلوگیری از استفاده از latest tag
cat <<EOF | kubectl apply -f -
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: enforce
  rules:
  - name: require-image-tag
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "Using 'latest' tag is not allowed"
      pattern:
        spec:
          containers:
          - name: "*"
            image: "!*:latest"
EOF
```

##### گزینه 2: OPA Gatekeeper

```bash
# روی Control Plane Node (k8s-cp-01)
# نصب OPA Gatekeeper از Nexus
helm install gatekeeper my-nexus/gatekeeper \
  --namespace gatekeeper-system \
  --create-namespace \
  --set image.registry=rr.alefba2.ir \
  --set image.repository=openpolicyagent/gatekeeper \
  --set image.tag=v3.21.0

# بررسی Status
kubectl get pods -n gatekeeper-system
```

#### 13.4.4. پیکربندی Security Policies

```bash
# روی Control Plane Node (k8s-cp-01)
# ایجاد Security Policies با Kyverno

# Policy 1: جلوگیری از اجرای Pod با root user
cat <<EOF | kubectl apply -f -
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-non-root-user
spec:
  validationFailureAction: enforce
  rules:
  - name: check-security-context
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "Pods must run as non-root user"
      pattern:
        spec:
          securityContext:
            runAsNonRoot: true
          containers:
          - name: "*"
            securityContext:
              runAsNonRoot: true
EOF

# Policy 2: الزام استفاده از read-only root filesystem
cat <<EOF | kubectl apply -f -
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-read-only-root-fs
spec:
  validationFailureAction: enforce
  rules:
  - name: check-read-only-root
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "Root filesystem must be read-only"
      pattern:
        spec:
          containers:
          - name: "*"
            securityContext:
              readOnlyRootFilesystem: true
EOF

# Policy 3: جلوگیری از استفاده از hostNetwork
cat <<EOF | kubectl apply -f -
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-host-network
spec:
  validationFailureAction: enforce
  rules:
  - name: check-host-network
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "hostNetwork is not allowed"
      pattern:
        spec:
          hostNetwork: "false"
EOF
```

#### 13.4.5. بررسی و Monitoring امنیتی

```bash
# روی Control Plane Node (k8s-cp-01)
# بررسی Vulnerability Reports از Trivy
kubectl get vulnerabilityreports -A

# بررسی Falco Events
kubectl logs -n falco-system -l app=falco --tail=100

# بررسی Kyverno Policy Violations
kubectl get policyreport -A
kubectl get clusterpolicyreport

# مشاهده Policy Violations
kubectl describe policyreport -n <namespace>
```

#### 13.4.6. یکپارچه‌سازی با Prometheus (اختیاری)

```bash
# روی Control Plane Node (k8s-cp-01)
# Falco metrics در Prometheus
# Falco به صورت خودکار metrics را در /metrics endpoint ارائه می‌دهد

# اضافه کردن ServiceMonitor برای Falco
cat <<EOF | kubectl apply -f -
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: falco
  namespace: falco-system
spec:
  selector:
    matchLabels:
      app: falco
  endpoints:
  - port: metrics
    interval: 30s
EOF
```

**نکات مهم:**

- **Trivy Operator**: به صورت خودکار تمام images را اسکن می‌کند و Vulnerability Reports ایجاد می‌کند
- **Falco**: به صورت real-time رفتارهای مشکوک را شناسایی می‌کند
- **Kyverno/OPA**: از اجرای Podها و Deployments ناامن جلوگیری می‌کند
- برای جزئیات بیشتر، به [راهنمای جامع OWASP](Security-OWASP-Comprehensive-Guide) مراجعه کنید

---

## 14. راه‌اندازی Backup و Disaster Recovery

### 14.1. نصب Velero

#### 14.1.1. نصب Velero CLI

```bash
# روی Management Node
# ⚠ air-gapped: فایل باینری velero را در Nexus نگهداری کنید و از همانجا دانلود کنید
# نسخه پیشنهادی (بر اساس موجودی رجیستری): v1.17.2
wget https://github.com/vmware-tanzu/velero/releases/download/v1.17.2/velero-v1.17.2-linux-amd64.tar.gz
tar -xzf velero-v1.17.2-linux-amd64.tar.gz
sudo mv velero-v1.17.2-linux-amd64/velero /usr/local/bin/
```

#### 14.1.2. نصب Velero در Cluster

```bash
# روی Management Node
# نیاز به S3-compatible storage
velero install \
  --provider aws \
  --image rr.alefba2.ir/velero/velero:v1.17.2 \
  --plugins rr.alefba2.ir/velero/velero-plugin-for-aws:v1.13.0 \
  --bucket my-backup-bucket \
  --secret-file ./credentials-velero \
  --use-volume-snapshots=false \
  --backup-location-config region=us-west-2
```

### 14.2. تنظیم Backup Schedule

#### 14.2.1. ایجاد Backup Schedule

```bash
# روی Management Node
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces production,stage,dev \
  --ttl 720h0m0s
```

### 14.3. Database Backup Scripts

#### 14.3.1. CockroachDB Backup

```bash
# ایجاد CronJob برای CockroachDB backup
cat <<EOF | kubectl apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cockroachdb-backup
  namespace: production
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: rr.alefba2.ir/cockroachdb/cockroach:v24.3.25
              command:
                - /cockroach/cockroach
                - dump
                - --host=cockroachdb.production.svc.cluster.local
                - --user=root
                - --insecure
                - --database=app_db
                - --format=sql
                - > /backup/cockroachdb-\$(date +%Y%m%d).sql
              volumeMounts:
                - name: backup-volume
                  mountPath: /backup
          volumes:
            - name: backup-volume
              persistentVolumeClaim:
                claimName: backup-pvc
          restartPolicy: OnFailure
EOF
```

---

## 15. تنظیمات Port و Networking

### 15.1. Port Allocation

#### 15.1.1. Service Ports

```yaml
# Backend Services
infrastructure-service: 8080
workflow-service: 8080
report-manager-service: 8080
gateway-ui: 8080
gateway-external: 8080
gateway-input: 8080

# Databases
cockroachdb: 26257 (grpc), 8080 (http)
clickhouse: 8123 (http), 9000 (native)
redis: 6379

# Messaging
kafka/redpanda: 9092
schema-registry: 8081

# Infrastructure Tools
jira: 8080
confluence: 8090
gitlab: 80, 443
jenkins: 8080
nextcloud: 80, 443
```

#### 15.1.2. Ingress Ports

```yaml
# HTTP: 80
# HTTPS: 443

# Dev Environment
dev-api.example.com: 80 -> gateway-ui.dev
dev-app.example.com: 80 -> frontend.dev

# Stage Environment
stage-api.example.com: 80 -> gateway-ui.stage
stage-app.example.com: 80 -> frontend.stage

# Production Environment
api.example.com: 443 -> gateway-ui.production
app.example.com: 443 -> frontend.production
```

### 15.2. Ingress Configuration

#### 15.2.1. ایجاد Ingress برای Production

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: production-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
    - hosts:
        - api.example.com
        - app.example.com
      secretName: production-tls
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
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 80
EOF
```

---

## 16. بهینه‌سازی و Performance Tuning

### 16.1. Resource Optimization

#### 16.1.1. تنظیم ResourceQuota

```bash
# روی Master Node
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
EOF
```

### 16.2. Performance Tuning

#### 16.2.1. JVM Tuning برای Java Services

```yaml
# در Deployment
env:
  - name: JAVA_OPTS
    value: "-Xms1g -Xmx2g -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
```

#### 16.2.2. Database Tuning

```yaml
# Cockro achDB
--cache=25%
--max-sql-memory=25%

# ClickHouse
max_memory_usage: 10000000000
max_threads: 8
```

---

## نتیجه‌گیری

این راهنمای فنی، مراحل کامل راه‌اندازی یک خوشه Kubernetes یکپارچه را برای پروژه بزرگ بیمه شرح می‌دهد. با دنبال کردن این
مراحل، می‌توانید یک زیرساخت enterprise-grade ایجاد کنید که تمام نیازهای پروژه را پوشش می‌دهد.

**نکات مهم:**

- همیشه backup بگیرید قبل از تغییرات مهم
- تست کنید در محیط dev/stage قبل از production
- مانیتورینگ را فعال نگه دارید
- Security را جدی بگیرید

---

# Debug

```bash
#قسمت ۱: اطلاعات کلی کلاستر

#این دستورات وضعیت کلی کلاستر را نشان می‌دهند.

# 1.1. وضعیت عمومی کلاستر
kubectl cluster-info
kubectl version

# 1.2. وضعیت همه nodeها
kubectl get nodes -o wide
kubectl describe nodes | grep -A5 Taints

# 1.3. وضعیت همه podها در همه namespaceها
kubectl get pods --all-namespaces -o wide

#قسمت ۲: اطلاعات کامل Calico

#این دستورات وضعیت Calico را به طور کامل نشان می‌دهند.

# 2.1. وضعیت کلی Calico (از دید خودش)
sudo calicoctl node status

# 2.2. اطلاعات کامل BGP (برای یافتن mismatch)
sudo calicoctl get bgpconfigurations -o yaml
sudo calicoctl get bgppeers -o yaml
sudo calicoctl get ippool -o yaml

# 2.3. اطلاعات کامل nodeها از دید Calico (IP، AS Number)
sudo calicoctl get nodes -o yaml

#قسمت ۳: اطلاعات کامل podهای مشکل‌دار در calico-system

#سه پاد مشکل‌دار فعلی را بررسی می‌کنیم.
#الف) calico-node روی worker-02

# 3.1. نام دقیق pod calico-node روی worker-02 را پیدا کنید
kubectl get pods -n calico-system -o wide | grep worker-02 | grep calico-node

# (خروجی این دستور را ببینید و نام پاد را در دستورات زیر جایگزین <pod-name> کنید)
# مثال: اگر نام پاد calico-node-xxxxx بود، دستورات زیر را با آن نام اجرا کنید.

# 3.2. رویدادهای مربوط به این pod
kubectl describe pod -n calico-system <pod-name>

# 3.3. لاگ کامل (و لاگ قبلی) این pod
kubectl logs -n calico-system <pod-name>
kubectl logs -n calico-system <pod-name> --previous

# 3.4. وضعیت bird داخل کانتینر (اگر pod در حال اجراست)
kubectl exec -n calico-system <pod-name> -- birdc show status
kubectl exec -n calico-system <pod-name> -- birdc show protocols
kubectl exec -n calico-system <pod-name> -- cat /var/log/calico/bird/bird.log

#ب) csi-node-driver روی worker-02

# 3.5. نام دقیق pod csi-node-driver روی worker-02 را پیدا کنید
kubectl get pods -n calico-system -o wide | grep worker-02 | grep csi-node-driver

# 3.6. رویدادها و لاگ‌های این pod
kubectl describe pod -n calico-system <csi-pod-name>
kubectl logs -n calico-system <csi-pod-name> -c calico-csi --previous
kubectl logs -n calico-system <csi-pod-name> -c csi-node-driver-registrar --previous

#قسمت ۴: اطلاعات کامل Ingress Controller

# 4.1. رویدادهای Deployment و Pod
kubectl describe deployment -n ingress-nginx ingress-nginx-controller
kubectl describe pod -n ingress-nginx -l app.kubernetes.io/component=controller

# 4.2. لاگ‌های پاد (حتی اگر در حال اجرا نیست)
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller --tail=100
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller --previous --tail=100

# 4.3. وضعیت سرویس‌ها و webhook
kubectl get svc -n ingress-nginx
kubectl get validatingwebhookconfiguration ingress-nginx-admission -o yaml

#قسمت ۵: اطلاعات سیستم‌عامل و شبکه روی خود nodeها (این دستورات را با SSH روی هر node اجرا کنید)
#روی k8s-worker-02 (ماشین اصلی مشکل‌دار)

# با دستور ssh k8s-worker-02 وارد شوید و این دستورات را اجرا کنید:

# 5.1. اطلاعات سیستم‌عامل و هسته
uname -a
cat /etc/os-release

# 5.2. وضعیت پورت‌های مورد نیاز Calico (179 برای BGP، 4789 برای VXLAN)
sudo ss -tulpn | grep -E ':(179|4789|5473|9099)'

# 5.3. لاگ‌های مربوط به bird (اگر روی سیستم نصب است) و containerd
sudo journalctl -u containerd --since "5 minutes ago" | grep -i error
sudo journalctl -u kubelet --since "10 minutes ago" | grep -E "Error|Fail|Crash|calico|bird"

# 5.4. اطلاعات شبکه و مسیریابی
ip addr show
ip route show
ping -c 3 192.168.10.151   # control-plane
ping -c 3 192.168.10.152   # worker-01
ping -c 3 192.168.10.154   # collab-01

# 5.5. تست اتصال به رجیستری داخلی
curl -v https://alefba2.ir/v2/
curl -v https://rr.alefba2.ir/v2/  # باید 401 بدهد، یعنی اتصال برقرار است

# روی k8s-worker-01 (برای مقایسه)

# با دستور ssh k8s-worker-01 وارد شوید:

# 5.6. وضعیت پورت‌ها
sudo ss -tulpn | grep -E ':(179|4789|5473|9099)'

# 5.7. لاگ‌های کوتاه kubelet و containerd
sudo journalctl -u kubelet --since "10 minutes ago" | grep -E "Error|Fail|calico"
sudo journalctl -u containerd --since "5 minutes ago" | grep -i error

# 5.8. تست اتصال به رجیستری
curl -v https://alefba2.ir/v2/

#قسمت ۶: اطلاعات نهایی

# 6.1. تمام رویدادهای namespaceهای مهم در 30 دقیقه اخیر
kubectl get events -n calico-system --sort-by='.lastTimestamp' | tail -30
kubectl get events -n ingress-nginx --sort-by='.lastTimestamp' | tail -20


```

<div align="center">

[↑ بازگشت به بالا](#راهنمای-فنی-پیادهسازی-kubernetes---قدم-به-قدم) | [← بازگشت به صفحه اصلی](Home) | [پروپوزال Kubernetes](Proposal-Kubernetes) | [لینک‌های مفید](References)

</div>

