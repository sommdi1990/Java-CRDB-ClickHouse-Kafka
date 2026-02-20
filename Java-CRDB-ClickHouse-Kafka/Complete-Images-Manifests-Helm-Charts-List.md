# لیست کامل Images، Manifests و Helm Charts - راه‌اندازی از صفر تا صد

## Rocky Linux 10 – Revision 4

> **Owner:** Soroush  
> **Scope:** لیست کامل تمام منابع مورد نیاز برای راه‌اندازی کامل سیستم  
> **Kubernetes Version:** v1.32.3 (Stable LTS - 2026)

---

## 📋 فهرست مطالب

1. [Phase 0: Registry و Nexus Infrastructure](#phase-0-registry-و-nexus-infrastructure)
2. [Phase 1: Kubernetes Core Images](#phase-1-kubernetes-core-images)
3. [Phase 2: CNI و Networking](#phase-2-cni-و-networking)
4. [Phase 3: Core Add-ons](#phase-3-core-add-ons)
5. [Phase 4: Monitoring Stack](#phase-4-monitoring-stack)
6. [Phase 5: Databases](#phase-5-databases)
7. [Phase 6: Messaging](#phase-6-messaging)
8. [Phase 7: Security](#phase-7-security)
9. [Phase 8: Infrastructure Tools](#phase-8-infrastructure-tools)
10. [Phase 9: Application Services](#phase-9-application-services)
11. [Phase 10: Backup و Disaster Recovery](#phase-10-backup-و-disaster-recovery)

---

```bash
nerdctl login rr.alefba2.ir -u admin -p '<pass>'
```

## Phase 0: Registry و Nexus Infrastructure

### 0.1. Docker Registry Images

| Image                      | Version | Source     | Download Link                              | Push Command                                                |
|----------------------------|---------|------------|--------------------------------------------|-------------------------------------------------------------|
| `registry:3`               | `3.0.0` | Docker Hub | `docker.io/library/registry:3.0.0`         | `nerdctl push rr.alefba2.ir/library/registry:3.0.0`         |
| `joxit/docker-registry-ui` | `2.6.0` | Docker Hub | `docker.io/joxit/docker-registry-ui:2.6.0` | `nerdctl push rr.alefba2.ir/joxit/docker-registry-ui:2.6.0` |

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
# Pull images
nerdctl pull docker.io/library/registry:3.0.0
nerdctl pull docker.io/joxit/docker-registry-ui:2.6.0

# Tag برای registry محلی
nerdctl tag docker.io/library/registry:3.0.0 rr.alefba2.ir/library/registry:3.0.0
nerdctl tag docker.io/joxit/docker-registry-ui:2.6.0 rr.alefba2.ir/joxit/docker-registry-ui:2.6.0

# Login به registry
nerdctl login rr.alefba2.ir -u admin -p '<pass>'

# Push به registry
nerdctl push rr.alefba2.ir/library/registry:3.0.0
nerdctl push rr.alefba2.ir/joxit/docker-registry-ui:2.6.0
```

### 0.2. Nexus Repository Manager

| Component                | Version     | Download Link                                                       | Installation   |
|--------------------------|-------------|---------------------------------------------------------------------|----------------|
| Nexus Repository Manager | `3.68.0-02` | `https://download.sonatype.com/nexus/3/nexus-3.68.0-02-unix.tar.gz` | Manual install |

**نکته:** Nexus به صورت binary نصب می‌شود، نه Docker image.

---

## Phase 1: Kubernetes Core Images

### 1.1. Kubernetes Control Plane Images

| Image                     | Version    | Source          | Download Link                                     | Push Command                                                     |
|---------------------------|------------|-----------------|---------------------------------------------------|------------------------------------------------------------------|
| `kube-apiserver`          | `v1.32.3`  | registry.k8s.io | `registry.k8s.io/kube-apiserver:v1.32.3`          | `nerdctl push rr.alefba2.ir/k8s/kube-apiserver:v1.32.3`          |
| `kube-controller-manager` | `v1.32.3`  | registry.k8s.io | `registry.k8s.io/kube-controller-manager:v1.32.3` | `nerdctl push rr.alefba2.ir/k8s/kube-controller-manager:v1.32.3` |
| `kube-scheduler`          | `v1.32.3`  | registry.k8s.io | `registry.k8s.io/kube-scheduler:v1.32.3`          | `nerdctl push rr.alefba2.ir/k8s/kube-scheduler:v1.32.3`          |
| `kube-proxy`              | `v1.32.3`  | registry.k8s.io | `registry.k8s.io/kube-proxy:v1.32.3`              | `nerdctl push rr.alefba2.ir/k8s/kube-proxy:v1.32.3`              |
| `etcd`                    | `3.5.15-0` | registry.k8s.io | `registry.k8s.io/etcd:3.5.15-0`                   | `nerdctl push rr.alefba2.ir/k8s/etcd:3.5.15-0`                   |
| `coredns`                 | `v1.11.3`  | registry.k8s.io | `registry.k8s.io/coredns/coredns:v1.11.3`         | `nerdctl push rr.alefba2.ir/k8s/coredns:v1.11.3`                 |
| `pause`                   | `3.10.1`   | registry.k8s.io | `registry.k8s.io/pause:3.10.1`                    | `nerdctl push rr.alefba2.ir/k8s/pause:3.10.1`                    |

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
# Pull همه images
nerdctl pull registry.k8s.io/kube-apiserver:v1.32.3
nerdctl pull registry.k8s.io/kube-controller-manager:v1.32.3
nerdctl pull registry.k8s.io/kube-scheduler:v1.32.3
nerdctl pull registry.k8s.io/kube-proxy:v1.32.3
nerdctl pull registry.k8s.io/etcd:3.5.15-0
nerdctl pull registry.k8s.io/coredns/coredns:v1.11.3
nerdctl pull registry.k8s.io/pause:3.10.1

# Tag برای registry محلی (سرور ایران)
nerdctl tag registry.k8s.io/kube-apiserver:v1.32.3 rr.alefba2.ir/k8s/kube-apiserver:v1.32.3
nerdctl tag registry.k8s.io/kube-controller-manager:v1.32.3 rr.alefba2.ir/k8s/kube-controller-manager:v1.32.3
nerdctl tag registry.k8s.io/kube-scheduler:v1.32.3 rr.alefba2.ir/k8s/kube-scheduler:v1.32.3
nerdctl tag registry.k8s.io/kube-proxy:v1.32.3 rr.alefba2.ir/k8s/kube-proxy:v1.32.3
nerdctl tag registry.k8s.io/etcd:3.5.15-0 rr.alefba2.ir/k8s/etcd:3.5.15-0
nerdctl tag registry.k8s.io/coredns/coredns:v1.11.3 rr.alefba2.ir/k8s/coredns:v1.11.3
nerdctl tag registry.k8s.io/pause:3.10.1 rr.alefba2.ir/k8s/pause:3.10.1

# Push به registry سرور ایران
nerdctl push rr.alefba2.ir/k8s/kube-apiserver:v1.32.3
nerdctl push rr.alefba2.ir/k8s/kube-controller-manager:v1.32.3
nerdctl push rr.alefba2.ir/k8s/kube-scheduler:v1.32.3
nerdctl push rr.alefba2.ir/k8s/kube-proxy:v1.32.3
nerdctl push rr.alefba2.ir/k8s/etcd:3.5.15-0
nerdctl push rr.alefba2.ir/k8s/coredns:v1.11.3
nerdctl push rr.alefba2.ir/k8s/pause:3.10.1
```

**استفاده در kubeadm:**

```bash
# روی Master Node
sudo kubeadm init \
  --pod-network-cidr=192.168.0.0/16 \
  --image-repository=rr.alefba2.ir/k8s \
  --kubernetes-version=v1.32.3
```

---

## Phase 2: CNI و Networking

### 2.1. Calico CNI Images

| Image                          | Version   | Source  | Download Link                                  | Push Command                                                           |
|--------------------------------|-----------|---------|------------------------------------------------|------------------------------------------------------------------------|
| `calico/node`                  | `v3.35.0` | quay.io | `quay.io/calico/node:v3.35.0`                  | `nerdctl push rr.alefba2.ir/quay/calico/node:v3.35.0`                  |
| `calico/cni`                   | `v3.35.0` | quay.io | `quay.io/calico/cni:v3.35.0`                   | `nerdctl push rr.alefba2.ir/quay/calico/cni:v3.35.0`                   |
| `calico/kube-controllers`      | `v3.35.0` | quay.io | `quay.io/calico/kube-controllers:v3.35.0`      | `nerdctl push rr.alefba2.ir/quay/calico/kube-controllers:v3.35.0`      |
| `calico/pod2daemon-flexvol`    | `v3.35.0` | quay.io | `quay.io/calico/pod2daemon-flexvol:v3.35.0`    | `nerdctl push rr.alefba2.ir/quay/calico/pod2daemon-flexvol:v3.35.0`    |
| `calico/csi`                   | `v3.35.0` | quay.io | `quay.io/calico/csi:v3.35.0`                   | `nerdctl push rr.alefba2.ir/quay/calico/csi:v3.35.0`                   |
| `calico/typha`                 | `v3.35.0` | quay.io | `quay.io/calico/typha:v3.35.0`                 | `nerdctl push rr.alefba2.ir/quay/calico/typha:v3.35.0`                 |
| `calico/apiserver`             | `v3.35.0` | quay.io | `quay.io/calico/apiserver:v3.35.0`             | `nerdctl push rr.alefba2.ir/quay/calico/apiserver:v3.35.0`             |
| `calico/node-driver-registrar` | `v3.35.0` | quay.io | `quay.io/calico/node-driver-registrar:v3.35.0` | `nerdctl push rr.alefba2.ir/quay/calico/node-driver-registrar:v3.35.0` |
| `tigera/operator`              | `v1.45.0` | quay.io | `quay.io/tigera/operator:v1.40.3`              | `nerdctl push rr.alefba2.ir/tigera/operator:v1.40.3`                   |

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
nerdctl pull quay.io/tigera/operator:v1.40.3
nerdctl pull quay.io/calico/node:v3.31.3
nerdctl pull quay.io/calico/cni:v3.31.3
nerdctl pull quay.io/calico/kube-controllers:v3.31.3
nerdctl pull quay.io/calico/pod2daemon-flexvol:v3.31.3
nerdctl pull quay.io/calico/csi:v3.31.3
nerdctl pull quay.io/calico/typha:v3.31.3
nerdctl pull quay.io/calico/node-driver-registrar:v3.31.3
nerdctl pull quay.io/calico/apiserver:v3.31.3
nerdctl pull quay.io/calico/goldmane:v3.31.3
nerdctl pull quay.io/calico/whisker:v3.31.3
nerdctl pull quay.io/calico/whisker-backend:v3.31.3


# Tag برای registry محلی (سرور ایران)
nerdctl tag quay.io/tigera/operator:v1.40.3 rr.alefba2.ir/tigera/operator:v1.40.3
nerdctl tag quay.io/calico/node:v3.31.3 rr.alefba2.ir/quay/calico/node:v3.31.3
nerdctl tag quay.io/calico/cni:v3.31.3 rr.alefba2.ir/quay/calico/cni:v3.31.3
nerdctl tag quay.io/calico/kube-controllers:v3.31.3 rr.alefba2.ir/quay/calico/kube-controllers:v3.31.3
nerdctl tag quay.io/calico/pod2daemon-flexvol:v3.31.3 rr.alefba2.ir/quay/calico/pod2daemon-flexvol:v3.31.3
nerdctl tag quay.io/calico/csi:v3.31.3 rr.alefba2.ir/quay/calico/csi:v3.31.3
nerdctl tag quay.io/calico/typha:v3.31.3 rr.alefba2.ir/quay/calico/typha:v3.31.3
nerdctl tag quay.io/calico/node-driver-registrar:v3.31.3 rr.alefba2.ir/quay/calico/node-driver-registrar:v3.31.3
nerdctl tag quay.io/calico/apiserver:v3.31.3 rr.alefba2.ir/quay/calico/apiserver:v3.31.3
nerdctl tag quay.io/calico/goldmane:v3.31.3 rr.alefba2.ir/quay/calico/goldmane:v3.31.3
nerdctl tag quay.io/calico/whisker:v3.31.3 rr.alefba2.ir/quay/calico/whisker:v3.31.3
docker tag quay.io/calico/whisker-backend:v3.31.3 rr.alefba2.ir/quay/calico/whisker-backend:v3.31.3

# Push به registry سرور ایران
nerdctl push rr.alefba2.ir/tigera/operator:v1.40.3
nerdctl push rr.alefba2.ir/quay/calico/node:v3.31.3
nerdctl push rr.alefba2.ir/quay/calico/cni:v3.31.3
nerdctl push rr.alefba2.ir/quay/calico/kube-controllers:v3.31.3
nerdctl push rr.alefba2.ir/quay/calico/pod2daemon-flexvol:v3.31.3
nerdctl push rr.alefba2.ir/quay/calico/csi:v3.31.3
nerdctl push rr.alefba2.ir/quay/calico/typha:v3.31.3
nerdctl push rr.alefba2.ir/quay/calico/node-driver-registrar:v3.31.3
nerdctl push rr.alefba2.ir/quay/calico/apiserver:v3.31.3
nerdctl push rr.alefba2.ir/quay/calico/goldmane:v3.31.3
nerdctl push rr.alefba2.ir/quay/calico/whisker:v3.31.3
docker push rr.alefba2.ir/quay/calico/whisker-backend:v3.31.3

# Tag برای registry محلی (سرور ایران)
nerdctl tag quay.io/tigera/operator:v1.40.3 rr.alefba2.ir/tigera/operator:v1.40.3
nerdctl tag quay.io/calico/node:v3.31.3 rr.alefba2.ir/calico/node:v3.31.3
nerdctl tag quay.io/calico/cni:v3.31.3 rr.alefba2.ir/calico/cni:v3.31.3
nerdctl tag quay.io/calico/kube-controllers:v3.31.3 rr.alefba2.ir/calico/kube-controllers:v3.31.3
nerdctl tag quay.io/calico/pod2daemon-flexvol:v3.31.3 rr.alefba2.ir/calico/pod2daemon-flexvol:v3.31.3
nerdctl tag quay.io/calico/csi:v3.31.3 rr.alefba2.ir/calico/csi:v3.31.3
nerdctl tag quay.io/calico/typha:v3.31.3 rr.alefba2.ir/calico/typha:v3.31.3
nerdctl tag quay.io/calico/node-driver-registrar:v3.31.3 rr.alefba2.ir/calico/node-driver-registrar:v3.31.3
nerdctl tag quay.io/calico/apiserver:v3.31.3 rr.alefba2.ir/calico/apiserver:v3.31.3
nerdctl tag quay.io/calico/goldmane:v3.31.3 rr.alefba2.ir/calico/goldmane:v3.31.3
nerdctl tag quay.io/calico/whisker:v3.31.3 rr.alefba2.ir/calico/whisker:v3.31.3
docker tag quay.io/calico/whisker-backend:v3.31.3 rr.alefba2.ir/calico/whisker-backend:v3.31.3

# Push به registry سرور ایران
nerdctl push rr.alefba2.ir/tigera/operator:v1.40.3
nerdctl push rr.alefba2.ir/calico/node:v3.31.3
nerdctl push rr.alefba2.ir/calico/cni:v3.31.3
nerdctl push rr.alefba2.ir/calico/kube-controllers:v3.31.3
nerdctl push rr.alefba2.ir/calico/pod2daemon-flexvol:v3.31.3
nerdctl push rr.alefba2.ir/calico/csi:v3.31.3
nerdctl push rr.alefba2.ir/calico/typha:v3.31.3
nerdctl push rr.alefba2.ir/calico/node-driver-registrar:v3.31.3
nerdctl push rr.alefba2.ir/calico/apiserver:v3.31.3
nerdctl push rr.alefba2.ir/calico/goldmane:v3.31.3
nerdctl push rr.alefba2.ir/calico/whisker:v3.31.3
docker push rr.alefba2.ir/calico/whisker-backend:v3.31.3

```

**Helm Chart:**

| Chart             | Repository                             | Version   | Download/Push               |
|-------------------|----------------------------------------|-----------|-----------------------------|
| `tigera-operator` | `https://docs.tigera.io/calico/charts` | `v3.35.0` | Push to Nexus `helm-charts` |

**دستورات Helm:**

```bash
# روی Management Node
curl -u k8s-reader https://mn.alefba2.ir/repository/helm-charts/index.yaml
# اضافه کردن repo
helm repo add projectcalico https://docs.tigera.io/calico/charts
helm repo update

# Package chart
helm pull projectcalico/tigera-operator --version v3.35.0
helm package tigera-operator-v3.35.0.tgz

# Push به Nexus
helm repo index . --url https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader -T ./tigera-operator-*.tgz https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader -T ./index.yaml https://mn.alefba2.ir/repository/helm-charts/

# استفاده
helm repo add my-nexus https://mn.alefba2.ir/repository/helm-charts/ --username k8s-reader
helm install calico my-nexus/tigera-operator
```

---

## Phase 3: Core Add-ons

### 3.1. Metrics Server

| Image            | Version  | Source          | Download Link                                          | Push Command                                           |
|------------------|----------|-----------------|--------------------------------------------------------|--------------------------------------------------------|
| `metrics-server` | `v0.8.0` | registry.k8s.io | `registry.k8s.io/metrics-server/metrics-server:v0.8.0` | `nerdctl push rr.alefba2.ir/k8s/metrics-server:v0.8.0` |

**Manifest:**

| Manifest              | Source | Download Link                                                                                | Push to Nexus           |
|-----------------------|--------|----------------------------------------------------------------------------------------------|-------------------------|
| `metrics-server.yaml` | GitHub | `https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.8.0/components.yaml` | Push to `k8s-manifests` |

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
nerdctl pull registry.k8s.io/metrics-server/metrics-server:v0.8.0
nerdctl tag registry.k8s.io/metrics-server/metrics-server:v0.8.0 rr.alefba2.ir/k8s/metrics-server:v0.8.0
nerdctl push rr.alefba2.ir/k8s/metrics-server:v0.8.0

# دانلود و push manifest
curl -L https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.8.0/components.yaml -o metrics-server.yaml
# ویرایش image reference در manifest
sed -i 's|registry.k8s.io/metrics-server/metrics-server:v0.8.0|rr.alefba2.ir/k8s/metrics-server:v0.8.0|g' metrics-server.yaml
# In PowerShell Windows
(Get-Content .\metrics-server.yaml) -replace 'registry.k8s.io/metrics-server/metrics-server:v0.8.0', 'rr.alefba2.ir/k8s/metrics-server:v0.8.0' | Set-Content .\metrics-server.yaml
# Push به Nexus
curl -u k8s-reader --upload-file metrics-server.yaml https://mn.alefba2.ir/repository/k8s-manifests/core/metrics-server.yaml
```

### 3.2. Ingress NGINX

| Image                                | Version               | Source          | Download Link                                                            | Push Command                                                                        |
|--------------------------------------|-----------------------|-----------------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| `ingress-nginx/controller`           | `v1.12.0`             | registry.k8s.io | `registry.k8s.io/ingress-nginx/controller:v1.12.0`                       | `nerdctl push rr.alefba2.ir/ingress-nginx/controller:v1.12.0`                       |
| `ingress-nginx/kube-webhook-certgen` | `v20250101-8b53cabe0` | registry.k8s.io | `registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20250101-8b53cabe0` | `nerdctl push rr.alefba2.ir/ingress-nginx/kube-webhook-certgen:v20250101-8b53cabe0` |

**Helm Chart:**

| Chart           | Repository                                   | Version  | Download/Push               |
|-----------------|----------------------------------------------|----------|-----------------------------|
| `ingress-nginx` | `https://kubernetes.github.io/ingress-nginx` | `4.12.0` | Push to Nexus `helm-charts` |

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
docker pull registry.k8s.io/ingress-nginx/controller:v1.10.0
docker pull registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.0
docker pull k8s.gcr.io/defaultbackend-amd64:1.5

docker tag registry.k8s.io/ingress-nginx/controller:v1.10.0 rr.alefba2.ir/ingress-nginx/controller:v1.10.0
docker tag registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.0 rr.alefba2.ir/ingress-nginx/kube-webhook-certgen:v1.4.0
docker tag k8s.gcr.io/defaultbackend-amd64:1.5 rr.alefba2.ir/ingress-nginx/defaultbackend-amd64:1.5

docker push rr.alefba2.ir/ingress-nginx/controller:v1.10.0
docker push rr.alefba2.ir/ingress-nginx/kube-webhook-certgen:v1.4.0
docker push rr.alefba2.ir/ingress-nginx/defaultbackend-amd64:1.5

# Helm Chart
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm pull ingress-nginx/ingress-nginx --version 4.12.0
helm package ingress-nginx-4.12.0.tgz
helm repo index . --url https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader -T ./ingress-nginx-*.tgz https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader -T ./index.yaml https://mn.alefba2.ir/repository/helm-charts/
```

### 3.3. CSI Drivers و Storage (برای StorageClass)

| Image                       | Version   | Source          | Download Link                                                   | Push Command                                                       |
|-----------------------------|-----------|-----------------|-----------------------------------------------------------------|--------------------------------------------------------------------|
| `csi-snapshotter`           | `v6.3.2`  | registry.k8s.io | `registry.k8s.io/sig-storage/snapshot-controller:v6.3.2`        | `nerdctl push rr.alefba2.ir/k8s/snapshot-controller:v6.3.2`        |
| `csi-provisioner`           | `v4.0.0`  | registry.k8s.io | `registry.k8s.io/sig-storage/csi-provisioner:v4.0.0`            | `nerdctl push rr.alefba2.ir/k8s/csi-provisioner:v4.0.0`            |
| `csi-attacher`              | `v4.5.0`  | registry.k8s.io | `registry.k8s.io/sig-storage/csi-attacher:v4.5.0`               | `nerdctl push rr.alefba2.ir/k8s/csi-attacher:v4.5.0`               |
| `csi-resizer`               | `v1.10.0` | registry.k8s.io | `registry.k8s.io/sig-storage/csi-resizer:v1.10.0`               | `nerdctl push rr.alefba2.ir/k8s/csi-resizer:v1.10.0`               |
| `csi-node-driver-registrar` | `v2.11.0` | registry.k8s.io | `registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.11.1` | `nerdctl push rr.alefba2.ir/k8s/csi-node-driver-registrar:v2.11.0` |
| `snapshot-controller`       | `v6.3.2`  | registry.k8s.io | `registry.k8s.io/sig-storage/snapshot-controller:v6.3.2`        | `nerdctl push rr.alefba2.ir/k8s/snapshot-controller:v6.3.2`        |

**نکته:** این images برای StorageClass (مثل Local PV، NFS، Ceph) ضروری هستند. اگر از StorageClass استفاده می‌کنید، حتماً
این images را اضافه کنید.

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
nerdctl pull registry.k8s.io/sig-storage/snapshot-controller:v8.4.0
nerdctl pull registry.k8s.io/sig-storage/csi-provisioner:v4.0.1
nerdctl pull registry.k8s.io/sig-storage/csi-attacher:v4.9.0
nerdctl pull registry.k8s.io/sig-storage/csi-resizer:v1.12.0
nerdctl pull registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.14.0

# Tag و Push
nerdctl tag registry.k8s.io/sig-storage/snapshot-controller:v8.4.0 rr.alefba2.ir/k8s/snapshot-controller:v8.4.0
nerdctl tag registry.k8s.io/sig-storage/csi-provisioner:v4.0.1 rr.alefba2.ir/k8s/csi-provisioner:v4.0.1
nerdctl tag registry.k8s.io/sig-storage/csi-attacher:v4.9.0 rr.alefba2.ir/k8s/csi-attacher:v4.9.0
nerdctl tag registry.k8s.io/sig-storage/csi-resizer:v1.12.0 rr.alefba2.ir/k8s/csi-resizer:v1.12.0
nerdctl tag registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.14.0 rr.alefba2.ir/k8s/csi-node-driver-registrar:v2.14.0

nerdctl push rr.alefba2.ir/k8s/snapshot-controller:v8.4.0
nerdctl push rr.alefba2.ir/k8s/csi-provisioner:v4.0.1
nerdctl push rr.alefba2.ir/k8s/csi-attacher:v4.9.0
nerdctl push rr.alefba2.ir/k8s/csi-resizer:v1.12.0
nerdctl push rr.alefba2.ir/k8s/csi-node-driver-registrar:v2.14.0
```

### 3.4. cert-manager

> **نکته نسخه:** در حال حاضر نسخهٔ پایدار و موجود در رجیستری برای این استک، `v1.14.4` است (همخوان با Helm chart در همین
> فایل). نسخهٔ `v1.18.0` هنوز در quay.io منتشر نشده و `docker pull` برای آن خطای `not found` می‌دهد.

| Image                                  | Version   | Source  | Download Link                                      | Push Command                                                          |
|----------------------------------------|-----------|---------|----------------------------------------------------|-----------------------------------------------------------------------|
| `cert-manager/cert-manager-controller` | `v1.14.4` | quay.io | `quay.io/jetstack/cert-manager-controller:v1.14.4` | `nerdctl push rr.alefba2.ir/jetstack/cert-manager-controller:v1.14.4` |
| `cert-manager/cert-manager-webhook`    | `v1.14.4` | quay.io | `quay.io/jetstack/cert-manager-webhook:v1.14.4`    | `nerdctl push rr.alefba2.ir/jetstack/cert-manager-webhook:v1.14.4`    |
| `cert-manager/cert-manager-cainjector` | `v1.14.4` | quay.io | `quay.io/jetstack/cert-manager-cainjector:v1.14.4` | `nerdctl push rr.alefba2.ir/jetstack/cert-manager-cainjector:v1.14.4` |
| `cert-manager/cert-manager-ctl`        | `v1.14.4` | quay.io | `quay.io/jetstack/cert-manager-ctl:v1.14.4`        | `nerdctl push rr.alefba2.ir/jetstack/cert-manager-ctl:v1.14.4`        |

**Helm Chart:**

| Chart          | Repository                   | Version   | Download/Push               |
|----------------|------------------------------|-----------|-----------------------------|
| `cert-manager` | `https://charts.jetstack.io` | `v1.18.0` | Push to Nexus `helm-charts` |

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
nerdctl pull quay.io/jetstack/cert-manager-controller:v1.14.4
nerdctl pull quay.io/jetstack/cert-manager-webhook:v1.14.4
nerdctl pull quay.io/jetstack/cert-manager-cainjector:v1.14.4
nerdctl pull quay.io/jetstack/cert-manager-ctl:v1.14.4

nerdctl tag quay.io/jetstack/cert-manager-controller:v1.14.4 rr.alefba2.ir/jetstack/cert-manager-controller:v1.14.4
nerdctl tag quay.io/jetstack/cert-manager-webhook:v1.14.4 rr.alefba2.ir/jetstack/cert-manager-webhook:v1.14.4
nerdctl tag quay.io/jetstack/cert-manager-cainjector:v1.14.4 rr.alefba2.ir/jetstack/cert-manager-cainjector:v1.14.4
nerdctl tag quay.io/jetstack/cert-manager-ctl:v1.14.4 rr.alefba2.ir/jetstack/cert-manager-ctl:v1.14.4

nerdctl push rr.alefba2.ir/jetstack/cert-manager-controller:v1.14.4
nerdctl push rr.alefba2.ir/jetstack/cert-manager-webhook:v1.14.4
nerdctl push rr.alefba2.ir/jetstack/cert-manager-cainjector:v1.14.4
nerdctl push rr.alefba2.ir/jetstack/cert-manager-ctl:v1.14.4

# Helm Chart
helm repo add jetstack https://charts.jetstack.io
helm pull jetstack/cert-manager --version v1.18.0
helm package cert-manager-v1.18.0.tgz
helm repo index . --url https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader -T ./cert-manager-*.tgz https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader -T ./index.yaml https://mn.alefba2.ir/repository/helm-charts/
```

---

## Phase 4: Monitoring Stack

### 4.1. Prometheus Stack

| Image                                            | Version   | Source          | Download Link                                                    | Push Command                                                                        |
|--------------------------------------------------|-----------|-----------------|------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| `prometheus/prometheus`                          | `v3.12.0` | quay.io         | `quay.io/prometheus/prometheus:v3.12.0`                          | `nerdctl push rr.alefba2.ir/prometheus/prometheus:v3.12.0`                          |
| `prometheus/alertmanager`                        | `v0.32.0` | quay.io         | `quay.io/prometheus/alertmanager:v0.32.0`                        | `nerdctl push rr.alefba2.ir/prometheus/alertmanager:v0.32.0`                        |
| `prometheus/node-exporter`                       | `v1.12.0` | quay.io         | `quay.io/prometheus/node-exporter:v1.12.0`                       | `nerdctl push rr.alefba2.ir/prometheus/node-exporter:v1.12.0`                       |
| `prometheus/pushgateway`                         | `v1.13.0` | quay.io         | `quay.io/prometheus/pushgateway:v1.13.0`                         | `nerdctl push rr.alefba2.ir/prometheus/pushgateway:v1.13.0`                         |
| `grafana/grafana`                                | `13.0.0`  | docker.io       | `docker.io/grafana/grafana:13.0.0`                               | `nerdctl push rr.alefba2.ir/grafana/grafana:13.0.0`                                 |
| `kube-state-metrics/kube-state-metrics`          | `v2.20.0` | registry.k8s.io | `registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.20.0`  | `nerdctl push rr.alefba2.ir/k8s/kube-state-metrics:v2.20.0`                         |
| `prometheus-operator/prometheus-operator`        | `v0.95.0` | quay.io         | `quay.io/prometheus-operator/prometheus-operator:v0.95.0`        | `nerdctl push rr.alefba2.ir/prometheus-operator/prometheus-operator:v0.95.0`        |
| `prometheus-operator/prometheus-config-reloader` | `v0.95.0` | quay.io         | `quay.io/prometheus-operator/prometheus-config-reloader:v0.95.0` | `nerdctl push rr.alefba2.ir/prometheus-operator/prometheus-config-reloader:v0.95.0` |

**Helm Chart:**

| Chart                   | Repository                                           | Version  | Download/Push               |
|-------------------------|------------------------------------------------------|----------|-----------------------------|
| `kube-prometheus-stack` | `https://prometheus-community.github.io/helm-charts` | `65.0.0` | Push to Nexus `helm-charts` |

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
nerdctl pull quay.io/prometheus/prometheus:v3.12.0
nerdctl pull quay.io/prometheus/alertmanager:v0.32.0
nerdctl pull quay.io/prometheus/node-exporter:v1.12.0
nerdctl pull quay.io/prometheus/pushgateway:v1.13.0
nerdctl pull docker.io/grafana/grafana:13.0.0
nerdctl pull registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.20.0
nerdctl pull quay.io/prometheus-operator/prometheus-operator:v0.95.0
nerdctl pull quay.io/prometheus-operator/prometheus-config-reloader:v0.95.0

# Tag و Push
nerdctl tag quay.io/prometheus/prometheus:v3.12.0 rr.alefba2.ir/prometheus-stack/prometheus:v3.12.0
nerdctl tag quay.io/prometheus/alertmanager:v0.32.0 rr.alefba2.ir/prometheus-stack/alertmanager:v0.32.0
nerdctl tag quay.io/prometheus/node-exporter:v1.12.0 rr.alefba2.ir/prometheus-stack/node-exporter:v1.12.0
nerdctl tag quay.io/prometheus/pushgateway:v1.13.0 rr.alefba2.ir/prometheus-stack/pushgateway:v1.13.0
nerdctl tag docker.io/grafana/grafana:13.0.0 rr.alefba2.ir/prometheus-stack/grafana:13.0.0
nerdctl tag registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.20.0 rr.alefba2.ir/prometheus-stack/kube-state-metrics:v2.20.0
nerdctl tag quay.io/prometheus-operator/prometheus-operator:v0.95.0 rr.alefba2.ir/prometheus-stack/prometheus-operator:v0.95.0
nerdctl tag quay.io/prometheus-operator/prometheus-config-reloader:v0.95.0 rr.alefba2.ir/prometheus-stack/prometheus-config-reloader:v0.95.0

nerdctl push rr.alefba2.ir/prometheus-stack/prometheus:v3.12.0
nerdctl push rr.alefba2.ir/prometheus-stack/alertmanager:v0.32.0
nerdctl push rr.alefba2.ir/prometheus-stack/node-exporter:v1.12.0
nerdctl push rr.alefba2.ir/prometheus-stack/pushgateway:v1.13.0
nerdctl push rr.alefba2.ir/prometheus-stack/grafana:13.0.0
nerdctl push rr.alefba2.ir/prometheus-stack/kube-state-metrics:v2.20.0
nerdctl push rr.alefba2.ir/prometheus-stack/prometheus-operator:v0.95.0
nerdctl push rr.alefba2.ir/prometheus-stack/prometheus-config-reloader:v0.95.0

# Helm Chart
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm pull prometheus-community/kube-prometheus-stack --version 65.0.0
helm package kube-prometheus-stack-65.0.0.tgz
helm repo index . --url https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader -T ./kube-prometheus-stack-*.tgz https://mn.alefba2.ir/repository/helm-charts/
curl -u k8s-reader -T ./index.yaml https://mn.alefba2.ir/repository/helm-charts/
```

### 4.2. Loki Stack

| Image              | Version | Source    | Download Link                    | Push Command                                      |
|--------------------|---------|-----------|----------------------------------|---------------------------------------------------|
| `grafana/loki`     | `2.9.3` | docker.io | `docker.io/grafana/loki:3.6`     | `nerdctl push rr.alefba2.ir/grafana/loki:3.6`     |
| `grafana/promtail` | `2.9.3` | docker.io | `docker.io/grafana/promtail:3.6` | `nerdctl push rr.alefba2.ir/grafana/promtail:3.6` |

**Helm Chart:**

| Chart        | Repository                              | Version  | Download/Push               |
|--------------|-----------------------------------------|----------|-----------------------------|
| `loki-stack` | `https://grafana.github.io/helm-charts` | `2.10.2` | Push to Nexus `helm-charts` |

### 4.3. Tempo (Distributed Tracing)

| Image           | Version | Source    | Download Link                    | Push Command                                      |
|-----------------|---------|-----------|----------------------------------|---------------------------------------------------|
| `grafana/tempo` | `2.3.1` | docker.io | `docker.io/grafana/tempo:2.10.0` | `nerdctl push rr.alefba2.ir/grafana/tempo:2.10.0` |

**Helm Chart:**

| Chart   | Repository                              | Version | Download/Push               |
|---------|-----------------------------------------|---------|-----------------------------|
| `tempo` | `https://grafana.github.io/helm-charts` | `1.6.0` | Push to Nexus `helm-charts` |

### 4.4. Grafana Agent (اختیاری - برای آینده)

| Image           | Version   | Source    | Download Link                     | Push Command                                       |
|-----------------|-----------|-----------|-----------------------------------|----------------------------------------------------|
| `grafana/agent` | `v0.40.0` | docker.io | `docker.io/grafana/agent:v0.44.7` | `nerdctl push rr.alefba2.ir/grafana/agent:v0.44.7` |

**نکته:** Grafana Agent برای جمع‌آوری metrics و logs به صورت یکپارچه استفاده می‌شود. اختیاری است ولی برای آینده توصیه
می‌شود.

| Image           | Version | Source    | Download Link                    | Push Command                                      |
|-----------------|---------|-----------|----------------------------------|---------------------------------------------------|
| `grafana/tempo` | `2.3.1` | docker.io | `docker.io/grafana/tempo:2.10.0` | `nerdctl push rr.alefba2.ir/grafana/tempo:2.10.0` |

**Helm Chart:**

| Chart   | Repository                              | Version | Download/Push               |
|---------|-----------------------------------------|---------|-----------------------------|
| `tempo` | `https://grafana.github.io/helm-charts` | `1.6.0` | Push to Nexus `helm-charts` |

---

```bash
# 1. Loki Stack Imagess to match your stack
# Pull images
nerdctl pull docker.io/grafana/loki:3.6
nerdctl pull docker.io/grafana/promtail:3.6

# Tag images
nerdctl tag docker.io/grafana/loki:3.6 rr.alefba2.ir/grafana/loki:3.6
nerdctl tag docker.io/grafana/promtail:3.6 rr.alefba2.ir/grafana/promtail:3.6

# Push images
nerdctl push rr.alefba2.ir/grafana/loki:3.6
nerdctl push rr.alefba2.ir/grafana/promtail:3.6

# 2. Tempo Image
# Pull image
nerdctl pull docker.io/grafana/tempo:2.10.0

# Tag image
nerdctl tag docker.io/grafana/tempo:2.10.0 rr.alefba2.ir/grafana/tempo:2.10.0

# Push image
nerdctl push rr.alefba2.ir/grafana/tempo:2.10.0

# 3. Grafana Agent Image
# Pull image
nerdctl pull docker.io/grafana/agent:v0.44.7

# Tag image
nerdctl tag docker.io/grafana/agent:v0.44.7 rr.alefba2.ir/grafana/agent:v0.44.7

# Push image
nerdctl push rr.alefba2.ir/grafana/agent:v0.44.7

# 5. Helm Charts (unchanged)
# Add repositories
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Pull Loki Stack chart
helm pull grafana/loki --version 6.51.0
# Push to Nexus helm-charts repository

# Pull Tempo chart
helm pull grafana/tempo --version 1.24.4
# Push to Nexus helm-charts repository

# 6. Verification commands
# List all grafana images
nerdctl images | grep -E "(grafana|loki|promtail|tempo|agent)"

# List all prometheus images
nerdctl images | grep -E "(prometheus|alertmanager|node-exporter|pushgateway|kube-state-metrics)"

# List all tagged images for your registry
nerdctl images | grep rr.alefba2.ir

```

## Phase 5: Databases

### 5.1. CockroachDB

| Image                   | Version   | Source    | Download Link                              | Push Command                                                |
|-------------------------|-----------|-----------|--------------------------------------------|-------------------------------------------------------------|
| `cockroachdb/cockroach` | `v24.1.0` | docker.io | `docker.io/cockroachdb/cockroach:v24.3.25` | `nerdctl push rr.alefba2.ir/cockroachdb/cockroach:v24.3.25` |

**Manifest:**

| Manifest                       | Source | Download Link          | Push to Nexus           |
|--------------------------------|--------|------------------------|-------------------------|
| `cockroachdb-statefulset.yaml` | Custom | Create custom manifest | Push to `k8s-manifests` |

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
nerdctl pull docker.io/cockroachdb/cockroach:v24.3.25
nerdctl tag docker.io/cockroachdb/cockroach:v24.3.25 rr.alefba2.ir/cockroachdb/cockroach:v24.3.25
nerdctl push rr.alefba2.ir/cockroachdb/cockroach:v24.3.25

# ایجاد و push manifest
# (استفاده از manifest از Phase 10 در Kubernetes-Implementation-Guide)
curl -u k8s-reader --upload-file cockroachdb-statefulset.yaml https://mn.alefba2.ir/repository/k8s-manifests/databases/cockroachdb.yaml
```

### 5.2. ClickHouse

| Image                            | Version   | Source    | Download Link                                    | Push Command                                                      |
|----------------------------------|-----------|-----------|--------------------------------------------------|-------------------------------------------------------------------|
| `clickhouse/clickhouse-server`   | `25.12.2` | docker.io | `docker.io/clickhouse/clickhouse-server:25.12.2` | `nerdctl push rr.alefba2.ir/clickhouse/clickhouse-server:25.12.2` |
| `clickhouse/clickhouse-operator` | `0.26.0`  | docker.io | `docker.io/altinity/clickhouse-operator:0.26.0`  | `nerdctl push rr.alefba2.ir/altinity/clickhouse-operator:0.26.0`  |

**Helm Chart:**

| Chart                 | Repository                                        | Version  | Download/Push               |
|-----------------------|---------------------------------------------------|----------|-----------------------------|
| `clickhouse-operator` | `https://github.com/Altinity/clickhouse-operator` | `0.26.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull clickhouse/clickhouse-server:25.12.5
nerdctl tag clickhouse/clickhouse-server:25.12.5 rr.alefba2.ir/clickhouse/clickhouse-server:25.12.5
nerdctl push rr.alefba2.ir/clickhouse/clickhouse-server:25.12.5

nerdctl pull altinity/clickhouse-operator:0.26.0
nerdctl tag altinity/clickhouse-operator:0.26.0 rr.alefba2.ir/clickhouse/clickhouse-operator:0.26.0
nerdctl push rr.alefba2.ir/clickhouse/clickhouse-operator:0.26.0

```

### 5.3. Redis

| Image   | Version | Source    | Download Link                   | Push Command                                     |
|---------|---------|-----------|---------------------------------|--------------------------------------------------|
| `redis` | `8.4.0` | docker.io | `docker.io/library/redis:8.4.0` | `nerdctl push rr.alefba2.ir/library/redis:8.4.0` |

**Helm Chart:**

| Chart   | Repository                           | Version  | Download/Push               |
|---------|--------------------------------------|----------|-----------------------------|
| `redis` | `https://charts.bitnami.com/bitnami` | `19.1.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull redis:8.4.0
nerdctl tag redis:8.4.0 rr.alefba2.ir/library/redis:8.4.0
nerdctl push rr.alefba2.ir/library/redis:8.4.0
```

---

## Phase 6: Messaging

### 6.1. Redpanda (توصیه می‌شود)

| Image                   | Version   | Source    | Download Link                             | Push Command                                               |
|-------------------------|-----------|-----------|-------------------------------------------|------------------------------------------------------------|
| `redpandadata/redpanda` | `v24.1.1` | docker.io | `docker.io/redpandadata/redpanda:v25.3.6` | `nerdctl push rr.alefba2.ir/redpandadata/redpanda:v24.1.1` |
| `redpandadata/console`  | `v3.5.1`  | docker.io | `docker.io/redpandadata/console:v3.5.1`   | `nerdctl push rr.alefba2.ir/redpandadata/console:v2.5.0`   |

**Helm Chart:**

| Chart      | Repository                    | Version | Download/Push               |
|------------|-------------------------------|---------|-----------------------------|
| `redpanda` | `https://charts.redpanda.com` | `4.0.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull redpandadata/redpanda:v25.3.6
nerdctl pull redpandadata/console:v3.5.1

nerdctl tag redpandadata/redpanda:v25.3.6 rr.alefba2.ir/redpandadata/redpanda:v25.3.6
nerdctl tag redpandadata/console:v3.5.1 rr.alefba2.ir/redpandadata/console:v3.5.1

nerdctl push rr.alefba2.ir/redpandadata/redpanda:v25.3.6
nerdctl push rr.alefba2.ir/redpandadata/console:v3.5.1
```

### 6.2. Apache Kafka (جایگزین - کامل)

| Image                       | Version              | Source    | Download Link                               | Push Command                                                  |
|-----------------------------|----------------------|-----------|---------------------------------------------|---------------------------------------------------------------|
| `confluentinc/cp-kafka`     | `7.7.7`              | docker.io | `docker.io/confluentinc/cp-kafka:7.7.7`     | `nerdctl push rr.alefba2.ir/confluentinc/cp-kafka:7.7.7`      |
| `confluentinc/cp-zookeeper` | `7.6.0`              | docker.io | `docker.io/confluentinc/cp-zookeeper:7.7.7` | `nerdctl push rr.alefba2.ir/confluentinc/cp-zookeeper:7.7.7`  |
| `strimzi/kafka`             | `0.40.0-kafka-3.6.0` | quay.io   | `quay.io/strimzi/kafka:0.50.0-kafka-4.1.1`  | `nerdctl push rr.alefba2.ir/strimzi/kafka:0.50.0-kafka-4.1.1` |
| `strimzi/operator`          | `0.40.0`             | quay.io   | `quay.io/strimzi/operator:0.50.0`           | `nerdctl push rr.alefba2.ir/strimzi/operator:0.50.0`          |
| `danielqsj/kafka-exporter`  | `v1.8.0`             | docker.io | `docker.io/danielqsj/kafka-exporter:v1.9.0` | `nerdctl push rr.alefba2.ir/danielqsj/kafka-exporter:v1.9.0`  |

**Helm Chart:**

| Chart   | Repository                   | Version  | Download/Push               |
|---------|------------------------------|----------|-----------------------------|
| `kafka` | `https://strimzi.io/charts/` | `0.40.0` | Push to Nexus `helm-charts` |

**دستورات:**

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
nerdctl pull docker.io/confluentinc/cp-kafka:7.7.7
nerdctl pull docker.io/confluentinc/cp-zookeeper:7.7.7
nerdctl pull quay.io/strimzi/kafka:0.50.0-kafka-4.1.1
nerdctl pull quay.io/strimzi/operator:0.50.0
nerdctl pull docker.io/danielqsj/kafka-exporter:v1.9.0

# Tag و Push
nerdctl tag docker.io/confluentinc/cp-kafka:7.7.7 rr.alefba2.ir/confluentinc/cp-kafka:7.7.7
nerdctl tag docker.io/confluentinc/cp-zookeeper:7.7.7 rr.alefba2.ir/confluentinc/cp-zookeeper:7.7.7
nerdctl tag quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 rr.alefba2.ir/strimzi/kafka:0.50.0-kafka-4.1.1
nerdctl tag quay.io/strimzi/operator:0.50.0 rr.alefba2.ir/strimzi/operator:0.50.0
nerdctl tag docker.io/danielqsj/kafka-exporter:v1.9.0 rr.alefba2.ir/danielqsj/kafka-exporter:v1.9.0

nerdctl push rr.alefba2.ir/confluentinc/cp-kafka:7.7.7
nerdctl push rr.alefba2.ir/confluentinc/cp-zookeeper:7.7.7
nerdctl push rr.alefba2.ir/strimzi/kafka:0.50.0-kafka-4.1.1
nerdctl push rr.alefba2.ir/strimzi/operator:0.50.0
nerdctl push rr.alefba2.ir/danielqsj/kafka-exporter:v1.9.0
```

---

## Phase 7: Security

### 7.1. Keycloak

| Image                       | Version  | Source  | Download Link                      | Push Command                                          |
|-----------------------------|----------|---------|------------------------------------|-------------------------------------------------------|
| `quay.io/keycloak/keycloak` | `25.0.4` | quay.io | `quay.io/keycloak/keycloak:25.0.4` | `nerdctl push rr.alefba2.ir/keycloak/keycloak:25.0.4` |

**Helm Chart:**

| Chart      | Repository                                  | Version  | Download/Push               |
|------------|---------------------------------------------|----------|-----------------------------|
| `keycloak` | `https://codecentric.github.io/helm-charts` | `25.0.4` | Push to Nexus `helm-charts` |

```bash
nerdctl pull quay.io/keycloak/keycloak:26.5.2
nerdctl tag quay.io/keycloak/keycloak:26.5.2 rr.alefba2.ir/keycloak/keycloak:26.5.2
nerdctl push rr.alefba2.ir/keycloak/keycloak:26.5.2

helm repo add codecentric https://codecentric.github.io/helm-charts
helm pull codecentric/keycloak --version 26.5.2
helm package keycloak-26.5.2.tgz --destination ./helm-charts
helm push keycloak-26.5.2.tgz nexus-repo
```

### 7.2. Trivy Operator

> **نکته نسخه و رجیستری:** ایمیج Trivy Operator در نسخه‌های جدید به GitHub Container Registry منتقل شده است و همهٔ تگ‌ها
> روی Docker Hub (`docker.io/aquasec/trivy-operator`) منتشر نمی‌شوند. برای همسانی با اسکریپت Helm در همین فایل، از نسخهٔ
> پایدار `0.31.0` روی Docker Hub استفاده می‌کنیم.

| Image                    | Version  | Source    | Download Link                             | Push Command                                               |
|--------------------------|----------|-----------|-------------------------------------------|------------------------------------------------------------|
| `aquasec/trivy-operator` | `0.31.0` | docker.io | `docker.io/aquasec/trivy-operator:0.31.0` | `nerdctl push rr.alefba2.ir/aquasec/trivy-operator:0.31.0` |

**Helm Chart:**

| Chart            | Repository                                   | Version  | Download/Push               |
|------------------|----------------------------------------------|----------|-----------------------------|
| `trivy-operator` | `https://aquasecurity.github.io/helm-charts` | `0.31.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull aquasec/trivy-operator:0.31.0
nerdctl tag aquasec/trivy-operator:0.31.0 rr.alefba2.ir/aquasec/trivy-operator:0.31.0
nerdctl push rr.alefba2.ir/aquasec/trivy-operator:0.31.0

helm repo add aqua https://aquasecurity.github.io/helm-charts
helm pull aqua/trivy-operator --version 0.31.0
helm package trivy-operator-0.31.0.tgz --destination ./helm-charts
helm push trivy-operator-0.31.0.tgz nexus-repo
```

### 7.3. Falco

| Image                         | Version  | Source    | Download Link                                 | Push Command                                                   |
|-------------------------------|----------|-----------|-----------------------------------------------|----------------------------------------------------------------|
| `falcosecurity/falco`         | `0.40.0` | docker.io | `docker.io/falcosecurity/falco:0.40.0`        | `nerdctl push rr.alefba2.ir/falcosecurity/falco:0.40.0`        |
| `falcosecurity/falcosidekick` | `2.6.0`  | docker.io | `docker.io/falcosecurity/falcosidekick:2.6.0` | `nerdctl push rr.alefba2.ir/falcosecurity/falcosidekick:2.6.0` |

**Helm Chart:**

| Chart   | Repository                               | Version | Download/Push               |
|---------|------------------------------------------|---------|-----------------------------|
| `falco` | `https://falcosecurity.github.io/charts` | `4.0.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull falcosecurity/falco:0.43.0
nerdctl pull falcosecurity/falcosidekick:2.32.0

nerdctl tag falcosecurity/falco:0.43.0 rr.alefba2.ir/falcosecurity/falco:0.43.0
nerdctl tag falcosecurity/falcosidekick:2.32.0 rr.alefba2.ir/falcosecurity/falcosidekick:2.32.0

nerdctl push rr.alefba2.ir/falcosecurity/falco:0.43.0
nerdctl push rr.alefba2.ir/falcosecurity/falcosidekick:2.32.0

helm repo add falcosecurity https://falcosecurity.github.io/charts
helm pull falcosecurity/falco --version 8.0.0
helm package falco-8.0.0.tgz --destination ./helm-charts
helm push falco-8.0.0.tgz nexus-repo

```

### 7.4. OPA Gatekeeper (Policy & Admission Control)

| Image                        | Version   | Source    | Download Link                                  | Push Command                                                    |
|------------------------------|-----------|-----------|------------------------------------------------|-----------------------------------------------------------------|
| `openpolicyagent/gatekeeper` | `v3.15.0` | docker.io | `docker.io/openpolicyagent/gatekeeper:v3.15.0` | `nerdctl push rr.alefba2.ir/openpolicyagent/gatekeeper:v3.15.0` |

**Helm Chart:**

| Chart        | Repository                                              | Version   | Download/Push               |
|--------------|---------------------------------------------------------|-----------|-----------------------------|
| `gatekeeper` | `https://open-policy-agent.github.io/gatekeeper/charts` | `v3.15.0` | Push to Nexus `helm-charts` |

**نکته:** OPA Gatekeeper برای Policy Enforcement و Admission Control ضروری است. جایگزین ساده‌تر: **Kyverno** (در زیر).

```bash
nerdctl pull openpolicyagent/gatekeeper:v3.21.0
nerdctl tag openpolicyagent/gatekeeper:v3.21.0 rr.alefba2.ir/openpolicyagent/gatekeeper:v3.21.0
nerdctl push rr.alefba2.ir/openpolicyagent/gatekeeper:v3.21.0

helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm pull gatekeeper/gatekeeper --version 3.21.0
helm package gatekeeper-3.21.0.tgz --destination ./helm-charts
helm push gatekeeper-3.21.0.tgz nexus-repo

```

### 7.5. Kyverno (جایگزین ساده‌تر برای OPA)

| Image                | Version   | Source    | Download Link                          | Push Command                                            |
|----------------------|-----------|-----------|----------------------------------------|---------------------------------------------------------|
| `kyverno/kyverno`    | `v1.12.2` | docker.io | `docker.io/kyverno/kyverno:v1.12.2`    | `nerdctl push rr.alefba2.ir/kyverno/kyverno:v1.12.2`    |
| `kyverno/kyvernopre` | `v1.12.2` | docker.io | `docker.io/kyverno/kyvernopre:v1.12.2` | `nerdctl push rr.alefba2.ir/kyverno/kyvernopre:v1.12.2` |

**Helm Chart:**

| Chart     | Repository                           | Version  | Download/Push               |
|-----------|--------------------------------------|----------|-----------------------------|
| `kyverno` | `https://kyverno.github.io/kyverno/` | `v3.3.0` | Push to Nexus `helm-charts` |

**نکته:** Kyverno ساده‌تر از OPA Gatekeeper است و برای Policy Management در Kubernetes توصیه می‌شود. حداقل یکی از این
دو (OPA یا Kyverno) برای Production ضروری است.

```bash
nerdctl pull ghcr.io/kyverno/kyverno:v1.17.0
nerdctl pull ghcr.io/kyverno/kyvernopre:v1.17.0

nerdctl tag ghcr.io/kyverno/kyverno:v1.17.0 rr.alefba2.ir/kyverno/kyverno:v1.17.0
nerdctl tag ghcr.io/kyverno/kyvernopre:v1.17.0 rr.alefba2.ir/kyverno/kyvernopre:v1.17.0

nerdctl push rr.alefba2.ir/kyverno/kyverno:v1.17.0
nerdctl push rr.alefba2.ir/kyverno/kyvernopre:v1.17.0

helm repo add kyverno https://kyverno.github.io/kyverno/
helm pull kyverno/kyverno --version v3.3.0
helm package kyverno-v3.3.0.tgz --destination ./helm-charts
helm push kyverno-v3.3.0.tgz nexus-repo
```

### 7.6. OWASP ZAP (Zed Attack Proxy)

**⚠ مهم**: OWASP ZAP برای تست نفوذ خودکار و security scanning استفاده می‌شود. برای جزئیات کامل،
به [راهنمای جامع OWASP](Security-OWASP-Comprehensive-Guide) مراجعه کنید.

**نکته:** تصویر `owasp/zap2docker` در Docker Hub قدیمی است. از نسخه رسمی در GitHub Container Registry استفاده می‌کنیم.

| Image             | Version  | Source  | Download Link                    | Push Command                                        |
|-------------------|----------|---------|----------------------------------|-----------------------------------------------------|
| `zaproxy/zaproxy` | `stable` | ghcr.io | `ghcr.io/zaproxy/zaproxy:stable` | `nerdctl push rr.alefba2.ir/zaproxy/zaproxy:stable` |
| `zaproxy/zaproxy` | `latest` | ghcr.io | `ghcr.io/zaproxy/zaproxy:latest` | `nerdctl push rr.alefba2.ir/zaproxy/zaproxy:latest` |
| `zaproxy/zaproxy` | `2.14.0` | ghcr.io | `ghcr.io/zaproxy/zaproxy:2.14.0` | `nerdctl push rr.alefba2.ir/zaproxy/zaproxy:2.14.0` |

**نکته:** OWASP ZAP معمولاً به صورت Job یا CronJob در Kubernetes اجرا می‌شود و نیازی به Helm Chart ندارد.

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
# استفاده از نسخه stable (توصیه می‌شود)
nerdctl pull ghcr.io/zaproxy/zaproxy:stable

nerdctl tag ghcr.io/zaproxy/zaproxy:stable rr.alefba2.ir/zaproxy/zaproxy:stable

nerdctl push rr.alefba2.ir/zaproxy/zaproxy:stable

# یا استفاده از نسخه مشخص (2.14.0)
nerdctl pull ghcr.io/zaproxy/zaproxy:2.14.0
nerdctl tag ghcr.io/zaproxy/zaproxy:2.14.0 rr.alefba2.ir/zaproxy/zaproxy:2.14.0
nerdctl push rr.alefba2.ir/zaproxy/zaproxy:2.14.0

# استفاده در Kubernetes Job (مثال)
cat <<EOF | kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: zap-scan
  namespace: security
spec:
  template:
    spec:
      containers:
      - name: zap
        image: rr.alefba2.ir/zaproxy/zaproxy:stable
        command:
        - zap-baseline.py
        - -t
        - http://your-app:8080
        - -J
        - /tmp/zap-report.json
        volumeMounts:
        - name: zap-reports
          mountPath: /tmp
      volumes:
      - name: zap-reports
        emptyDir: {}
      restartPolicy: Never
EOF
```

---

## Phase 8: Infrastructure Tools

### 8.1. Jira Data Center

| Image                     | Version  | Source    | Download Link                              | Push Command                                                |
|---------------------------|----------|-----------|--------------------------------------------|-------------------------------------------------------------|
| `atlassian/jira-software` | `9.28.0` | docker.io | `docker.io/atlassian/jira-software:9.28.0` | `nerdctl push rr.alefba2.ir/atlassian/jira-software:9.28.0` |

**Helm Chart:**

| Chart  | Repository                                            | Version | Download/Push               |
|--------|-------------------------------------------------------|---------|-----------------------------|
| `jira` | `https://atlassian.github.io/data-center-helm-charts` | `2.2.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull atlassian/jira-software:9.28.0
nerdctl tag atlassian/jira-software:9.28.0 rr.alefba2.ir/atlassian/jira-software:9.28.0
nerdctl push rr.alefba2.ir/atlassian/jira-software:9.28.0

helm repo add atlassian https://atlassian.github.io/data-center-helm-charts
helm pull atlassian/jira --version 2.2.0
helm package jira-2.2.0.tgz --destination ./helm-charts
helm push jira-2.2.0.tgz nexus-repo
```

### 8.2. Confluence Data Center

| Image                  | Version | Source    | Download Link                          | Push Command                                            |
|------------------------|---------|-----------|----------------------------------------|---------------------------------------------------------|
| `atlassian/confluence` | `9.3.0` | docker.io | `docker.io/atlassian/confluence:9.3.0` | `nerdctl push rr.alefba2.ir/atlassian/confluence:9.3.0` |

**Helm Chart:**

| Chart        | Repository                                            | Version | Download/Push               |
|--------------|-------------------------------------------------------|---------|-----------------------------|
| `confluence` | `https://atlassian.github.io/data-center-helm-charts` | `2.2.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull atlassian/confluence:9.3.0
nerdctl tag atlassian/confluence:9.3.0 rr.alefba2.ir/atlassian/confluence:9.3.0
nerdctl push rr.alefba2.ir/atlassian/confluence:9.3.0

helm repo add atlassian https://atlassian.github.io/data-center-helm-charts
helm pull atlassian/confluence --version 2.2.0
helm package confluence-2.2.0.tgz --destination ./helm-charts
helm push confluence-2.2.0.tgz nexus-repo

```

### 8.3. GitLab

| Image                  | Version       | Source    | Download Link                            | Push Command                                              |
|------------------------|---------------|-----------|------------------------------------------|-----------------------------------------------------------|
| `gitlab/gitlab-ce`     | `19.0.0-ce.0` | docker.io | `docker.io/gitlab/gitlab-ce:19.0.0-ce.0` | `nerdctl push rr.alefba2.ir/gitlab/gitlab-ce:19.0.0-ce.0` |
| `gitlab/gitlab-runner` | `v19.0.0`     | docker.io | `docker.io/gitlab/gitlab-runner:v19.0.0` | `nerdctl push rr.alefba2.ir/gitlab/gitlab-runner:v19.0.0` |

**Helm Chart:**

| Chart    | Repository                 | Version | Download/Push               |
|----------|----------------------------|---------|-----------------------------|
| `gitlab` | `https://charts.gitlab.io` | `9.0.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull gitlab/gitlab-ce:19.0.0-ce.0
nerdctl pull gitlab/gitlab-runner:v19.0.0

nerdctl tag gitlab/gitlab-ce:19.0.0-ce.0 rr.alefba2.ir/gitlab/gitlab-ce:19.0.0-ce.0
nerdctl tag gitlab/gitlab-runner:v19.0.0 rr.alefba2.ir/gitlab/gitlab-runner:v19.0.0

nerdctl push rr.alefba2.ir/gitlab/gitlab-ce:19.0.0-ce.0
nerdctl push rr.alefba2.ir/gitlab/gitlab-runner:v19.0.0

helm repo add gitlab https://charts.gitlab.io
helm pull gitlab/gitlab --version 9.0.0
helm package gitlab-9.0.0.tgz --destination ./helm-charts
helm push gitlab-9.0.0.tgz nexus-repo

```

### 8.4. Jenkins

| Image             | Version       | Source    | Download Link                           | Push Command                                             |
|-------------------|---------------|-----------|-----------------------------------------|----------------------------------------------------------|
| `jenkins/jenkins` | `2.480-jdk17` | docker.io | `docker.io/jenkins/jenkins:2.480-jdk17` | `nerdctl push rr.alefba2.ir/jenkins/jenkins:2.480-jdk17` |

**Helm Chart:**

| Chart     | Repository                  | Version | Download/Push               |
|-----------|-----------------------------|---------|-----------------------------|
| `jenkins` | `https://charts.jenkins.io` | `5.6.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull jenkins/jenkins:2.480-jdk17
nerdctl tag jenkins/jenkins:2.480-jdk17 rr.alefba2.ir/jenkins/jenkins:2.480-jdk17
nerdctl push rr.alefba2.ir/jenkins/jenkins:2.480-jdk17

helm repo add jenkins https://charts.jenkins.io
helm pull jenkins/jenkins --version 5.6.0
helm package jenkins-5.6.0.tgz --destination ./helm-charts
helm push jenkins-5.6.0.tgz nexus-repo

```

### 8.5. Nextcloud

| Image       | Version         | Source    | Download Link                               | Push Command                                                 |
|-------------|-----------------|-----------|---------------------------------------------|--------------------------------------------------------------|
| `nextcloud` | `30.0.0-apache` | docker.io | `docker.io/library/nextcloud:30.0.0-apache` | `nerdctl push rr.alefba2.ir/library/nextcloud:30.0.0-apache` |

**Helm Chart:**

| Chart       | Repository                          | Version | Download/Push               |
|-------------|-------------------------------------|---------|-----------------------------|
| `nextcloud` | `https://nextcloud.github.io/helm/` | `2.3.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull nextcloud:30.0.0-apache
nerdctl tag nextcloud:30.0.0-apache rr.alefba2.ir/library/nextcloud:30.0.0-apache
nerdctl push rr.alefba2.ir/library/nextcloud:30.0.0-apache

helm repo add nextcloud https://nextcloud.github.io/helm/
helm pull nextcloud/nextcloud --version 2.3.0
helm package nextcloud-2.3.0.tgz --destination ./helm-charts
helm push nextcloud-2.3.0.tgz nexus-repo

```

### 8.6. Mayan EDMS

| Image                 | Version | Source    | Download Link                          | Push Command                                            |
|-----------------------|---------|-----------|----------------------------------------|---------------------------------------------------------|
| `mayanedms/mayanedms` | `5.2.0` | docker.io | `docker.io/mayanedms/mayanedms:v4.9.8` | `nerdctl push rr.alefba2.ir/mayanedms/mayanedms:v4.9.8` |

```bash
nerdctl pull mayanedms/mayanedms:v4.9.8
nerdctl tag mayanedms/mayanedms:v4.9.8 rr.alefba2.ir/mayanedms/mayanedms:v4.9.8
nerdctl push rr.alefba2.ir/mayanedms/mayanedms:v4.9.8
```

---

## Phase 9: Application Services

### 9.1. Java Spring Boot Base Images

| Image             | Version         | Source    | Download Link                                     | Push Command                                                       |
|-------------------|-----------------|-----------|---------------------------------------------------|--------------------------------------------------------------------|
| `eclipse-temurin` | `21-jdk-alpine` | docker.io | `docker.io/library/eclipse-temurin:21-jdk-alpine` | `nerdctl push rr.alefba2.ir/library/eclipse-temurin:21-jdk-alpine` |
| `eclipse-temurin` | `21-jre-alpine` | docker.io | `docker.io/library/eclipse-temurin:21-jre-alpine` | `nerdctl push rr.alefba2.ir/library/eclipse-temurin:21-jre-alpine` |
| `distroless/java` | `21-nonroot`    | gcr.io    | `gcr.io/distroless/java21:nonroot`                | `nerdctl push rr.alefba2.ir/distroless/java21:nonroot`             |

```bash
nerdctl pull eclipse-temurin:21-jdk-alpine
nerdctl pull eclipse-temurin:21-jre-alpine
nerdctl pull gcr.io/distroless/java21:nonroot

nerdctl tag eclipse-temurin:21-jdk-alpine rr.alefba2.ir/library/eclipse-temurin:21-jdk-alpine
nerdctl tag eclipse-temurin:21-jre-alpine rr.alefba2.ir/library/eclipse-temurin:21-jre-alpine
nerdctl tag gcr.io/distroless/java21:nonroot rr.alefba2.ir/distroless/java21:nonroot

nerdctl push rr.alefba2.ir/library/eclipse-temurin:21-jdk-alpine
nerdctl push rr.alefba2.ir/library/eclipse-temurin:21-jre-alpine
nerdctl push rr.alefba2.ir/distroless/java21:nonroot
```

### 9.2. Node.js Base Images (برای Puppeteer Service)

| Image  | Version     | Source    | Download Link                      | Push Command                                        |
|--------|-------------|-----------|------------------------------------|-----------------------------------------------------|
| `node` | `20-alpine` | docker.io | `docker.io/library/node:20-alpine` | `nerdctl push rr.alefba2.ir/library/node:20-alpine` |
| `node` | `20-slim`   | docker.io | `docker.io/library/node:20-slim`   | `nerdctl push rr.alefba2.ir/library/node:20-slim`   |

```bash
nerdctl pull node:20-alpine
nerdctl pull node:20-slim

nerdctl tag node:20-alpine rr.alefba2.ir/library/node:20-alpine
nerdctl tag node:20-slim rr.alefba2.ir/library/node:20-slim

nerdctl push rr.alefba2.ir/library/node:20-alpine
nerdctl push rr.alefba2.ir/library/node:20-slim
```

### 9.3. Nginx (برای Frontend)

| Image   | Version       | Source    | Download Link                         | Push Command                                           |
|---------|---------------|-----------|---------------------------------------|--------------------------------------------------------|
| `nginx` | `1.29-alpine` | docker.io | `docker.io/library/nginx:1.29-alpine` | `nerdctl push rr.alefba2.ir/library/nginx:1.29-alpine` |

**نکته:** نسخه 1.29 آخرین نسخه stable برای سال 2026 است.

```bash
nerdctl pull nginx:1.29-alpine
nerdctl tag nginx:1.29-alpine rr.alefba2.ir/library/nginx:1.29-alpine
nerdctl push rr.alefba2.ir/library/nginx:1.29-alpine
```

### 9.4. Base Images اضافی (برای Utility)

| Image     | Version | Source    | Download Link                    | Push Command                                      |
|-----------|---------|-----------|----------------------------------|---------------------------------------------------|
| `busybox` | `1.36`  | docker.io | `docker.io/library/busybox:1.36` | `nerdctl push rr.alefba2.ir/library/busybox:1.36` |
| `alpine`  | `3.22`  | docker.io | `docker.io/library/alpine:3.22`  | `nerdctl push rr.alefba2.ir/library/alpine:3.22`  |

**نکته:** این base images برای debugging و utility containers مفید هستند.

```bash
nerdctl pull busybox:1.36
nerdctl pull alpine:3.22

nerdctl tag busybox:1.36 rr.alefba2.ir/library/busybox:1.36
nerdctl tag alpine:3.22 rr.alefba2.ir/library/alpine:3.22

nerdctl push rr.alefba2.ir/library/busybox:1.36
nerdctl push rr.alefba2.ir/library/alpine:3.22
```

---

## Phase 10: CI/CD Tools

### 10.1. ArgoCD

| Image                            | Version          | Source    | Download Link                                               | Push Command                                                                   |
|----------------------------------|------------------|-----------|-------------------------------------------------------------|--------------------------------------------------------------------------------|
| `argoproj/argocd`                | `SET_AT_INSTALL` | quay.io   | `quay.io/argoproj/argocd:<ARGOCD_TAG>`                      | `nerdctl push rr.alefba2.ir/argoproj/argocd:<ARGOCD_TAG>`                      |
| `argoproj/argocd-repo-server`    | `SET_AT_INSTALL` | quay.io   | `quay.io/argoproj/argocd-repo-server:<ARGOCD_TAG>`          | `nerdctl push rr.alefba2.ir/argoproj/argocd-repo-server:<ARGOCD_TAG>`          |
| `argoproj/argocd-applicationset` | `SET_AT_INSTALL` | quay.io   | `quay.io/argoproj/argocd-applicationset:<APPSET_TAG>`       | `nerdctl push rr.alefba2.ir/argoproj/argocd-applicationset:<APPSET_TAG>`       |
| `argoproj/argocd-image-updater`  | `SET_AT_INSTALL` | quay.io   | `quay.io/argoproj/argocd-image-updater:<IMAGE_UPDATER_TAG>` | `nerdctl push rr.alefba2.ir/argoproj/argocd-image-updater:<IMAGE_UPDATER_TAG>` |
| `argoproj/argocd-notifications`  | *(استفاده نشود)* | quay.io   | –                                                           | –                                                                              |
| `argoproj/argocd-rollouts`       | `SET_AT_INSTALL` | quay.io   | `quay.io/argoproj/argocd-rollouts:<ROLLOUTS_TAG>`           | `nerdctl push rr.alefba2.ir/argoproj/argocd-rollouts:<ROLLOUTS_TAG>`           |
| `redis`                          | `7.2-alpine`     | docker.io | `docker.io/library/redis:7.2-alpine`                        | (قبلاً push شده)                                                               |

> **هشدار:** نسخه‌های مثال `v3.8.0`، `v0.18.0` و `v2.18.0` برای کامپوننت‌های ArgoCD در quay.io هنوز منتشر نشده‌اند و
`docker pull` برای آن‌ها خطای `not found` یا `401 UNAUTHORIZED` برمی‌گرداند. برای هر کلاستر، مطابق مستندات رسمی ArgoCD و
> نسخهٔ Helm chart مورد استفاده، تگ‌های واقعی (`<ARGOCD_TAG>`، `<APPSET_TAG>`، `<IMAGE_UPDATER_TAG>`، `<ROLLOUTS_TAG>`)
> را
> انتخاب و در این جدول و اسکریپت‌ها جایگزین کن. ایمیج قدیمی `argocd-notifications` دیگر استفاده نمی‌شود و کنترلر/بات
> نوتیفیکیشن در پایین اسکریپت اضافه شده‌اند.

**Helm Chart:**

| Chart     | Repository                             | Version  | Download/Push               |
|-----------|----------------------------------------|----------|-----------------------------|
| `argo-cd` | `https://argoproj.github.io/argo-helm` | `10.2.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull quay.io/argoproj/argocd:v3.8.0
nerdctl pull quay.io/argoproj/argocd-repo-server:v3.8.0
nerdctl pull quay.io/argoproj/argocd-applicationset:v0.18.0
nerdctl pull quay.io/argoproj/argocd-image-updater:v0.18.0
nerdctl pull quay.io/argoproj/argocd-notifications:v3.8.0
nerdctl pull quay.io/argoproj/argocd-rollouts:v2.18.0

nerdctl tag quay.io/argoproj/argocd:v3.8.0 rr.alefba2.ir/argoproj/argocd:v3.8.0
nerdctl tag quay.io/argoproj/argocd-repo-server:v3.8.0 rr.alefba2.ir/argoproj/argocd-repo-server:v3.8.0
nerdctl tag quay.io/argoproj/argocd-applicationset:v0.18.0 rr.alefba2.ir/argoproj/argocd-applicationset:v0.18.0
nerdctl tag quay.io/argoproj/argocd-image-updater:v0.18.0 rr.alefba2.ir/argoproj/argocd-image-updater:v0.18.0
nerdctl tag quay.io/argoproj/argocd-notifications:v3.8.0 rr.alefba2.ir/argoproj/argocd-notifications:v3.8.0
nerdctl tag quay.io/argoproj/argocd-rollouts:v2.18.0 rr.alefba2.ir/argoproj/argocd-rollouts:v2.18.0

nerdctl push rr.alefba2.ir/argoproj/argocd:v3.8.0
nerdctl push rr.alefba2.ir/argoproj/argocd-repo-server:v3.8.0
nerdctl push rr.alefba2.ir/argoproj/argocd-applicationset:v0.18.0
nerdctl push rr.alefba2.ir/argoproj/argocd-image-updater:v0.18.0
nerdctl push rr.alefba2.ir/argoproj/argocd-notifications:v3.8.0
nerdctl push rr.alefba2.ir/argoproj/argocd-rollouts:v2.18.0

helm repo add argo https://argoproj.github.io/argo-helm
helm pull argo/argo-cd --version 10.2.0
helm package argo-cd-10.2.0.tgz --destination ./helm-charts
helm push argo-cd-10.2.0.tgz nexus-repo
```

### 10.2. Spring Boot Admin

| Image                           | Version  | Source    | Download Link                                   | Push Command                                                     |
|---------------------------------|----------|-----------|-------------------------------------------------|------------------------------------------------------------------|
| `codecentric/spring-boot-admin` | `2.11.0` | docker.io | `docker.io/codecentric/spring-boot-admin:2.6.7` | `nerdctl push rr.alefba2.ir/codecentric/spring-boot-admin:2.6.7` |

```bash
nerdctl pull codecentric/spring-boot-admin:2.6.7
nerdctl tag codecentric/spring-boot-admin:2.6.7 rr.alefba2.ir/codecentric/spring-boot-admin:2.6.7
nerdctl push rr.alefba2.ir/codecentric/spring-boot-admin:2.6.7
```

---

## Phase 11: Backup و Disaster Recovery

### 11.1. Velero

> **نکته نسخه:** نسخهٔ `v1.18.2` و پلاگین `v0.10.0` در حال حاضر در Docker Hub موجود نیستند و `docker pull` برای آن‌ها
> خطای `not found` می‌دهد. برای همخوانی با نسخهٔ Helm chart (`6.3.0`) و وضعیت فعلی Velero، از نسخهٔ پایدار `v1.13.0` و
> پلاگین‌های متناظر استفاده می‌کنیم.

| Image                            | Version   | Source    | Download Link                                     | Push Command                                                       |
|----------------------------------|-----------|-----------|---------------------------------------------------|--------------------------------------------------------------------|
| `velero/velero`                  | `v1.13.0` | docker.io | `docker.io/velero/velero:v1.13.0`                 | `nerdctl push rr.alefba2.ir/velero/velero:v1.13.0`                 |
| `velero/velero-plugin-for-aws`   | `v1.13.0` | docker.io | `docker.io/velero/velero-plugin-for-aws:v1.13.0`  | `nerdctl push rr.alefba2.ir/velero/velero-plugin-for-aws:v1.13.0`  |
| `velero/velero-plugin-for-gcp`   | `v1.13.0` | docker.io | `docker.io/velero/velero-plugin-for-gcp:v1.13.0`  | `nerdctl push rr.alefba2.ir/velero/velero-plugin-for-gcp:v1.13.0`  |
| `velero/velero-plugin-for-csi`   | `v0.7.0`  | docker.io | `docker.io/velero/velero-plugin-for-csi:v0.7.0`   | `nerdctl push rr.alefba2.ir/velero/velero-plugin-for-csi:v0.7.0`   |
| `velero/velero-plugin-for-local` | `v0.1.0`  | docker.io | `docker.io/velero/velero-plugin-for-local:v0.1.0` | `nerdctl push rr.alefba2.ir/velero/velero-plugin-for-local:v0.1.0` |

**نکته:** Velero plugins بسته به storage backend شما انتخاب می‌شوند. `velero-plugin-for-csi` برای CSI snapshots ضروری
است.

**Helm Chart:**

| Chart    | Repository                                   | Version | Download/Push               |
|----------|----------------------------------------------|---------|-----------------------------|
| `velero` | `https://vmware-tanzu.github.io/helm-charts` | `6.3.0` | Push to Nexus `helm-charts` |

```bash
nerdctl pull velero/velero:v1.13.0
nerdctl pull velero/velero-plugin-for-aws:v1.13.0
nerdctl pull velero/velero-plugin-for-gcp:v1.13.0
nerdctl pull velero/velero-plugin-for-csi:v0.7.0
# Note: velero-plugin-for-local may not be available in Docker Hub, check GitHub releases if needed

nerdctl tag velero/velero:v1.13.0 rr.alefba2.ir/velero/velero:v1.13.0
nerdctl tag velero/velero-plugin-for-aws:v1.13.0 rr.alefba2.ir/velero/velero-plugin-for-aws:v1.13.0
nerdctl tag velero/velero-plugin-for-gcp:v1.13.0 rr.alefba2.ir/velero/velero-plugin-for-gcp:v1.13.0
nerdctl tag velero/velero-plugin-for-csi:v0.7.0 rr.alefba2.ir/velero/velero-plugin-for-csi:v0.7.0

nerdctl push rr.alefba2.ir/velero/velero:v1.13.0
nerdctl push rr.alefba2.ir/velero/velero-plugin-for-aws:v1.13.0
nerdctl push rr.alefba2.ir/velero/velero-plugin-for-gcp:v1.13.0
nerdctl push rr.alefba2.ir/velero/velero-plugin-for-csi:v0.7.0

helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm pull vmware-tanzu/velero --version 6.3.0
helm package velero-6.3.0.tgz --destination ./helm-charts
helm push velero-6.3.0.tgz nexus-repo
```

### 11.2. PostgreSQL (برای Mayan EDMS و برخی سرویس‌ها)

| Image      | Version     | Source    | Download Link                          | Push Command                                            |
|------------|-------------|-----------|----------------------------------------|---------------------------------------------------------|
| `postgres` | `16-alpine` | docker.io | `docker.io/library/postgres:16-alpine` | `nerdctl push rr.alefba2.ir/library/postgres:16-alpine` |
| `postgres` | `15-alpine` | docker.io | `docker.io/library/postgres:15-alpine` | `nerdctl push rr.alefba2.ir/library/postgres:15-alpine` |

```bash
nerdctl pull postgres:16-alpine
nerdctl pull postgres:15-alpine

nerdctl tag postgres:16-alpine rr.alefba2.ir/library/postgres:16-alpine
nerdctl tag postgres:15-alpine rr.alefba2.ir/library/postgres:15-alpine

nerdctl push rr.alefba2.ir/library/postgres:16-alpine
nerdctl push rr.alefba2.ir/library/postgres:15-alpine
```

---

## ترتیب استفاده (Installation Order)

### مرحله 0: آماده‌سازی Registry و Nexus

1. **نصب و راه‌اندازی Registry** (روی سرور `registry` - Free internet)
2. **نصب و راه‌اندازی Nexus** (روی سرور `registry` - Free internet)
3. **Push تمام images و charts به Registry و Nexus**

### مرحله 1: Kubernetes Core

1. Pull و Push **Kubernetes Core Images** (Phase 1)
2. Initialize **Kubernetes Cluster** با استفاده از registry محلی
3. Join **Worker Nodes**

### مرحله 2: Networking

1. Pull و Push **Calico Images** (Phase 2)
2. نصب **Calico CNI** با استفاده از Helm chart از Nexus

### مرحله 3: Core Add-ons

1. Pull و Push **Metrics Server** (Phase 3.1)
2. Pull و Push **Ingress NGINX** (Phase 3.2)
3. Pull و Push **cert-manager** (Phase 3.3)
4. نصب با استفاده از Helm charts از Nexus

### مرحله 4: Monitoring

1. Pull و Push **Prometheus Stack Images** (Phase 4.1)
2. Pull و Push **Loki Stack Images** (Phase 4.2)
3. Pull و Push **Tempo Images** (Phase 4.3)
4. نصب با استفاده از Helm charts از Nexus

### مرحله 5: Databases

1. Pull و Push **CockroachDB** (Phase 5.1)
2. Pull و Push **ClickHouse** (Phase 5.2)
3. Pull و Push **Redis** (Phase 5.3)
4. Deploy با استفاده از manifests/charts از Nexus

### مرحله 6: Messaging

1. Pull و Push **Redpanda** (Phase 6.1) - توصیه می‌شود
2. یا Pull و Push **Kafka** (Phase 6.2)
3. Deploy با استفاده از Helm charts از Nexus

### مرحله 7: Security

1. Pull و Push **Keycloak** (Phase 7.1)
2. Pull و Push **Trivy Operator** (Phase 7.2)
3. Pull و Push **Falco** (Phase 7.3)
4. Deploy با استفاده از Helm charts از Nexus

### مرحله 8: Infrastructure Tools

1. Pull و Push **Jira** (Phase 8.1)
2. Pull و Push **Confluence** (Phase 8.2)
3. Pull و Push **GitLab** (Phase 8.3)
4. Pull و Push **Jenkins** (Phase 8.4)
5. Pull و Push **Nextcloud** (Phase 8.5)
6. Pull و Push **Mayan EDMS** (Phase 8.6)
7. Deploy با استفاده از Helm charts از Nexus

### مرحله 9: Application Services

1. Pull و Push **Base Images** (Java, Node.js, Nginx) (Phase 9)
2. Build و Push **Application Images** (Backend Services, Frontend)
3. Deploy با استفاده از manifests/charts

### مرحله 10: CI/CD

1. Pull و Push **ArgoCD Images** (Phase 10.1)
2. Pull و Push **Spring Boot Admin** (Phase 10.2)
3. Deploy با استفاده از Helm charts از Nexus

### مرحله 11: Backup

1. Pull و Push **Velero** (Phase 11)
2. نصب و پیکربندی **Velero** برای backup

---

## اسکریپت خودکار برای Pull و Push

### اسکریپت کامل Pull و Push

```bash
#!/bin/bash
# روی سرور هلند با اینترنت آزاد (Download Source)
# این سرور فقط pull/tag/push انجام می‌دهد؛ سرور Registry و Nexus در ایران (rr.alefba2.ir و mn.alefba2.ir) فضای دیسک کافی دارند.
# اسکریپت برای pull و push تمام images با تمیزکاری دوره‌ای دیسک
# تمام images از سرور هلند pull شده و به registry سرور ایران (rr.alefba2.ir) push می‌شوند

REGISTRY="rr.alefba2.ir"
REGISTRY_USER="admin"
REGISTRY_PASS="<pass>"

# Login
nerdctl login $REGISTRY -u $REGISTRY_USER -p "$REGISTRY_PASS"

# شمارنده برای کنترل تمیزکاری دوره‌ای (بعد از هر ۳ تصویر)
IMAGE_COUNTER=0

# Function برای pull, tag, push و تمیزکاری روی سرور مبدأ
pull_tag_push() {
    local source_image=$1
    local target_image=$2
    
    echo "Pulling $source_image..."
    nerdctl pull "$source_image"
    
    echo "Tagging as $target_image..."
    nerdctl tag "$source_image" "$target_image"
    
    echo "Pushing $target_image..."
    nerdctl push "$target_image"
    
    echo "✓ Done: $target_image"

    # حذف ایمیج‌های محلی برای آزادسازی دیسک روی سرور مبدأ
    echo "Cleaning up local images for $source_image and $target_image..."
    nerdctl rmi "$source_image" "$target_image" >/dev/null 2>&1 || true

    # افزایش شمارنده و تمیزکاری عمیق بعد از هر ۳ ایمیج
    IMAGE_COUNTER=$((IMAGE_COUNTER + 1))
    if (( IMAGE_COUNTER % 3 == 0 )); then
        echo "Running deep cleanup after $IMAGE_COUNTER images..."
        nerdctl image prune -f >/dev/null 2>&1 || true
    fi
}

# Phase 0: Registry
pull_tag_push "docker.io/library/registry:3.0.0" "$REGISTRY/library/registry:3.0.0"
pull_tag_push "docker.io/joxit/docker-registry-ui:2.6.0" "$REGISTRY/joxit/docker-registry-ui:2.6.0"

# Phase 1: Kubernetes Core
pull_tag_push "registry.k8s.io/kube-apiserver:v1.32.3" "$REGISTRY/k8s/kube-apiserver:v1.32.3"
pull_tag_push "registry.k8s.io/kube-controller-manager:v1.32.3" "$REGISTRY/k8s/kube-controller-manager:v1.32.3"
pull_tag_push "registry.k8s.io/kube-scheduler:v1.32.3" "$REGISTRY/k8s/kube-scheduler:v1.32.3"
pull_tag_push "registry.k8s.io/kube-proxy:v1.32.3" "$REGISTRY/k8s/kube-proxy:v1.32.3"
pull_tag_push "registry.k8s.io/etcd:3.5.15-0" "$REGISTRY/k8s/etcd:3.5.15-0"
pull_tag_push "registry.k8s.io/coredns/coredns:v1.11.3" "$REGISTRY/k8s/coredns:v1.11.3"
pull_tag_push "registry.k8s.io/pause:3.10.1" "$REGISTRY/k8s/pause:3.10.1"

# Phase 2: Calico
pull_tag_push "quay.io/tigera/operator:v1.40.3" "$REGISTRY/tigera/operator:v1.40.3"
pull_tag_push "quay.io/calico/node:v3.35.0" "$REGISTRY/quay/calico/node:v3.35.0"
pull_tag_push "quay.io/calico/cni:v3.35.0" "$REGISTRY/quay/calico/cni:v3.35.0"
pull_tag_push "quay.io/calico/kube-controllers:v3.35.0" "$REGISTRY/quay/calico/kube-controllers:v3.35.0"
pull_tag_push "quay.io/calico/pod2daemon-flexvol:v3.35.0" "$REGISTRY/quay/calico/pod2daemon-flexvol:v3.35.0"
pull_tag_push "quay.io/calico/csi:v3.35.0" "$REGISTRY/quay/calico/csi:v3.35.0"
pull_tag_push "quay.io/calico/typha:v3.35.0" "$REGISTRY/quay/calico/typha:v3.35.0"
pull_tag_push "quay.io/calico/apiserver:v3.35.0" "$REGISTRY/quay/calico/apiserver:v3.35.0"
pull_tag_push "quay.io/calico/node-driver-registrar:v3.35.0" "$REGISTRY/quay/calico/node-driver-registrar:v3.35.0"

# Phase 3: Core Add-ons
pull_tag_push "registry.k8s.io/metrics-server/metrics-server:v0.8.0" "$REGISTRY/k8s/metrics-server:v0.8.0"
pull_tag_push "registry.k8s.io/ingress-nginx/controller:v1.12.0" "$REGISTRY/ingress-nginx/controller:v1.12.0"
pull_tag_push "registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20250101-8b53cabe0" "$REGISTRY/ingress-nginx/kube-webhook-certgen:v20250101-8b53cabe0"
pull_tag_push "quay.io/jetstack/cert-manager-controller:v1.14.4" "$REGISTRY/jetstack/cert-manager-controller:v1.14.4"
pull_tag_push "quay.io/jetstack/cert-manager-webhook:v1.14.4" "$REGISTRY/jetstack/cert-manager-webhook:v1.14.4"
pull_tag_push "quay.io/jetstack/cert-manager-cainjector:v1.14.4" "$REGISTRY/jetstack/cert-manager-cainjector:v1.14.4"
pull_tag_push "quay.io/jetstack/cert-manager-ctl:v1.14.4" "$REGISTRY/jetstack/cert-manager-ctl:v1.14.4"
pull_tag_push "quay.io/jetstack/cert-manager-acmesolver:v1.14.4" "$REGISTRY/jetstack/cert-manager-acmesolver:v1.14.4"
# CSI Drivers (برای StorageClass)
pull_tag_push "registry.k8s.io/sig-storage/snapshot-controller:v6.3.2" "$REGISTRY/k8s/snapshot-controller:v6.3.2"
pull_tag_push "registry.k8s.io/sig-storage/csi-provisioner:v4.0.0" "$REGISTRY/k8s/csi-provisioner:v4.0.0"
pull_tag_push "registry.k8s.io/sig-storage/csi-attacher:v4.5.0" "$REGISTRY/k8s/csi-attacher:v4.5.0"
pull_tag_push "registry.k8s.io/sig-storage/csi-resizer:v1.10.0" "$REGISTRY/k8s/csi-resizer:v1.10.0"
pull_tag_push "registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.11.1" "$REGISTRY/k8s/csi-node-driver-registrar:v2.11.0"

# Phase 4: Monitoring
pull_tag_push "quay.io/prometheus/prometheus:v3.12.0" "$REGISTRY/prometheus/prometheus:v3.12.0"
pull_tag_push "quay.io/prometheus/alertmanager:v0.32.0" "$REGISTRY/prometheus/alertmanager:v0.32.0"
pull_tag_push "quay.io/prometheus/node-exporter:v1.12.0" "$REGISTRY/prometheus/node-exporter:v1.12.0"
pull_tag_push "quay.io/prometheus/pushgateway:v1.13.0" "$REGISTRY/prometheus/pushgateway:v1.13.0"
pull_tag_push "docker.io/grafana/grafana:13.0.0" "$REGISTRY/grafana/grafana:13.0.0"
pull_tag_push "registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.16.0" "$REGISTRY/k8s/kube-state-metrics:v2.16.0"
pull_tag_push "quay.io/prometheus-operator/prometheus-operator:v0.88.1" "$REGISTRY/prometheus-operator/prometheus-operator:v0.88.1"
pull_tag_push "quay.io/prometheus-operator/prometheus-config-reloader:v0.88.1" "$REGISTRY/prometheus-operator/prometheus-config-reloader:v0.88.1"
pull_tag_push "docker.io/grafana/loki:3.6" "$REGISTRY/grafana/loki:3.6"
pull_tag_push "docker.io/grafana/promtail:3.6" "$REGISTRY/grafana/promtail:3.6"
pull_tag_push "docker.io/grafana/tempo:2.10.0" "$REGISTRY/grafana/tempo:2.10.0"
pull_tag_push "docker.io/grafana/agent:v0.44.7" "$REGISTRY/grafana/agent:v0.44.7"

# Phase 5: Databases
pull_tag_push "docker.io/cockroachdb/cockroach:v24.3.25" "$REGISTRY/cockroachdb/cockroach:v24.3.25"
pull_tag_push "docker.io/clickhouse/clickhouse-server:24.1" "$REGISTRY/clickhouse/clickhouse-server:24.1"
pull_tag_push "docker.io/altinity/clickhouse-operator:0.25.0" "$REGISTRY/altinity/clickhouse-operator:0.25.0"
pull_tag_push "docker.io/library/redis:7.2-alpine" "$REGISTRY/library/redis:7.2-alpine"
pull_tag_push "docker.io/library/postgres:16-alpine" "$REGISTRY/library/postgres:16-alpine"

# Phase 6: Messaging
pull_tag_push "docker.io/redpandadata/redpanda:v24.1.1" "$REGISTRY/redpandadata/redpanda:v24.1.1"
pull_tag_push "docker.io/redpandadata/console:v2.5.0" "$REGISTRY/redpandadata/console:v2.5.0"

# Phase 7: Security
pull_tag_push "quay.io/keycloak/keycloak:25.0.4" "$REGISTRY/keycloak/keycloak:25.0.4"
pull_tag_push "docker.io/aquasec/trivy-operator:0.31.0" "$REGISTRY/aquasec/trivy-operator:0.31.0"
pull_tag_push "docker.io/falcosecurity/falco:0.40.0" "$REGISTRY/falcosecurity/falco:0.40.0"
pull_tag_push "docker.io/falcosecurity/falcosidekick:2.6.0" "$REGISTRY/falcosecurity/falcosidekick:2.6.0"
# OPA Gatekeeper یا Kyverno (انتخاب یکی)
pull_tag_push "docker.io/openpolicyagent/gatekeeper:v3.15.0" "$REGISTRY/openpolicyagent/gatekeeper:v3.15.0"
# یا Kyverno (ساده‌تر):
pull_tag_push "docker.io/kyverno/kyverno:v1.12.2" "$REGISTRY/kyverno/kyverno:v1.12.2"
pull_tag_push "docker.io/kyverno/kyvernopre:v1.12.2" "$REGISTRY/kyverno/kyvernopre:v1.12.2"
pull_tag_push "ghcr.io/zaproxy/zaproxy:stable" "$REGISTRY/zaproxy/zaproxy:stable"

# Phase 8: Infrastructure Tools
pull_tag_push "docker.io/atlassian/jira-software:9.28.0" "$REGISTRY/atlassian/jira-software:9.28.0"
# NOTE: نسخهٔ Confluence را باید در زمان نصب از Docker Hub انتخاب کنی (بخش 8.2 را ببین).
# pull_tag_push "docker.io/atlassian/confluence:9.3.0" "$REGISTRY/atlassian/confluence:9.3.0"
# NOTE: نسخه‌های GitLab CE/Runner در این اسکریپت به‌صورت placeholder هستند و باید بر اساس نسخهٔ LTS واقعی تنظیم شوند.
# pull_tag_push "docker.io/gitlab/gitlab-ce:19.0.0-ce.0" "$REGISTRY/gitlab/gitlab-ce:19.0.0-ce.0"
# pull_tag_push "docker.io/gitlab/gitlab-runner:v19.0.0" "$REGISTRY/gitlab/gitlab-runner:v19.0.0"
pull_tag_push "docker.io/jenkins/jenkins:2.480-jdk17" "$REGISTRY/jenkins/jenkins:2.480-jdk17"
pull_tag_push "docker.io/library/nextcloud:30.0.0-apache" "$REGISTRY/library/nextcloud:30.0.0-apache"
pull_tag_push "docker.io/mayanedms/mayanedms:v4.9.8" "$REGISTRY/mayanedms/mayanedms:v4.9.8"

# Phase 9: Base Images
pull_tag_push "docker.io/library/eclipse-temurin:21-jdk-alpine" "$REGISTRY/library/eclipse-temurin:21-jdk-alpine"
pull_tag_push "docker.io/library/eclipse-temurin:21-jre-alpine" "$REGISTRY/library/eclipse-temurin:21-jre-alpine"
pull_tag_push "gcr.io/distroless/java21:nonroot" "$REGISTRY/distroless/java21:nonroot"
pull_tag_push "docker.io/library/node:20-alpine" "$REGISTRY/library/node:20-alpine"
pull_tag_push "docker.io/library/node:20-slim" "$REGISTRY/library/node:20-slim"
pull_tag_push "docker.io/library/nginx:1.29-alpine" "$REGISTRY/library/nginx:1.29-alpine"
pull_tag_push "docker.io/library/busybox:1.36" "$REGISTRY/library/busybox:1.36"
pull_tag_push "docker.io/library/alpine:3.22" "$REGISTRY/library/alpine:3.22"
pull_tag_push "docker.io/library/ubuntu:22.04" "$REGISTRY/library/ubuntu:22.04"
pull_tag_push "docker.io/library/debian:12-slim" "$REGISTRY/library/debian:12-slim"
pull_tag_push "docker.io/alpine/helm:3.15.3" "$REGISTRY/alpine/helm:3.15.3"

# Phase 10: CI/CD
# NOTE: نسخه‌های ArgoCD باید در زمان نصب بر اساس مستندات رسمی انتخاب شوند (بخش 10.1 را ببین).
# pull_tag_push "quay.io/argoproj/argocd:v3.8.0" "$REGISTRY/argoproj/argocd:v3.8.0"
# pull_tag_push "quay.io/argoproj/argocd-repo-server:v3.8.0" "$REGISTRY/argoproj/argocd-repo-server:v3.8.0"
# pull_tag_push "quay.io/argoproj/argocd-applicationset:v0.18.0" "$REGISTRY/argoproj/argocd-applicationset:v0.18.0"
# pull_tag_push "quay.io/argoproj/argocd-image-updater:v0.18.0" "$REGISTRY/argoproj/argocd-image-updater:v0.18.0"
# pull_tag_push "quay.io/argoproj/argocd-notifications:v3.8.0" "$REGISTRY/argoproj/argocd-notifications:v3.8.0"
# pull_tag_push "quay.io/argoproj/argocd-rollouts:v2.18.0" "$REGISTRY/argoproj/argocd-rollouts:v2.18.0"
pull_tag_push "quay.io/argoproj/notifications-controller:v1.5.0" "$REGISTRY/argoproj/notifications-controller:v1.5.0"
pull_tag_push "quay.io/argoproj/notifications-bot:v1.5.0" "$REGISTRY/argoproj/notifications-bot:v1.5.0"
pull_tag_push "docker.io/codecentric/spring-boot-admin:2.6.7" "$REGISTRY/codecentric/spring-boot-admin:2.6.7"

# Phase 11: Backup
pull_tag_push "docker.io/velero/velero:v1.13.0" "$REGISTRY/velero/velero:v1.13.0"
pull_tag_push "docker.io/velero/velero-plugin-for-aws:v1.13.0" "$REGISTRY/velero/velero-plugin-for-aws:v1.13.0"
pull_tag_push "docker.io/velero/velero-plugin-for-gcp:v1.13.0" "$REGISTRY/velero/velero-plugin-for-gcp:v1.13.0"
pull_tag_push "docker.io/velero/velero-plugin-for-csi:v0.7.0" "$REGISTRY/velero/velero-plugin-for-csi:v0.7.0"
# Kubernetes Control Plane - Additional versions for upgrade scenarios
pull_tag_push "registry.k8s.io/kube-apiserver:v1.32.2" "$REGISTRY/k8s/kube-apiserver:v1.32.2"
pull_tag_push "registry.k8s.io/kube-controller-manager:v1.32.2" "$REGISTRY/k8s/kube-controller-manager:v1.32.2"
pull_tag_push "registry.k8s.io/kube-scheduler:v1.32.2" "$REGISTRY/k8s/kube-scheduler:v1.32.2"
pull_tag_push "registry.k8s.io/kube-proxy:v1.32.2" "$REGISTRY/k8s/kube-proxy:v1.32.2"
# DNS & Network Utilities
pull_tag_push "registry.k8s.io/e2e-test-images/dnsutils:1.3" "$REGISTRY/k8s/dnsutils:1.3"
pull_tag_push "docker.io/praqma/network-multitool:latest" "$REGISTRY/praqma/network-multitool:latest"
# Storage - NFS Provisioner
pull_tag_push "registry.k8s.io/sig-storage/nfs-subdir-external-provisioner:v4.0.2" "$REGISTRY/k8s/nfs-subdir-external-provisioner:v4.0.2"
# Security - Trivy CLI
pull_tag_push "docker.io/aquasec/trivy:0.50.1" "$REGISTRY/aquasec/trivy:0.50.1"

echo "✓ All images pushed successfully!"
```

---

## اسکریپت خودکار برای Helm Charts

```bash
#!/bin/bash
# روی Management Node (یا سرور هلند با اینترنت آزاد)
# اسکریپت برای pull و push Helm charts به Nexus سرور ایران (mn.alefba2.ir)

NEXUS_URL="https://mn.alefba2.ir/repository/helm-charts"
NEXUS_USER="k8s-reader"
NEXUS_PASS="<Token>"

# Function برای pull, package و push chart
pull_package_push() {
    local repo_name=$1
    local repo_url=$2
    local chart_name=$3
    local chart_version=$4
    
    echo "Adding repo $repo_name..."
    helm repo add $repo_name $repo_url
    helm repo update
    
    echo "Pulling $chart_name:$chart_version..."
    helm pull $repo_name/$chart_name --version $chart_version
    
    echo "Packaging chart..."
    helm package $chart_name-$chart_version.tgz
    
    echo "Updating index..."
    helm repo index . --url $NEXUS_URL
    
    echo "Pushing chart..."
    curl -u $NEXUS_USER:$NEXUS_PASS -T ./$chart_name-$chart_version.tgz $NEXUS_URL/
    curl -u $NEXUS_USER:$NEXUS_PASS -T ./index.yaml $NEXUS_URL/
    
    echo "✓ Done: $chart_name:$chart_version"
}

# Phase 2: Calico
pull_package_push "projectcalico" "https://docs.tigera.io/calico/charts" "tigera-operator" "v3.31.3"

# Phase 3: Core Add-ons
pull_package_push "ingress-nginx" "https://kubernetes.github.io/ingress-nginx" "ingress-nginx" "4.10.0"
pull_package_push "jetstack" "https://charts.jetstack.io" "cert-manager" "v1.14.4"

# Phase 4: Monitoring
pull_package_push "prometheus-community" "https://prometheus-community.github.io/helm-charts" "kube-prometheus-stack" "59.0.0"
pull_package_push "grafana" "https://grafana.github.io/helm-charts" "loki-stack" "2.10.2"
pull_package_push "grafana" "https://grafana.github.io/helm-charts" "tempo" "1.6.0"

# Phase 5: Databases
pull_package_push "bitnami" "https://charts.bitnami.com/bitnami" "redis" "19.1.0"

# Phase 6: Messaging
pull_package_push "redpanda" "https://charts.redpanda.com" "redpanda" "4.0.0"

# Phase 7: Security
pull_package_push "codecentric" "https://codecentric.github.io/helm-charts" "keycloak" "25.0.4"
pull_package_push "aquasecurity" "https://aquasecurity.github.io/helm-charts" "trivy-operator" "0.31.0"
pull_package_push "falcosecurity" "https://falcosecurity.github.io/charts" "falco" "4.0.0"

# Phase 8: Infrastructure Tools
pull_package_push "atlassian-data-center" "https://atlassian.github.io/data-center-helm-charts" "jira" "2.1.0"
pull_package_push "atlassian-data-center" "https://atlassian.github.io/data-center-helm-charts" "confluence" "2.1.0"
pull_package_push "gitlab" "https://charts.gitlab.io" "gitlab" "8.0.0"
pull_package_push "jenkins" "https://charts.jenkins.io" "jenkins" "5.4.0"
pull_package_push "nextcloud" "https://nextcloud.github.io/helm/" "nextcloud" "2.2.0"

# Phase 10: CI/CD
pull_package_push "argo" "https://argoproj.github.io/argo-helm" "argo-cd" "9.1.7"

# Phase 11: Backup
pull_package_push "vmware-tanzu" "https://vmware-tanzu.github.io/helm-charts" "velero" "6.1.0"

echo "✓ All Helm charts pushed successfully!"
```

---

## خلاصه کامل Images (Quick Reference)

### تعداد کل Images تقریبی: ~80-100 image

| Category             | تعداد Images | مثال‌ها                                                   |
|----------------------|--------------|-----------------------------------------------------------|
| Kubernetes Core      | 7            | kube-apiserver, etcd, coredns                             |
| CNI (Calico)         | 8            | calico/node, calico/cni, typha, apiserver                 |
| Core Add-ons         | 13           | metrics-server, ingress-nginx, cert-manager, CSI drivers  |
| Monitoring           | 11           | prometheus, grafana, loki, tempo, grafana-agent           |
| Databases            | 5            | cockroachdb, clickhouse, redis, postgres                  |
| Messaging            | 2-5          | redpanda, kafka (optional)                                |
| Security             | 8            | keycloak, trivy, falco, gatekeeper/kyverno, zap           |
| Infrastructure Tools | 7            | jira, confluence, gitlab, jenkins, nextcloud, mayan       |
| CI/CD                | 7            | argocd, notifications, rollouts, spring-boot-admin        |
| Base Images          | 8            | eclipse-temurin, distroless, node, nginx, busybox, alpine |
| Backup               | 4            | velero + plugins                                          |
| Registry             | 2            | registry, registry-ui                                     |

---

## خلاصه کامل Helm Charts (Quick Reference)

### تعداد کل Charts تقریبی: ~20-25 chart

| Category             | تعداد Charts | مثال‌ها                                               |
|----------------------|--------------|-------------------------------------------------------|
| CNI                  | 1            | tigera-operator (Calico)                              |
| Core Add-ons         | 2            | ingress-nginx, cert-manager                           |
| Monitoring           | 3            | kube-prometheus-stack, loki-stack, tempo              |
| Databases            | 1            | redis (CockroachDB و ClickHouse معمولاً با manifests) |
| Messaging            | 1            | redpanda                                              |
| Security             | 4-5          | keycloak, trivy-operator, falco, gatekeeper/kyverno   |
| Infrastructure Tools | 5            | jira, confluence, gitlab, jenkins, nextcloud          |
| CI/CD                | 1            | argo-cd                                               |
| Backup               | 1            | velero                                                |

---

## نکات مهم

1. **همه images باید ابتدا pull و push شوند قبل از استفاده**
2. **همه manifests باید در Nexus push شوند**
3. **همه Helm charts باید در Nexus push شوند**
4. **اسکریپت Pull/Push برای سرور مبدأ با دیسک محدود طراحی شده است** → بعد از push هر ایمیج، نسخه‌های محلی آن حذف می‌شود
   و بعد از هر ۳ ایمیج، تمیزکاری عمیق (`image prune`) اجرا می‌شود تا مشکل کمبود فضا پیش نیاید. روی سرور Registry/Nexus
   نیازی به این تمیزکاری نیست چون دیسک کافی در نظر گرفته شده است.
5. **برخی ایمیج‌ها و پلاگین‌ها مانند Kafka/Strimzi، Postgres 15، distroless/java21، Velero GCP plugin و ... به‌صورت
   اختیاری در فازها ذکر شده‌اند**؛ لیست و اسکریپت خودکار «Complete» فقط مجموعه حداقلی و نهایی مورد توافق برای این پروژه
   را پوشش می‌دهد. در صورت نیاز می‌توان این موارد اختیاری را نیز به اسکریپت و جدول‌ها اضافه کرد.
6. **استفاده از ورژن‌های stable و LTS**
7. **بررسی compatibility بین ورژن‌ها**
8. **Backup منظم registry و nexus**
9. **تخمین حجم کل:** تقریباً 50-100 GB برای تمام images
10. **زمان دانلود:** بسته به سرعت اینترنت، 4-8 ساعت برای تمام images
11. **فضای مورد نیاز برای Registry:** حداقل 200 GB (با در نظر گیری رشد آینده)
12. **فضای مورد نیاز برای Nexus:** حداقل 100 GB (برای charts و manifests)

---

## جدول کامل Images (Complete Images Table)

### Phase 0: Registry Infrastructure

| # | Image Name                 | Version | Source Registry | Target Registry                                | Size (approx) |
|---|----------------------------|---------|-----------------|------------------------------------------------|---------------|
| 1 | `registry:3`               | `3.0.0` | docker.io       | `rr.alefba2.ir/library/registry:3.0.0`         | ~25 MB        |
| 2 | `joxit/docker-registry-ui` | `2.6.0` | docker.io       | `rr.alefba2.ir/joxit/docker-registry-ui:2.6.0` | ~15 MB        |

### Phase 1: Kubernetes Core

| # | Image Name                | Version    | Source Registry | Target Registry                                     | Size (approx) |
|---|---------------------------|------------|-----------------|-----------------------------------------------------|---------------|
| 3 | `kube-apiserver`          | `v1.32.3`  | registry.k8s.io | `rr.alefba2.ir/k8s/kube-apiserver:v1.32.3`          | ~150 MB       |
| 4 | `kube-controller-manager` | `v1.32.3`  | registry.k8s.io | `rr.alefba2.ir/k8s/kube-controller-manager:v1.32.3` | ~130 MB       |
| 5 | `kube-scheduler`          | `v1.32.3`  | registry.k8s.io | `rr.alefba2.ir/k8s/kube-scheduler:v1.32.3`          | ~120 MB       |
| 6 | `kube-proxy`              | `v1.32.3`  | registry.k8s.io | `rr.alefba2.ir/k8s/kube-proxy:v1.32.3`              | ~120 MB       |
| 7 | `etcd`                    | `3.5.15-0` | registry.k8s.io | `rr.alefba2.ir/k8s/etcd:3.5.15-0`                   | ~200 MB       |
| 8 | `coredns`                 | `v1.11.3`  | registry.k8s.io | `rr.alefba2.ir/k8s/coredns:v1.11.3`                 | ~50 MB        |
| 9 | `pause`                   | `3.10`     | registry.k8s.io | `rr.alefba2.ir/k8s/pause:3.10`                      | ~1 MB         |

### Phase 2: CNI (Calico)

| #  | Image Name                  | Version   | Source Registry | Target Registry                                        | Size (approx) |
|----|-----------------------------|-----------|-----------------|--------------------------------------------------------|---------------|
| 10 | `calico/node`               | `v3.35.0` | quay.io         | `rr.alefba2.ir/quay/calico/node:v3.35.0`               | ~200 MB       |
| 11 | `calico/cni`                | `v3.35.0` | quay.io         | `rr.alefba2.ir/quay/calico/cni:v3.35.0`                | ~150 MB       |
| 12 | `calico/kube-controllers`   | `v3.35.0` | quay.io         | `rr.alefba2.ir/quay/calico/kube-controllers:v3.35.0`   | ~100 MB       |
| 13 | `calico/pod2daemon-flexvol` | `v3.35.0` | quay.io         | `rr.alefba2.ir/quay/calico/pod2daemon-flexvol:v3.35.0` | ~20 MB        |
| 14 | `calico/csi`                | `v3.35.0` | quay.io         | `rr.alefba2.ir/quay/calico/csi:v3.35.0`                | ~50 MB        |
| 15 | `calico/typha`              | `v3.35.0` | quay.io         | `rr.alefba2.ir/quay/calico/typha:v3.35.0`              | ~100 MB       |
| 16 | `calico/apiserver`          | `v3.35.0` | quay.io         | `rr.alefba2.ir/quay/calico/apiserver:v3.35.0`          | ~80 MB        |
| 17 | `tigera/operator`           | `v1.45.0` | quay.io         | `rr.alefba2.ir/tigera/operator:v1.40.3`                | ~100 MB       |

### Phase 3: Core Add-ons

| #   | Image Name                           | Version               | Source Registry | Target Registry                                                        | Size (approx) |
|-----|--------------------------------------|-----------------------|-----------------|------------------------------------------------------------------------|---------------|
| 18  | `metrics-server`                     | `v0.8.0`              | registry.k8s.io | `rr.alefba2.ir/k8s/metrics-server:v0.8.0`                              | ~60 MB        |
| 19  | `ingress-nginx/controller`           | `v1.12.0`             | registry.k8s.io | `rr.alefba2.ir/ingress-nginx/controller:v1.12.0`                       | ~200 MB       |
| 20  | `ingress-nginx/kube-webhook-certgen` | `v20250101-8b53cabe0` | registry.k8s.io | `rr.alefba2.ir/ingress-nginx/kube-webhook-certgen:v20250101-8b53cabe0` | ~50 MB        |
| 21  | `cert-manager-controller`            | `v1.18.0`             | quay.io         | `rr.alefba2.ir/jetstack/cert-manager-controller:v1.18.0`               | ~150 MB       |
| 22  | `cert-manager-webhook`               | `v1.18.0`             | quay.io         | `rr.alefba2.ir/jetstack/cert-manager-webhook:v1.18.0`                  | ~100 MB       |
| 23  | `cert-manager-cainjector`            | `v1.18.0`             | quay.io         | `rr.alefba2.ir/jetstack/cert-manager-cainjector:v1.18.0`               | ~100 MB       |
| 24  | `cert-manager-ctl`                   | `v1.18.0`             | quay.io         | `rr.alefba2.ir/jetstack/cert-manager-ctl:v1.18.0`                      | ~50 MB        |
| 24a | `cert-manager-acmesolver`            | `v1.18.0`             | quay.io         | `rr.alefba2.ir/jetstack/cert-manager-acmesolver:v1.18.0`               | ~50 MB        |
| 25  | `snapshot-controller`                | `v6.3.2`              | registry.k8s.io | `rr.alefba2.ir/k8s/snapshot-controller:v6.3.2`                         | ~50 MB        |
| 26  | `csi-provisioner`                    | `v4.0.0`              | registry.k8s.io | `rr.alefba2.ir/k8s/csi-provisioner:v4.0.0`                             | ~50 MB        |
| 27  | `csi-attacher`                       | `v4.5.0`              | registry.k8s.io | `rr.alefba2.ir/k8s/csi-attacher:v4.5.0`                                | ~50 MB        |
| 28  | `csi-resizer`                        | `v1.10.0`             | registry.k8s.io | `rr.alefba2.ir/k8s/csi-resizer:v1.10.0`                                | ~50 MB        |
| 29  | `csi-node-driver-registrar`          | `v2.11.0`             | registry.k8s.io | `rr.alefba2.ir/k8s/csi-node-driver-registrar:v2.11.0`                  | ~30 MB        |

### Phase 4: Monitoring Stack

| #  | Image Name                   | Version   | Source Registry | Target Registry                                                     | Size (approx) |
|----|------------------------------|-----------|-----------------|---------------------------------------------------------------------|---------------|
| 30 | `prometheus`                 | `v3.12.0` | quay.io         | `rr.alefba2.ir/prometheus-stack/prometheus:v3.12.0`                 | ~250 MB       |
| 31 | `alertmanager`               | `v0.32.0` | quay.io         | `rr.alefba2.ir/prometheus-stack/alertmanager:v0.32.0`               | ~80 MB        |
| 32 | `node-exporter`              | `v1.12.0` | quay.io         | `rr.alefba2.ir/prometheus-stack/node-exporter:v1.12.0`              | ~30 MB        |
| 33 | `pushgateway`                | `v1.13.0` | quay.io         | `rr.alefba2.ir/prometheus-stack/pushgateway:v1.13.0`                | ~30 MB        |
| 34 | `grafana`                    | `13.0.0`  | docker.io       | `rr.alefba2.ir/prometheus-stack/grafana:13.0.0`                     | ~200 MB       |
| 35 | `kube-state-metrics`         | `v2.20.0` | registry.k8s.io | `rr.alefba2.ir/prometheus-stack/kube-state-metrics:v2.20.0`         | ~50 MB        |
| 36 | `prometheus-operator`        | `v0.95.0` | quay.io         | `rr.alefba2.ir/prometheus-stack/prometheus-operator:v0.95.0`        | ~100 MB       |
| 37 | `prometheus-config-reloader` | `v0.95.0` | quay.io         | `rr.alefba2.ir/prometheus-stack/prometheus-config-reloader:v0.95.0` | ~30 MB        |
| 38 | `loki`                       | `2.9.3`   | docker.io       | `rr.alefba2.ir/grafana/loki:3.6`                                    | ~150 MB       |
| 39 | `promtail`                   | `2.9.3`   | docker.io       | `rr.alefba2.ir/grafana/promtail:3.6`                                | ~80 MB        |
| 40 | `tempo`                      | `2.3.1`   | docker.io       | `rr.alefba2.ir/grafana/tempo:2.10.0`                                | ~100 MB       |
| 41 | `grafana-agent`              | `v0.40.0` | docker.io       | `rr.alefba2.ir/grafana/agent:v0.44.7`                               | ~100 MB       |

### Phase 5: Databases

| #  | Image Name                     | Version      | Source Registry | Target Registry                                     | Size (approx) |
|----|--------------------------------|--------------|-----------------|-----------------------------------------------------|---------------|
| 42 | `cockroachdb/cockroach`        | `v24.1.0`    | docker.io       | `rr.alefba2.ir/cockroachdb/cockroach:v24.3.25`      | ~250 MB       |
| 43 | `clickhouse/clickhouse-server` | `24.1`       | docker.io       | `rr.alefba2.ir/clickhouse/clickhouse-server:24.1`   | ~600 MB       |
| 44 | `clickhouse-operator`          | `0.25.0`     | docker.io       | `rr.alefba2.ir/altinity/clickhouse-operator:0.25.0` | ~100 MB       |
| 45 | `redis`                        | `7.2-alpine` | docker.io       | `rr.alefba2.ir/library/redis:7.2-alpine`            | ~30 MB        |
| 46 | `postgres`                     | `16-alpine`  | docker.io       | `rr.alefba2.ir/library/postgres:16-alpine`          | ~250 MB       |

### Phase 6: Messaging

| #  | Image Name              | Version   | Source Registry | Target Registry                               | Size (approx) |
|----|-------------------------|-----------|-----------------|-----------------------------------------------|---------------|
| 47 | `redpandadata/redpanda` | `v24.1.1` | docker.io       | `rr.alefba2.ir/redpandadata/redpanda:v24.1.1` | ~300 MB       |
| 48 | `redpandadata/console`  | `v2.5.0`  | docker.io       | `rr.alefba2.ir/redpandadata/console:v2.5.0`   | ~200 MB       |

### Phase 7: Security

| #  | Image Name          | Version   | Source Registry | Target Registry                                    | Size (approx) |
|----|---------------------|-----------|-----------------|----------------------------------------------------|---------------|
| 49 | `keycloak/keycloak` | `25.0.4`  | quay.io         | `rr.alefba2.ir/keycloak/keycloak:25.0.4`           | ~600 MB       |
| 50 | `trivy-operator`    | `0.31.0`  | docker.io       | `rr.alefba2.ir/aquasec/trivy-operator:0.31.0`      | ~100 MB       |
| 51 | `falco`             | `0.40.0`  | docker.io       | `rr.alefba2.ir/falcosecurity/falco:0.40.0`         | ~150 MB       |
| 52 | `falcosidekick`     | `2.6.0`   | docker.io       | `rr.alefba2.ir/falcosecurity/falcosidekick:2.6.0`  | ~50 MB        |
| 53 | `gatekeeper`        | `v3.15.0` | docker.io       | `rr.alefba2.ir/openpolicyagent/gatekeeper:v3.15.0` | ~100 MB       |
| 54 | `kyverno`           | `v1.12.2` | docker.io       | `rr.alefba2.ir/kyverno/kyverno:v1.12.2`            | ~150 MB       |
| 55 | `kyvernopre`        | `v1.12.2` | docker.io       | `rr.alefba2.ir/kyverno/kyvernopre:v1.12.2`         | ~50 MB        |
| 56 | `zaproxy/zaproxy`   | `stable`  | ghcr.io         | `rr.alefba2.ir/zaproxy/zaproxy:stable`             | ~500 MB       |

### Phase 8: Infrastructure Tools

| #  | Image Name                | Version         | Source Registry | Target Registry                                 | Size (approx) |
|----|---------------------------|-----------------|-----------------|-------------------------------------------------|---------------|
| 56 | `atlassian/jira-software` | `9.28.0`        | docker.io       | `rr.alefba2.ir/atlassian/jira-software:9.28.0`  | ~1.5 GB       |
| 57 | `atlassian/confluence`    | `9.3.0`         | docker.io       | `rr.alefba2.ir/atlassian/confluence:9.3.0`      | ~1.2 GB       |
| 58 | `gitlab/gitlab-ce`        | `19.0.0-ce.0`   | docker.io       | `rr.alefba2.ir/gitlab/gitlab-ce:19.0.0-ce.0`    | ~2 GB         |
| 59 | `gitlab/gitlab-runner`    | `v19.0.0`       | docker.io       | `rr.alefba2.ir/gitlab/gitlab-runner:v19.0.0`    | ~200 MB       |
| 60 | `jenkins/jenkins`         | `2.480-jdk17`   | docker.io       | `rr.alefba2.ir/jenkins/jenkins:2.480-jdk17`     | ~500 MB       |
| 61 | `nextcloud`               | `30.0.0-apache` | docker.io       | `rr.alefba2.ir/library/nextcloud:30.0.0-apache` | ~300 MB       |
| 62 | `mayanedms/mayanedms`     | `5.2.0`         | docker.io       | `rr.alefba2.ir/mayanedms/mayanedms:v4.9.8`      | ~500 MB       |

### Phase 9: Base Images

| #  | Image Name        | Version         | Source Registry | Target Registry                                       | Size (approx) |
|----|-------------------|-----------------|-----------------|-------------------------------------------------------|---------------|
| 63 | `eclipse-temurin` | `21-jdk-alpine` | docker.io       | `rr.alefba2.ir/library/eclipse-temurin:21-jdk-alpine` | ~400 MB       |
| 64 | `eclipse-temurin` | `21-jre-alpine` | docker.io       | `rr.alefba2.ir/library/eclipse-temurin:21-jre-alpine` | ~200 MB       |
| 65 | `distroless/java` | `21-nonroot`    | gcr.io          | `rr.alefba2.ir/distroless/java21:nonroot`             | ~50 MB        |
| 66 | `node`            | `20-alpine`     | docker.io       | `rr.alefba2.ir/library/node:20-alpine`                | ~150 MB       |
| 67 | `node`            | `20-slim`       | docker.io       | `rr.alefba2.ir/library/node:20-slim`                  | ~100 MB       |
| 68 | `nginx`           | `1.29-alpine`   | docker.io       | `rr.alefba2.ir/library/nginx:1.29-alpine`             | ~50 MB        |
| 69 | `busybox`         | `1.39`          | docker.io       | `rr.alefba2.ir/library/busybox:1.39`                  | ~5 MB         |
| 70 | `alpine`          | `3.22`          | docker.io       | `rr.alefba2.ir/library/alpine:3.22`                   | ~5 MB         |

### Phase 10: CI/CD

| #   | Image Name                        | Version   | Source Registry | Target Registry                                          | Size (approx) |
|-----|-----------------------------------|-----------|-----------------|----------------------------------------------------------|---------------|
| 71  | `argoproj/argocd`                 | `v3.8.0`  | quay.io         | `rr.alefba2.ir/argoproj/argocd:v3.8.0`                   | ~200 MB       |
| 72  | `argoproj/argocd-repo-server`     | `v3.8.0`  | quay.io         | `rr.alefba2.ir/argoproj/argocd-repo-server:v3.8.0`       | ~150 MB       |
| 73  | `argoproj/argocd-applicationset`  | `v0.18.0` | quay.io         | `rr.alefba2.ir/argoproj/argocd-applicationset:v0.18.0`   | ~100 MB       |
| 74  | `argoproj/argocd-image-updater`   | `v0.18.0` | quay.io         | `rr.alefba2.ir/argoproj/argocd-image-updater:v0.18.0`    | ~80 MB        |
| 75  | `argoproj/argocd-notifications`   | `v3.8.0`  | quay.io         | `rr.alefba2.ir/argoproj/argocd-notifications:v3.8.0`     | ~100 MB       |
| 76  | `argoproj/argocd-rollouts`        | `v2.18.0` | quay.io         | `rr.alefba2.ir/argoproj/argocd-rollouts:v2.18.0`         | ~150 MB       |
| 77  | `spring-boot-admin`               | `2.11.0`  | docker.io       | `rr.alefba2.ir/codecentric/spring-boot-admin:2.6.7`      | ~200 MB       |
| 77a | `argocd-notifications-controller` | `v1.5.0`  | quay.io         | `rr.alefba2.ir/argoproj/notifications-controller:v1.5.0` | ~100 MB       |
| 77b | `argocd-notifications-bot`        | `v1.5.0`  | quay.io         | `rr.alefba2.ir/argoproj/notifications-bot:v1.5.0`        | ~50 MB        |

### Phase 11: Backup

| #  | Image Name              | Version   | Source Registry | Target Registry                                      | Size (approx) |
|----|-------------------------|-----------|-----------------|------------------------------------------------------|---------------|
| 78 | `velero/velero`         | `v1.18.2` | docker.io       | `rr.alefba2.ir/velero/velero:v1.18.2`                | ~100 MB       |
| 79 | `velero-plugin-for-aws` | `v1.13.0` | docker.io       | `rr.alefba2.ir/velero/velero-plugin-for-aws:v1.13.0` | ~50 MB        |
| 80 | `velero-plugin-for-gcp` | `v1.13.0` | docker.io       | `rr.alefba2.ir/velero/velero-plugin-for-gcp:v1.13.0` | ~50 MB        |
| 81 | `velero-plugin-for-csi` | `v0.10.0` | docker.io       | `rr.alefba2.ir/velero/velero-plugin-for-csi:v0.10.0` | ~50 MB        |

**مجموع حجم تقریبی:** ~15-18 GB (بدون compression)

**تعداد کل Images:** 82 image

---

## جدول کامل Helm Charts (Complete Helm Charts Table)

| #  | Chart Name              | Repository                                            | Version   | Chart Size | Push Command          |
|----|-------------------------|-------------------------------------------------------|-----------|------------|-----------------------|
| 1  | `tigera-operator`       | `https://docs.tigera.io/calico/charts`                | `v3.31.3` | ~500 KB    | Push to `helm-charts` |
| 2  | `ingress-nginx`         | `https://kubernetes.github.io/ingress-nginx`          | `4.10.0`  | ~200 KB    | Push to `helm-charts` |
| 3  | `cert-manager`          | `https://charts.jetstack.io`                          | `v1.14.4` | ~300 KB    | Push to `helm-charts` |
| 4  | `kube-prometheus-stack` | `https://prometheus-community.github.io/helm-charts`  | `59.0.0`  | ~1 MB      | Push to `helm-charts` |
| 5  | `loki-stack`            | `https://grafana.github.io/helm-charts`               | `2.10.2`  | ~400 KB    | Push to `helm-charts` |
| 6  | `tempo`                 | `https://grafana.github.io/helm-charts`               | `1.6.0`   | ~300 KB    | Push to `helm-charts` |
| 7  | `redis`                 | `https://charts.bitnami.com/bitnami`                  | `19.1.0`  | ~200 KB    | Push to `helm-charts` |
| 8  | `redpanda`              | `https://charts.redpanda.com`                         | `4.0.0`   | ~400 KB    | Push to `helm-charts` |
| 9  | `keycloak`              | `https://codecentric.github.io/helm-charts`           | `25.0.4`  | ~300 KB    | Push to `helm-charts` |
| 10 | `trivy-operator`        | `https://aquasecurity.github.io/helm-charts`          | `0.31.0`  | ~200 KB    | Push to `helm-charts` |
| 11 | `falco`                 | `https://falcosecurity.github.io/charts`              | `4.0.0`   | ~300 KB    | Push to `helm-charts` |
| 12 | `jira`                  | `https://atlassian.github.io/data-center-helm-charts` | `2.1.0`   | ~500 KB    | Push to `helm-charts` |
| 13 | `confluence`            | `https://atlassian.github.io/data-center-helm-charts` | `2.1.0`   | ~500 KB    | Push to `helm-charts` |
| 14 | `gitlab`                | `https://charts.gitlab.io`                            | `8.0.0`   | ~2 MB      | Push to `helm-charts` |
| 15 | `jenkins`               | `https://charts.jenkins.io`                           | `5.4.0`   | ~400 KB    | Push to `helm-charts` |
| 16 | `nextcloud`             | `https://nextcloud.github.io/helm/`                   | `2.2.0`   | ~300 KB    | Push to `helm-charts` |
| 17 | `argo-cd`               | `https://argoproj.github.io/argo-helm`                | `9.1.7`   | ~1 MB      | Push to `helm-charts` |
| 18 | `velero`                | `https://vmware-tanzu.github.io/helm-charts`          | `6.1.0`   | ~300 KB    | Push to `helm-charts` |

**مجموع حجم Charts:** ~10-15 MB

---

## اسکریپت کامل Pull و Push (Complete Script)

فایل کامل اسکریپت در بخش قبلی آمده است. برای استفاده:

```bash
# روی سرور هلند با اینترنت آزاد (Download Source)
chmod +x pull-push-all-images.sh
./pull-push-all-images.sh
```

---

## اسکریپت کامل Helm Charts (Complete Helm Script)

```bash
#!/bin/bash
# روی Management Node (یا سرور هلند با اینترنت آزاد)
# اسکریپت کامل برای pull و push Helm charts به Nexus سرور ایران (mn.alefba2.ir)

NEXUS_URL="https://mn.alefba2.ir/repository/helm-charts"
NEXUS_USER="k8s-reader"
NEXUS_PASS="<Token>"

mkdir -p helm-charts-work
cd helm-charts-work

# Function برای pull, package و push chart
pull_package_push() {
    local repo_name=$1
    local repo_url=$2
    local chart_name=$3
    local chart_version=$4
    
    echo "=========================================="
    echo "Processing: $chart_name:$chart_version"
    echo "=========================================="
    
    # اضافه کردن repo
    helm repo add $repo_name $repo_url 2>/dev/null || true
    helm repo update
    
    # Pull chart
    helm pull $repo_name/$chart_name --version $chart_version
    
    # Package (اگر tar.gz است، نیازی به package نیست)
    if [ -f "$chart_name-$chart_version.tgz" ]; then
        echo "Chart downloaded: $chart_name-$chart_version.tgz"
    else
        echo "Error: Chart not downloaded"
        return 1
    fi
    
    # Update index
    helm repo index . --url $NEXUS_URL
    
    # Push chart
    echo "Pushing chart to Nexus..."
    curl -u $NEXUS_USER:$NEXUS_PASS -T ./$chart_name-$chart_version.tgz $NEXUS_URL/ || echo "Error pushing chart"
    
    # Push index
    echo "Updating index..."
    curl -u $NEXUS_USER:$NEXUS_PASS -T ./index.yaml $NEXUS_URL/ || echo "Error pushing index"
    
    echo "✓ Done: $chart_name:$chart_version"
    echo ""
}

# Phase 2: CNI
pull_package_push "projectcalico" "https://docs.tigera.io/calico/charts" "tigera-operator" "v3.31.3"

# Phase 3: Core Add-ons
pull_package_push "ingress-nginx" "https://kubernetes.github.io/ingress-nginx" "ingress-nginx" "4.10.0"
pull_package_push "jetstack" "https://charts.jetstack.io" "cert-manager" "v1.14.4"

# Phase 4: Monitoring
pull_package_push "prometheus-community" "https://prometheus-community.github.io/helm-charts" "kube-prometheus-stack" "59.0.0"
pull_package_push "grafana" "https://grafana.github.io/helm-charts" "loki-stack" "2.10.2"
pull_package_push "grafana" "https://grafana.github.io/helm-charts" "tempo" "1.6.0"

# Phase 5: Databases
pull_package_push "bitnami" "https://charts.bitnami.com/bitnami" "redis" "19.1.0"

# Phase 6: Messaging
pull_package_push "redpanda" "https://charts.redpanda.com" "redpanda" "4.0.0"

# Phase 7: Security
pull_package_push "codecentric" "https://codecentric.github.io/helm-charts" "keycloak" "25.0.4"
pull_package_push "aquasecurity" "https://aquasecurity.github.io/helm-charts" "trivy-operator" "0.31.0"
pull_package_push "falcosecurity" "https://falcosecurity.github.io/charts" "falco" "4.0.0"

# Phase 8: Infrastructure Tools
pull_package_push "atlassian-data-center" "https://atlassian.github.io/data-center-helm-charts" "jira" "2.1.0"
pull_package_push "atlassian-data-center" "https://atlassian.github.io/data-center-helm-charts" "confluence" "2.1.0"
pull_package_push "gitlab" "https://charts.gitlab.io" "gitlab" "8.0.0"
pull_package_push "jenkins" "https://charts.jenkins.io" "jenkins" "5.4.0"
pull_package_push "nextcloud" "https://nextcloud.github.io/helm/" "nextcloud" "2.2.0"

# Phase 10: CI/CD
pull_package_push "argo" "https://argoproj.github.io/argo-helm" "argo-cd" "9.1.7"

# Phase 11: Backup
pull_package_push "vmware-tanzu" "https://vmware-tanzu.github.io/helm-charts" "velero" "6.1.0"

echo "=========================================="
echo "✓ All Helm charts pushed successfully!"
echo "=========================================="
```

---

## Manifests مورد نیاز

### Manifests برای Push به Nexus

| Manifest                        | Source | Download Link                                                                                                      | Push Path                                          |
|---------------------------------|--------|--------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| `metrics-server.yaml`           | GitHub | `https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.7.0/components.yaml`                       | `k8s-manifests/core/metrics-server.yaml`           |
| `cockroachdb-statefulset.yaml`  | Custom | Create from template                                                                                               | `k8s-manifests/databases/cockroachdb.yaml`         |
| `clickhouse-operator.yaml`      | GitHub | `https://github.com/Altinity/clickhouse-operator/releases/download/0.25.0/clickhouse-operator-install-bundle.yaml` | `k8s-manifests/databases/clickhouse-operator.yaml` |
| `redis-deployment.yaml`         | Custom | Create from template                                                                                               | `k8s-manifests/databases/redis.yaml`               |
| `namespace-dev.yaml`            | Custom | Create                                                                                                             | `k8s-manifests/namespaces/dev.yaml`                |
| `namespace-stage.yaml`          | Custom | Create                                                                                                             | `k8s-manifests/namespaces/stage.yaml`              |
| `namespace-production.yaml`     | Custom | Create                                                                                                             | `k8s-manifests/namespaces/production.yaml`         |
| `namespace-infrastructure.yaml` | Custom | Create                                                                                                             | `k8s-manifests/namespaces/infrastructure.yaml`     |

**دستورات Push Manifests:**

```bash
# روی Management Node یا Master Node
# دانلود و ویرایش manifests
curl -L https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.8.0/components.yaml -o metrics-server.yaml

# ویرایش image reference
sed -i 's|registry.k8s.io/metrics-server/metrics-server:v0.8.0|rr.alefba2.ir/k8s/metrics-server:v0.8.0|g' metrics-server.yaml

# Push به Nexus
curl -u k8s-reader --upload-file metrics-server.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/core/metrics-server.yaml
```

---

## مراجع

- [Docker Registry Documentation](https://docs.docker.com/registry/)
- [Nexus Repository Manager Documentation](https://help.sonatype.com/repomanager3)
- [Kubernetes Images](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/#running-kubeadm-without-an-internet-connection)
- [Helm Charts](https://helm.sh/docs/topics/charts/)
- [Kubernetes Official Images](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io)
- [Calico Documentation](https://docs.tigera.io/calico/latest/about/)
- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)

---

❤️ Maintained by Soroush

