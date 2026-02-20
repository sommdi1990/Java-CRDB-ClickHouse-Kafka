# چک‌لیست Registry و Nexus - موارد کم‌بود

> **Owner:** Soroush  
> **Scope:** بررسی و لیست کردن مواردی که باید در Registry یا Nexus اضافه شوند

---

## ✅ موارد موجود در Registry (rr.alefba2.ir)

طبق فایل [Complete-Images-Manifests-Helm-Charts-List](Complete-Images-Manifests-Helm-Charts-List)، تمام images زیر در
registry موجود هستند:

- ✅ Kubernetes Core Images (v1.29.7 / v1.32.1)
- ✅ Calico CNI Images (v3.31.3)
- ✅ Metrics Server (v0.7.0)
- ✅ Ingress NGINX (v1.10.1)
- ✅ cert-manager (v1.14.4)
- ✅ CSI Drivers
- ✅ Prometheus Stack Images
- ✅ Grafana Images (Loki, Promtail, Tempo, Agent)
- ✅ Database Images (CockroachDB, ClickHouse, Redis, PostgreSQL)
- ✅ Messaging Images (Redpanda, Kafka)
- ✅ Security Images (Keycloak, Trivy, Falco, Gatekeeper, Kyverno)
- ✅ Infrastructure Tools Images (Jira, Confluence, GitLab, Jenkins, Nextcloud, Mayan EDMS)
- ✅ CI/CD Images (ArgoCD, Spring Boot Admin)
- ✅ Backup Images (Velero)
- ✅ Base Images (Java, Node.js, Nginx, Busybox, Alpine)

---

## ❌ موارد کم‌بود در Nexus (mn.alefba2.ir)

### Helm Charts

این Helm charts باید در Nexus (`mn.alefba2.ir/repository/helm-charts/`) اضافه شوند:

#### Phase 2: CNI

- [ ] `tigera-operator` (v3.31.3) - از `https://docs.tigera.io/calico/charts`

#### Phase 3: Core Add-ons

- [ ] `ingress-nginx` (4.10.0) - از `https://kubernetes.github.io/ingress-nginx`
- [ ] `cert-manager` (v1.14.4) - از `https://charts.jetstack.io`

#### Phase 4: Monitoring

- [ ] `kube-prometheus-stack` (59.0.0) - از `https://prometheus-community.github.io/helm-charts`
- [ ] `loki-stack` (2.10.2) - از `https://grafana.github.io/helm-charts`
- [ ] `tempo` (1.6.0) - از `https://grafana.github.io/helm-charts`

#### Phase 5: Databases

- [ ] `redis` (19.1.0) - از `https://charts.bitnami.com/bitnami`
- [ ] `clickhouse-operator` (0.26.0) - از `https://github.com/Altinity/clickhouse-operator`

#### Phase 6: Messaging

- [ ] `redpanda` (4.0.0) - از `https://charts.redpanda.com`

#### Phase 7: Security

- [ ] `keycloak` (25.0.4) - از `https://codecentric.github.io/helm-charts`
- [ ] `trivy-operator` (0.21.0) - از `https://aquasecurity.github.io/helm-charts`
- [ ] `falco` (4.0.0) - از `https://falcosecurity.github.io/charts`
- [ ] `gatekeeper` (v3.15.0) - از `https://open-policy-agent.github.io/gatekeeper/charts`
- [ ] `kyverno` (v3.3.0) - از `https://kyverno.github.io/kyverno/`

#### Phase 8: Infrastructure Tools (اولویت)

- [ ] `jira` (2.0.0) - از `https://atlassian.github.io/data-center-helm-charts` ⭐
- [ ] `confluence` (2.0.0) - از `https://atlassian.github.io/data-center-helm-charts` ⭐
- [ ] `nextcloud` (2.1.0) - از `https://nextcloud.github.io/helm/` ⭐
- [ ] `gitlab` (7.7.0) - از `https://charts.gitlab.io`
- [ ] `jenkins` (5.3.0) - از `https://charts.jenkins.io`

#### Phase 10: CI/CD

- [ ] `argo-cd` (7.6.0) - از `https://argoproj.github.io/argo-helm`

#### Phase 11: Backup

- [ ] `velero` (6.0.0) - از `https://vmware-tanzu.github.io/helm-charts`

---

### Kubernetes Manifests

این manifests باید در Nexus (`mn.alefba2.ir/repository/k8s-manifests/`) اضافه شوند:

#### Core Components

- [ ] `metrics-server.yaml` - از
  `https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.7.0/components.yaml`
    - **مسیر در Nexus:** `k8s-manifests/core/metrics-server.yaml`
    - **ویرایش لازم:** تغییر image reference به `rr.alefba2.ir/k8s/metrics-server:v0.7.0`

#### Networking

- [ ] `tigera-operator.yaml` - از `https://docs.tigera.io/calico/charts`
    - **مسیر در Nexus:** `k8s-manifests/networking/calico/tigera-operator.yaml`
- [ ] `custom-resources.yaml` - برای Calico
    - **مسیر در Nexus:** `k8s-manifests/networking/calico/custom-resources.yaml`

#### Databases

- [ ] `cockroachdb-statefulset.yaml` - Custom manifest
    - **مسیر در Nexus:** `k8s-manifests/databases/cockroachdb.yaml`
    - **ویرایش لازم:** تغییر image reference به `rr.alefba2.ir/cockroachdb/cockroach:v24.3.25`
- [ ] `clickhouse-operator.yaml` - از
  `https://github.com/Altinity/clickhouse-operator/releases/download/0.26.0/clickhouse-operator-install-bundle.yaml`
    - **مسیر در Nexus:** `k8s-manifests/databases/clickhouse-operator.yaml`
    - **ویرایش لازم:** تغییر image references به registry محلی

#### Namespaces

- [ ] `namespace-dev.yaml` - Custom
    - **مسیر در Nexus:** `k8s-manifests/namespaces/dev.yaml`
- [ ] `namespace-stage.yaml` - Custom
    - **مسیر در Nexus:** `k8s-manifests/namespaces/stage.yaml`
- [ ] `namespace-production.yaml` - Custom
    - **مسیر در Nexus:** `k8s-manifests/namespaces/production.yaml`
- [ ] `namespace-infrastructure.yaml` - Custom
    - **مسیر در Nexus:** `k8s-manifests/namespaces/infrastructure.yaml`

---

## 📋 دستورات برای Push Helm Charts به Nexus

### اسکریپت کامل برای Push Helm Charts

```bash
#!/bin/bash
# روی Control Plane Node یا Registry Node
# اسکریپت برای pull و push Helm charts به Nexus

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

# Phase 2: CNI (اولویت)
pull_package_push "projectcalico" "https://docs.tigera.io/calico/charts" "tigera-operator" "v3.31.3"

# Phase 3: Core Add-ons (اولویت)
pull_package_push "ingress-nginx" "https://kubernetes.github.io/ingress-nginx" "ingress-nginx" "4.10.0"
pull_package_push "jetstack" "https://charts.jetstack.io" "cert-manager" "v1.14.4"

# Phase 8: Infrastructure Tools (اولویت بالا - Jira, Confluence, Nextcloud)
pull_package_push "atlassian-data-center" "https://atlassian.github.io/data-center-helm-charts" "jira" "2.0.0"
pull_package_push "atlassian-data-center" "https://atlassian.github.io/data-center-helm-charts" "confluence" "2.0.0"
pull_package_push "nextcloud" "https://nextcloud.github.io/helm/" "nextcloud" "2.1.0"

# Phase 4: Monitoring (بعد از Infrastructure Tools)
pull_package_push "prometheus-community" "https://prometheus-community.github.io/helm-charts" "kube-prometheus-stack" "59.0.0"
pull_package_push "grafana" "https://grafana.github.io/helm-charts" "loki-stack" "2.10.2"
pull_package_push "grafana" "https://grafana.github.io/helm-charts" "tempo" "1.6.0"

# Phase 5: Databases
pull_package_push "bitnami" "https://charts.bitnami.com/bitnami" "redis" "19.1.0"

# Phase 6: Messaging
pull_package_push "redpanda" "https://charts.redpanda.com" "redpanda" "4.0.0"

# Phase 7: Security
pull_package_push "codecentric" "https://codecentric.github.io/helm-charts" "keycloak" "25.0.4"
pull_package_push "aquasecurity" "https://aquasecurity.github.io/helm-charts" "trivy-operator" "0.21.0"
pull_package_push "falcosecurity" "https://falcosecurity.github.io/charts" "falco" "4.0.0"

# Phase 8: Infrastructure Tools (بقیه)
pull_package_push "gitlab" "https://charts.gitlab.io" "gitlab" "7.7.0"
pull_package_push "jenkins" "https://charts.jenkins.io" "jenkins" "5.3.0"

# Phase 10: CI/CD
pull_package_push "argo" "https://argoproj.github.io/argo-helm" "argo-cd" "7.6.0"

# Phase 11: Backup
pull_package_push "vmware-tanzu" "https://vmware-tanzu.github.io/helm-charts" "velero" "6.0.0"

echo "=========================================="
echo "✓ All Helm charts pushed successfully!"
echo "=========================================="
```

---

## 📋 دستورات برای Push Manifests به Nexus

### Metrics Server Manifest

```bash
# روی Control Plane Node یا Registry Node
# دانلود manifest
curl -L https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.7.0/components.yaml -o metrics-server.yaml

# ویرایش image reference
sed -i 's|registry.k8s.io/metrics-server/metrics-server:v0.7.0|rr.alefba2.ir/k8s/metrics-server:v0.7.0|g' metrics-server.yaml

# Push به Nexus
curl -u k8s-reader:'<Token>' --upload-file metrics-server.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/core/metrics-server.yaml
```

### Calico Manifests

```bash
# روی Control Plane Node یا Registry Node
# دانلود manifests
curl -L https://docs.tigera.io/calico/charts -o calico-manifests.tar.gz
# یا از GitHub
curl -L https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/tigera-operator.yaml -o tigera-operator.yaml
curl -L https://raw.githubusercontent.com/projectcalico/calico/v3.31.3/manifests/custom-resources.yaml -o custom-resources.yaml

# ویرایش image references (اگر نیاز باشد)
# sed -i 's|quay.io/tigera|rr.alefba2.ir/tigera|g' tigera-operator.yaml
# sed -i 's|quay.io/calico|rr.alefba2.ir/quay/calico|g' custom-resources.yaml

# Push به Nexus
curl -u k8s-reader:'<Token>' --upload-file tigera-operator.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/networking/calico/tigera-operator.yaml

curl -u k8s-reader:'<Token>' --upload-file custom-resources.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/networking/calico/custom-resources.yaml
```

### Namespace Manifests

```bash
# روی Control Plane Node یا Registry Node
# ایجاد namespace manifests
cat <<EOF > namespace-dev.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
EOF

cat <<EOF > namespace-stage.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: stage
EOF

cat <<EOF > namespace-production.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
EOF

cat <<EOF > namespace-infrastructure.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: infrastructure
EOF

# Push به Nexus
curl -u k8s-reader:'<Token>' --upload-file namespace-dev.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/namespaces/dev.yaml

curl -u k8s-reader:'<Token>' --upload-file namespace-stage.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/namespaces/stage.yaml

curl -u k8s-reader:'<Token>' --upload-file namespace-production.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/namespaces/production.yaml

curl -u k8s-reader:'<Token>' --upload-file namespace-infrastructure.yaml \
  https://mn.alefba2.ir/repository/k8s-manifests/namespaces/infrastructure.yaml
```

---

## ✅ اولویت‌بندی

### اولویت بالا (قبل از نصب Kubernetes)

1. ✅ تمام Kubernetes Core Images در Registry
2. ✅ تمام Calico Images در Registry
3. ⚠️ Calico Helm Chart در Nexus (برای نصب CNI)

### اولویت متوسط (بعد از نصب CNI)

4. ⚠️ Ingress NGINX Helm Chart در Nexus
5. ⚠️ Metrics Server Manifest در Nexus
6. ⚠️ cert-manager Helm Chart در Nexus

### اولویت بالا (برای Infrastructure Tools)

7. ⚠️ Jira Helm Chart در Nexus ⭐
8. ⚠️ Confluence Helm Chart در Nexus ⭐
9. ⚠️ Nextcloud Helm Chart در Nexus ⭐

### اولویت پایین (بعد از Infrastructure Tools)

10. Monitoring Stack Charts
11. Database Charts
12. Security Charts
13. CI/CD Charts

---

## 📝 یادداشت‌ها

- تمام Helm charts باید قبل از استفاده در Nexus push شوند
- تمام Manifests باید قبل از استفاده در Nexus push شوند
- Image references در Manifests باید به registry محلی (`rr.alefba2.ir`) تغییر یابند
- برای جزئیات کامل images، به [Complete-Images-Manifests-Helm-Charts-List](Complete-Images-Manifests-Helm-Charts-List)
  مراجعه کنید

---

❤️ Maintained by Soroush
