# راهنمای کامل Kubernetes - از صفر تا صد

<div align="right">

[← بازگشت به صفحه اصلی](Home) | [پروپوزال](Proposal) | [لینک‌های مفید](References)

</div>

---

## فهرست مطالب

1. [مقدمه و تئوری Kubernetes](#1-مقدمه-و-تئوری-kubernetes)
2. [تعریف لغات و مفاهیم اصلی](#2-تعریف-لغات-و-مفاهیم-اصلی)
3. [معماری Kubernetes](#3-معماری-kubernetes)
4. [اجرای پروژه در Kubernetes (Stage و Production)](#4-اجرای-پروژه-در-kubernetes-stage-و-production)
5. [نصب و راه‌اندازی Kubernetes Cluster](#5-نصب-و-راهاندازی-kubernetes-cluster)
6. [راه‌اندازی VM مدیریت و مانیتورینگ Rocky 9](#6-راهاندازی-vm-مدیریت-و-مانیتورینگ-rocky-9)
7. [Load Balancing در Kubernetes](#7-load-balancing-در-kubernetes)
8. [مانیتورینگ و Observability](#8-مانیتورینگ-و-observability)
9. [چالش‌ها و راه‌حل‌ها](#9-چالشها-و-راهحلها)
10. [سوال و جواب‌های متداول](#10-سوال-و-جوابهای-متداول)
11. [مزایا و معایب Kubernetes](#11-مزایا-و-معایب-kubernetes)
12. [Best Practices و Recommendations](#12-best-practices-و-recommendations)
13. [لینک‌های مفید و منابع](#13-لینکهای-مفید-و-منابع)

---

## 1. مقدمه و تئوری Kubernetes

### 1.1. Kubernetes چیست؟

**Kubernetes** (که به اختصار K8s نیز نامیده می‌شود) یک پلتفرم منبع‌باز برای خودکارسازی استقرار، مقیاس‌گذاری و مدیریت
containerized applications است. Kubernetes در ابتدا توسط Google توسعه داده شد و اکنون توسط Cloud Native Computing
Foundation (CNCF) نگهداری می‌شود.

### 1.2. تاریخچه Kubernetes

- **سال 2014**: Google Kubernetes را به عنوان پروژه open-source منتشر کرد
- **سال 2015**: Kubernetes v1.0 منتشر شد و CNCF آن را پذیرفت
- **سال 2016**: Kubernetes به طور گسترده در production استفاده شد
- **تا امروز**: Kubernetes به استاندارد صنعتی برای container orchestration تبدیل شده است

### 1.3. چرا Kubernetes؟

**مشکلات قبل از Kubernetes:**

1. **مدیریت دستی Containers**: نیاز به مدیریت دستی چندین container
2. **مقیاس‌پذیری دشوار**: مقیاس‌گذاری دستی و پیچیده
3. **High Availability**: عدم تضمین availability بالا
4. **Rolling Updates**: انجام به‌روزرسانی‌ها بدون downtime دشوار است
5. **Resource Management**: مدیریت منابع بهینه نیست
6. **Service Discovery**: پیدا کردن سرویس‌ها پیچیده است
7. **Load Balancing**: نیاز به راه‌حل‌های پیچیده load balancing

**راه‌حل Kubernetes:**

- **خودکارسازی کامل**: مدیریت خودکار containers
- **Auto-scaling**: مقیاس‌گذاری خودکار بر اساس ترافیک
- **Self-healing**: ترمیم خودکار مشکلات
- **Rolling Updates**: به‌روزرسانی بدون downtime
- **Resource Management**: مدیریت بهینه منابع
- **Service Discovery**: کشف خودکار سرویس‌ها
- **Built-in Load Balancing**: load balancing داخلی

### 1.4. Kubernetes در مقابل Docker Compose

| ویژگی                   | Docker Compose           | Kubernetes       |
|-------------------------|--------------------------|------------------|
| **مقیاس‌پذیری**         | محدود                    | نامحدود          |
| **High Availability**   | نیاز به راه‌حل‌های اضافی | Built-in         |
| **Auto-scaling**        | دستی                     | خودکار           |
| **Rolling Updates**     | دستی                     | خودکار           |
| **Production Ready**    | برای development         | مناسب production |
| **Resource Management** | ساده                     | پیشرفته          |
| **Service Discovery**   | محدود                    | پیشرفته          |
| **پیچیدگی**             | ساده                     | پیچیده‌تر        |

---

## 2. تعریف لغات و مفاهیم اصلی

### 2.1. Core Concepts (مفاهیم اصلی)

#### 2.1.1. Cluster (خوشه)

یک **Cluster** مجموعه‌ای از nodes (سرورها) است که applications را اجرا می‌کنند. یک cluster شامل:

- **Control Plane** (Master Node): مدیریت cluster
- **Worker Nodes**: اجرای applications

#### 2.1.2. Node (گره)

یک **Node** یک ماشین (فیزیکی یا مجازی) است که بخشی از Kubernetes cluster است.

- **Master Node (Control Plane)**:
    - API Server
    - etcd
    - Scheduler
    - Controller Manager
    - Cloud Controller Manager

- **Worker Node**:
    - kubelet
    - kube-proxy
    - Container Runtime (Docker, containerd, CRI-O)

#### 2.1.3. Pod (پاد)

یک **Pod** کوچک‌ترین واحد deployable در Kubernetes است. یک Pod می‌تواند شامل:

- یک یا چند container
- Shared storage (volumes)
- Network IP address
- Configuration options

**مثال Pod:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-pod
spec:
  containers:
    - name: my-app
      image: my-app:1.0.0
      ports:
        - containerPort: 8080
```

#### 2.1.4. Deployment (استقرار)

یک **Deployment** controller است که Pods را مدیریت می‌کند. Deployment تضمین می‌کند که تعداد مشخصی از Pod replicas در حال
اجرا هستند.

**مثال Deployment:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-app:1.0.0
          ports:
            - containerPort: 8080
```

#### 2.1.5. Service (سرویس)

یک **Service** یک abstraction است که گروهی از Pods را با یک IP و DNS name یکپارچه می‌کند. Service load balancing داخلی
را فراهم می‌کند.

**انواع Service:**

1. **ClusterIP**: IP داخلی cluster (پیش‌فرض)
2. **NodePort**: درگاه باز در هر Node
3. **LoadBalancer**: IP خارجی از cloud provider
4. **ExternalName**: DNS name خارجی

**مثال Service:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

#### 2.1.6. Namespace (فضای نام)

یک **Namespace** یک محیط منطقی جداگانه در cluster است. برای جدا کردن resources مختلف استفاده می‌شود.

**Namespaceهای پیش‌فرض:**

- `default`: namespace پیش‌فرض
- `kube-system`: سیستم Kubernetes
- `kube-public`: منابع عمومی
- `kube-node-lease`: node heartbeat

**مثال Namespace:**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
```

#### 2.1.7. ConfigMap (نقشه پیکربندی)

یک **ConfigMap** برای ذخیره configuration data استفاده می‌شود که به Pods inject می‌شود.

**مثال ConfigMap:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-app-config
data:
  database_url: "postgresql://localhost:5432/mydb"
  log_level: "INFO"
```

#### 2.1.8. Secret (رمز)

یک **Secret** برای ذخیره داده‌های حساس مانند passwords، tokens، keys استفاده می‌شود.

**مثال Secret:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-app-secret
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: cGFzc3dvcmQ=  # base64 encoded
```

#### 2.1.9. Volume (حجم)

یک **Volume** storage است که با Pod lifecycle مرتبط است. انواع مختلف Volume وجود دارد:

- **emptyDir**: storage موقت
- **hostPath**: mount از host
- **PersistentVolumeClaim (PVC)**: storage پایدار
- **ConfigMap/Secret**: mount از ConfigMap/Secret

#### 2.1.10. PersistentVolume (PV) و PersistentVolumeClaim (PVC)

- **PersistentVolume (PV)**: storage resource در cluster
- **PersistentVolumeClaim (PVC)**: request برای storage

**مثال PVC:**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-app-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

#### 2.1.11. ReplicaSet (مجموعه رونوشت)

یک **ReplicaSet** تعداد مشخصی از Pod replicas را نگه می‌دارد. Deployment از ReplicaSet استفاده می‌کند.

#### 2.1.12. StatefulSet

یک **StatefulSet** برای stateful applications استفاده می‌شود که نیاز به:

- Stable network identity
- Stable persistent storage
- Ordered deployment و scaling

**مثال StatefulSet:**

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql-statefulset
spec:
  serviceName: mysql
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql:8.0
```

#### 2.1.13. DaemonSet

یک **DaemonSet** تضمین می‌کند که یک Pod در هر Node اجرا می‌شود. برای:

- Logging agents
- Monitoring agents
- Network plugins

**مثال DaemonSet:**

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-logging
  template:
    metadata:
      labels:
        name: fluentd-logging
    spec:
      containers:
        - name: fluentd
          image: fluent/fluentd:latest
```

#### 2.1.14. Job و CronJob

- **Job**: یک یا چند Pod را اجرا می‌کند تا completion
- **CronJob**: Job را در schedule منظم اجرا می‌کند

**مثال CronJob:**

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
spec:
  schedule: "0 2 * * *"  # هر روز ساعت 2 صبح
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: backup:latest
          restartPolicy: OnFailure
```

#### 2.1.15. Ingress

یک **Ingress** HTTP/HTTPS routing را به services فراهم می‌کند. Ingress controller مانند Nginx یا Traefik نیاز است.

**مثال Ingress:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-service
                port:
                  number: 80
```

#### 2.1.16. Horizontal Pod Autoscaler (HPA)

**HPA** به طور خودکار تعداد Pods را بر اساس metrics مانند CPU یا memory مقیاس می‌دهد.

**مثال HPA:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

#### 2.1.17. Vertical Pod Autoscaler (VPA)

**VPA** به طور خودکار resource requests و limits Pods را تنظیم می‌کند.

#### 2.1.18. NetworkPolicy

یک **NetworkPolicy** قوانین network traffic را بین Pods تعریف می‌کند.

**مثال NetworkPolicy:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: my-app-network-policy
spec:
  podSelector:
    matchLabels:
      app: my-app
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

#### 2.1.19. RBAC (Role-Based Access Control)

**RBAC** کنترل دسترسی بر اساس نقش‌ها را فراهم می‌کند.

**مولفه‌های RBAC:**

- **Role**: permissions در یک namespace
- **ClusterRole**: permissions در کل cluster
- **RoleBinding**: اتصال Role به User/Group
- **ClusterRoleBinding**: اتصال ClusterRole به User/Group

**مثال Role:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-reader
rules:
  - apiGroups: [ "" ]
    resources: [ "pods" ]
    verbs: [ "get", "list" ]
```

#### 2.1.20. Custom Resource Definition (CRD)

**CRD** امکان تعریف custom resources در Kubernetes را فراهم می‌کند.

---

## 3. معماری Kubernetes

### 3.1. معماری کلی Cluster

```
┌─────────────────────────────────────────────────────────┐
│                    Control Plane                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ API      │  │ etcd     │  │ Scheduler│            │
│  │ Server   │  │          │  │          │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│  ┌──────────┐  ┌──────────┐                          │
│  │ Controller│  │ Cloud     │                          │
│  │ Manager  │  │ Controller│                          │
│  └──────────┘  └──────────┘                          │
└─────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
│  Worker Node │  │  Worker Node │  │  Worker Node │
│  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │
│  │ kubelet│  │  │  │ kubelet│  │  │  │ kubelet│  │
│  └────────┘  │  │  └────────┘  │  │  └────────┘  │
│  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │
│  │kube-   │  │  │  │kube-   │  │  │  │kube-   │  │
│  │proxy   │  │  │  │proxy   │  │  │  │proxy   │  │
│  └────────┘  │  │  └────────┘  │  │  └────────┘  │
│  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │
│  │Runtime │  │  │  │Runtime │  │  │  │Runtime │  │
│  │(Docker)│  │  │  │(Docker)│  │  │  │(Docker)│  │
│  └────────┘  │  │  └────────┘  │  │  └────────┘  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 3.2. Control Plane Components

#### 3.2.1. API Server

- **وظیفه**: API RESTful برای تمام عملیات در cluster
- **مکان**: Master Node
- **پورت**: 6443 (HTTPS)

#### 3.2.2. etcd

- **وظیفه**: Key-value store برای cluster state
- **مکان**: Master Node
- **نسخه**: v3

#### 3.2.3. Scheduler

- **وظیفه**: تصمیم‌گیری برای قرار دادن Pods در Nodes
- **مکان**: Master Node

#### 3.2.4. Controller Manager

- **وظیفه**: اجرای controllers مختلف (Deployment, ReplicaSet, etc.)
- **مکان**: Master Node

#### 3.2.5. Cloud Controller Manager

- **وظیفه**: Integration با cloud providers
- **مکان**: Master Node (اختیاری)

### 3.3. Worker Node Components

#### 3.3.1. kubelet

- **وظیفه**: Agent که با API Server ارتباط برقرار می‌کند و Pods را مدیریت می‌کند
- **مکان**: Worker Node

#### 3.3.2. kube-proxy

- **وظیفه**: Network proxy برای Service load balancing
- **مکان**: Worker Node

#### 3.3.3. Container Runtime

- **وظیفه**: اجرای containers (Docker, containerd, CRI-O)
- **مکان**: Worker Node

### 3.4. Network Model

Kubernetes از **CNI (Container Network Interface)** برای networking استفاده می‌کند.

**اصول شبکه Kubernetes:**

1. **Pod-to-Pod Communication**: همه Pods می‌توانند بدون NAT با یکدیگر ارتباط برقرار کنند
2. **Node-to-Pod Communication**: همه Nodes می‌توانند بدون NAT با Pods ارتباط برقرار کنند
3. **Pod-to-Service Communication**: Pods می‌توانند با Services از طریق Cluster IP ارتباط برقرار کنند

**Pluginهای شبکه محبوب:**

- **Calico**: Network policy و security
- **Flannel**: ساده و سبک
- **Weave Net**: Network policy
- **Cilium**: eBPF-based networking

---

## 4. اجرای پروژه در Kubernetes (Stage و Production)

### 4.1. معماری پیشنهادی برای پروژه

#### 4.1.1. Namespace Structure

```
kubernetes/
├── namespaces/
│   ├── stage/
│   │   ├── backend-services/
│   │   ├── frontend/
│   │   ├── databases/
│   │   ├── messaging/
│   │   └── monitoring/
│   └── production/
│       ├── backend-services/
│       ├── frontend/
│       ├── databases/
│       ├── messaging/
│       └── monitoring/
```

#### 4.1.2. Deployment Strategy

**برای Stage Environment:**

- **Replicas**: 1-2 برای هر service
- **Resources**: محدودتر (CPU: 500m, Memory: 512Mi)
- **Auto-scaling**: غیرفعال یا محدود
- **Rolling Update**: با 1 replica

**برای Production Environment:**

- **Replicas**: 3+ برای هر service
- **Resources**: مناسب (CPU: 1000m, Memory: 1Gi+)
- **Auto-scaling**: فعال با HPA
- **Rolling Update**: با maxSurge=1, maxUnavailable=0

### 4.2. Backend Services Deployment

#### 4.2.1. Infrastructure Service

**deployment-infrastructure-stage.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: infrastructure-service
  namespace: stage
  labels:
    app: infrastructure-service
    env: stage
spec:
  replicas: 2
  selector:
    matchLabels:
      app: infrastructure-service
  template:
    metadata:
      labels:
        app: infrastructure-service
        env: stage
    spec:
      containers:
        - name: infrastructure-service
          image: registry.example.com/infrastructure-service:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              name: http
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: "stage"
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
              cpu: 500m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
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
---
apiVersion: v1
kind: Service
metadata:
  name: infrastructure-service
  namespace: stage
spec:
  selector:
    app: infrastructure-service
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: infrastructure-service-hpa
  namespace: stage
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: infrastructure-service
  minReplicas: 2
  maxReplicas: 5
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
```

**deployment-infrastructure-production.yaml:**

```yaml
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
          image: registry.example.com/infrastructure-service:v1.0.0
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
---
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
---
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
```

#### 4.2.2. Gateway Services

**deployment-gateway-ui-stage.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gateway-ui
  namespace: stage
  labels:
    app: gateway-ui
    env: stage
spec:
  replicas: 2
  selector:
    matchLabels:
      app: gateway-ui
  template:
    metadata:
      labels:
        app: gateway-ui
        env: stage
    spec:
      containers:
        - name: gateway-ui
          image: registry.example.com/gateway-ui:latest
          ports:
            - containerPort: 8080
              name: http
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: "stage"
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: gateway-ui
  namespace: stage
spec:
  selector:
    app: gateway-ui
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

### 4.3. Frontend Deployment

**deployment-frontend-stage.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: stage
  labels:
    app: frontend
    env: stage
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        env: stage
    spec:
      containers:
        - name: frontend
          image: registry.example.com/frontend:latest
          ports:
            - containerPort: 80
              name: http
          env:
            - name: API_URL
              value: "http://gateway-ui.stage.svc.cluster.local"
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
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: stage
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
```

### 4.4. Database Services

#### 4.4.1. CockroachDB StatefulSet

**cockroachdb-statefulset.yaml:**

```yaml
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
          image: cockroachdb/cockroach:v23.1.0
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
            - $(hostname).cockroachdb-public
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
        storageClassName: fast-ssd
```

#### 4.4.2. Redis Deployment

**redis-deployment.yaml:**

```yaml
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
          image: redis:7-alpine
          ports:
            - containerPort: 6379
              name: redis
          command:
            - redis-server
            - --appendonly yes
            - --requirepass $(REDIS_PASSWORD)
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
```

### 4.5. Kafka Deployment

**kafka-statefulset.yaml:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kafka-headless
  namespace: production
  labels:
    app: kafka
spec:
  ports:
    - port: 9092
      name: kafka
  clusterIP: None
  selector:
    app: kafka
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kafka
  namespace: production
spec:
  serviceName: kafka-headless
  replicas: 3
  selector:
    matchLabels:
      app: kafka
  template:
    metadata:
      labels:
        app: kafka
    spec:
      containers:
        - name: kafka
          image: confluentinc/cp-kafka:7.5.0
          ports:
            - containerPort: 9092
              name: kafka
          env:
            - name: KAFKA_BROKER_ID
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: KAFKA_ZOOKEEPER_CONNECT
              value: "zookeeper:2181"
            - name: KAFKA_ADVERTISED_LISTENERS
              value: "PLAINTEXT://$(hostname).kafka-headless:9092"
            - name: KAFKA_LISTENERS
              value: "PLAINTEXT://0.0.0.0:9092"
            - name: KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR
              value: "3"
          resources:
            requests:
              cpu: 2000m
              memory: 4Gi
            limits:
              cpu: 4000m
              memory: 8Gi
          volumeMounts:
            - name: kafka-data
              mountPath: /var/lib/kafka/data
  volumeClaimTemplates:
    - metadata:
        name: kafka-data
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 200Gi
        storageClassName: fast-ssd
```

### 4.6. Ingress Configuration

**ingress-stage.yaml:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: stage-ingress
  namespace: stage
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - stage-api.example.com
        - stage-app.example.com
      secretName: stage-tls
  rules:
    - host: stage-api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: gateway-ui
                port:
                  number: 80
    - host: stage-app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 80
```

**ingress-production.yaml:**

```yaml
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
```

### 4.7. ConfigMap و Secrets

**configmap-infrastructure-stage.yaml:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: infrastructure-config
  namespace: stage
data:
  database_url: "jdbc:postgresql://cockroachdb.stage.svc.cluster.local:26257/app_db"
  log_level: "INFO"
  spring_profiles_active: "stage"
---
apiVersion: v1
kind: Secret
metadata:
  name: infrastructure-secrets
  namespace: stage
type: Opaque
stringData:
  database_password: "your-secure-password"
  jwt_secret: "your-jwt-secret"
```

### 4.8. Network Policies

**network-policy-stage.yaml:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: stage
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
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - protocol: TCP
          port: 6379
    - to:
        - podSelector:
            matchLabels:
              app: kafka
      ports:
        - protocol: TCP
          port: 9092
```

---

## 5. نصب و راه‌اندازی Kubernetes Cluster

### 5.1. انتخاب روش نصب

#### 5.1.1. kubeadm (توصیه شده برای On-Premise)

**مزایا:**

- ساده و استاندارد
- مناسب برای learning
- مناسب برای small to medium clusters

**معایب:**

- نیاز به setup دستی بیشتر
- نیاز به maintenance بیشتر

#### 5.1.2. kops (برای AWS)

**مزایا:**

- مناسب برای AWS
- Production-ready

#### 5.1.3. kubespray

**مزایا:**

- Ansible-based
- مناسب برای multiple clouds
- Highly configurable

#### 5.1.4. Rancher

**مزایا:**

- UI-based management
- Multi-cluster management
- Easy setup

### 5.2. نصب با kubeadm (Rocky Linux 9)

#### 5.2.1. پیش‌نیازها

**الزامات سیستم:**

- حداقل 2 CPU cores
- حداقل 2GB RAM (برای master)، 1GB (برای worker)
- حداقل 20GB disk space
- Container runtime (containerd یا Docker)
- Network connectivity بین nodes

#### 5.2.2. تنظیمات اولیه (همه Nodes)

```bash
# غیرفعال کردن swap
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# تنظیمات kernel
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

# تنظیمات firewall
sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --permanent --add-port=2379-2380/tcp
sudo firewall-cmd --permanent --add-port=10250/tcp
sudo firewall-cmd --permanent --add-port=10251/tcp
sudo firewall-cmd --permanent --add-port=10252/tcp
sudo firewall-cmd --permanent --add-port=10255/tcp
sudo firewall-cmd --permanent --add-port=30000-32767/tcp
sudo firewall-cmd --reload

# نصب containerd
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y containerd.io
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd

# نصب kubeadm, kubelet, kubectl
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/repodata/repomd.xml.key
EOF

sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo systemctl enable --now kubelet
```

#### 5.2.3. نصب Master Node

```bash
# Initialize cluster
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# کپی کردن kubeconfig
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# نصب CNI plugin (Flannel)
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml

# بررسی status
kubectl get nodes
```

#### 5.2.4. اضافه کردن Worker Nodes

```bash
# در master node، دریافت join command
kubeadm token create --print-join-command

# در worker node، اجرای join command
sudo kubeadm join <master-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

### 5.3. نصب CNI Plugin

#### 5.3.1. Flannel (ساده و سبک)

```bash
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```

#### 5.3.2. Calico (با Network Policy)

```bash
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/custom-resources.yaml
```

### 5.4. نصب Ingress Controller (Nginx)

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
```

### 5.5. نصب Metrics Server

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### 5.6. بررسی نصب

```bash
# بررسی nodes
kubectl get nodes

# بررسی pods
kubectl get pods --all-namespaces

# بررسی services
kubectl get svc --all-namespaces

# بررسی cluster info
kubectl cluster-info
```

---

## 6. راه‌اندازی VM مدیریت و مانیتورینگ Rocky 9

### 6.1. هدف VM مدیریت

VM مدیریت برای موارد زیر استفاده می‌شود:

- **kubectl**: مدیریت Kubernetes cluster
- **Helm**: package manager برای Kubernetes
- **k9s/Lens**: UI tools برای مدیریت cluster
- **Monitoring Tools**: Prometheus, Grafana operators
- **CI/CD Tools**: ArgoCD, Jenkins (اختیاری)
- **Backup Tools**: Velero برای backup cluster

### 6.2. نصب OS و تنظیمات اولیه

#### 6.2.1. نصب Rocky Linux 9

```bash
# Update system
sudo dnf update -y

# نصب ابزارهای پایه
sudo dnf install -y vim git curl wget net-tools htop
```

#### 6.2.2. تنظیمات شبکه

```bash
# تنظیم hostname
sudo hostnamectl set-hostname k8s-management.example.com

# تنظیمات DNS
sudo vi /etc/hosts
# اضافه کردن:
# <master-ip> k8s-master
# <worker1-ip> k8s-worker1
# <worker2-ip> k8s-worker2
```

#### 6.2.3. تنظیمات SSH

```bash
# غیرفعال کردن password authentication
sudo vi /etc/ssh/sshd_config
# PasswordAuthentication no
sudo systemctl restart sshd
```

### 6.3. نصب kubectl

```bash
# نصب kubectl
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.28/rpm/repodata/repomd.xml.key
EOF

sudo dnf install -y kubectl

# بررسی نصب
kubectl version --client
```

### 6.4. کپی kubeconfig

```bash
# از master node کپی کردن
scp root@<master-ip>:/etc/kubernetes/admin.conf ~/.kube/config

# تنظیم permissions
mkdir -p ~/.kube
chmod 600 ~/.kube/config

# بررسی اتصال
kubectl get nodes
```

### 6.5. نصب Helm

```bash
# نصب Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# بررسی نصب
helm version

# اضافه کردن repos
helm repo add stable https://charts.helm.sh/stable
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### 6.6. نصب k9s (Terminal UI)

```bash
# نصب k9s
wget https://github.com/derailed/k9s/releases/download/v0.27.4/k9s_Linux_amd64.tar.gz
tar -xzf k9s_Linux_amd64.tar.gz
sudo mv k9s /usr/local/bin/
sudo chmod +x /usr/local/bin/k9s

# اجرا
k9s
```

### 6.7. نصب Lens (Desktop UI)

```bash
# دانلود و نصب Lens (نیاز به X11 یا VNC)
# از https://k8slens.dev/downloads دانلود کنید
```

### 6.8. نصب Prometheus Operator

```bash
# نصب Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set grafana.adminPassword=admin
```

### 6.9. نصب Grafana

```bash
# Grafana معمولاً با Prometheus Operator نصب می‌شود
# دسترسی به Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Login:
# Username: admin
# Password: admin (یا password تنظیم شده)
```

### 6.10. نصب Velero (Backup)

```bash
# نصب Velero CLI
wget https://github.com/vmware-tanzu/velero/releases/download/v1.12.0/velero-v1.12.0-linux-amd64.tar.gz
tar -xzf velero-v1.12.0-linux-amd64.tar.gz
sudo mv velero-v1.12.0-linux-amd64/velero /usr/local/bin/

# نصب Velero در cluster (نیاز به S3-compatible storage)
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket my-backup-bucket \
  --secret-file ./credentials-velero \
  --use-volume-snapshots=false \
  --backup-location-config region=us-west-2
```

### 6.11. نصب ArgoCD (GitOps)

```bash
# نصب ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# دریافت password اولیه
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port forward برای دسترسی
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### 6.12. اسکریپت‌های مفید

**k8s-utils.sh:**

```bash
#!/bin/bash

# بررسی status cluster
k8s-status() {
    echo "=== Nodes ==="
    kubectl get nodes
    echo ""
    echo "=== Pods (All namespaces) ==="
    kubectl get pods --all-namespaces
    echo ""
    echo "=== Services ==="
    kubectl get svc --all-namespaces
}

# Restart deployment
k8s-restart() {
    if [ -z "$1" ]; then
        echo "Usage: k8s-restart <deployment-name> [namespace]"
        return 1
    fi
    DEPLOYMENT=$1
    NAMESPACE=${2:-default}
    kubectl rollout restart deployment/$DEPLOYMENT -n $NAMESPACE
}

# Watch pods
k8s-watch() {
    NAMESPACE=${1:-default}
    watch kubectl get pods -n $NAMESPACE
}

# Logs
k8s-logs() {
    if [ -z "$1" ]; then
        echo "Usage: k8s-logs <pod-name> [namespace]"
        return 1
    fi
    POD=$1
    NAMESPACE=${2:-default}
    kubectl logs -f $POD -n $NAMESPACE
}

# Exec into pod
k8s-exec() {
    if [ -z "$1" ]; then
        echo "Usage: k8s-exec <pod-name> [namespace]"
        return 1
    fi
    POD=$1
    NAMESPACE=${2:-default}
    kubectl exec -it $POD -n $NAMESPACE -- /bin/bash
}
```

---

## 7. Load Balancing در Kubernetes

### 7.1. انواع Load Balancing

#### 7.1.1. Service Load Balancing (Built-in)

Kubernetes به طور خودکار load balancing را بین Pods یک Service انجام می‌دهد.

**مکانیزم:**

- **Round-robin**: به طور پیش‌فرض
- **Session affinity**: با `sessionAffinity: ClientIP`

**مثال:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

#### 7.1.2. Ingress Load Balancing

Ingress controller load balancing را در لایه HTTP/HTTPS انجام می‌دهد.

**مثال با Nginx Ingress:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/load-balance: "round_robin"
    nginx.ingress.kubernetes.io/upstream-hash-by: "$request_uri"
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-service
                port:
                  number: 80
```

#### 7.1.3. External Load Balancer (Cloud)

برای cloud providers، می‌توان از LoadBalancer service type استفاده کرد.

**مثال:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-lb
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

### 7.2. Load Balancing Strategies

#### 7.2.1. Round Robin (پیش‌فرض)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: round-robin-service
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
  # Round-robin به طور پیش‌فرض فعال است
```

#### 7.2.2. Session Affinity (Sticky Sessions)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: sticky-session-service
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

#### 7.2.3. Least Connections (با Nginx Ingress)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: least-conn-ingress
  annotations:
    nginx.ingress.kubernetes.io/upstream-keepalive-connections: "64"
    nginx.ingress.kubernetes.io/upstream-keepalive-requests: "100"
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-service
                port:
                  number: 80
```

### 7.3. Load Balancing برای پروژه

#### 7.3.1. Gateway Services

```yaml
apiVersion: v1
kind: Service
metadata:
  name: gateway-ui
  namespace: production
spec:
  selector:
    app: gateway-ui
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
  sessionAffinity: None  # Stateless services
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gateway-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/load-balance: "round_robin"
    nginx.ingress.kubernetes.io/upstream-keepalive-connections: "64"
spec:
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

#### 7.3.2. Database Connection Pooling

برای CockroachDB و سایر databases، connection pooling در application layer انجام می‌شود.

**Spring Boot Configuration:**

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
```

### 7.4. Load Testing

```bash
# نصب k6 (load testing tool)
sudo dnf install -y https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.rpm

# اجرای load test
k6 run load-test.js
```

**load-test.js:**

```javascript
import http from 'k6/http';
import {check, sleep} from 'k6';

export const options = {
    stages: [
        {duration: '30s', target: 100},
        {duration: '1m', target: 200},
        {duration: '30s', target: 0},
    ],
};

export default function () {
    const res = http.get('http://api.example.com/health');
    check(res, {'status was 200': (r) => r.status == 200});
    sleep(1);
}
```

---

## 8. مانیتورینگ و Observability

### 8.1. Prometheus

#### 8.1.1. نصب Prometheus Operator

```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

#### 8.1.2. ServiceMonitor برای Spring Boot

**servicemonitor-backend.yaml:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: infrastructure-service-monitor
  namespace: production
  labels:
    app: infrastructure-service
spec:
  selector:
    matchLabels:
      app: infrastructure-service
  endpoints:
    - port: http
      path: /actuator/prometheus
      interval: 30s
```

#### 8.1.3. Spring Boot Actuator Configuration

**application.yaml:**

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: ${spring.application.name}
      environment: ${spring.profiles.active}
```

### 8.2. Grafana

#### 8.2.1. Dashboard برای Spring Boot

**grafana-dashboard-springboot.yaml:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: springboot-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  springboot.json: |
    {
      "dashboard": {
        "title": "Spring Boot Application",
        "panels": [...]
      }
    }
```

#### 8.2.2. دسترسی به Grafana

```bash
# Port forward
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# دریافت password
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 -d
```

### 8.3. Distributed Tracing

#### 8.3.1. Jaeger

```bash
# نصب Jaeger با Helm
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm install jaeger jaegertracing/jaeger
```

#### 8.3.2. Spring Boot Integration

**pom.xml:**

```xml

<dependency>
    <groupId>io.jaegertracing</groupId>
    <artifactId>jaeger-client</artifactId>
</dependency>
<dependency>
<groupId>io.opentracing.contrib</groupId>
<artifactId>opentracing-spring-jaeger-starter</artifactId>
</dependency>
```

**application.yaml:**

```yaml
opentracing:
  jaeger:
    enabled: true
    service-name: infrastructure-service
    udp-sender:
      host: jaeger-agent.monitoring.svc.cluster.local
      port: 6831
```

### 8.4. Logging

#### 8.4.1. ELK Stack

```bash
# نصب ELK Stack با Helm
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch
helm install logstash elastic/logstash
helm install kibana elastic/kibana
```

#### 8.4.2. Loki (سبک‌تر از ELK)

```bash
# نصب Loki
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack
```

#### 8.4.3. Fluentd DaemonSet

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      containers:
        - name: fluentd
          image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
          env:
            - name: ELASTICSEARCH_HOST
              value: "elasticsearch.logging.svc.cluster.local"
            - name: ELASTICSEARCH_PORT
              value: "9200"
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: varlibdockercontainers
              mountPath: /var/lib/docker/containers
              readOnly: true
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: varlibdockercontainers
          hostPath:
            path: /var/lib/docker/containers
```

### 8.5. Alerting

#### 8.5.1. Prometheus Alertmanager

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-config
  namespace: monitoring
data:
  alertmanager.yml: |
    global:
      resolve_timeout: 5m
    route:
      group_by: ['alertname']
      group_wait: 10s
      group_interval: 10s
      repeat_interval: 12h
      receiver: 'web.hook'
    receivers:
    - name: 'web.hook'
      webhook_configs:
      - url: 'http://alert-webhook:5001/'
    inhibit_rules:
      - source_match:
          severity: 'critical'
        target_match:
          severity: 'warning'
        equal: ['alertname', 'dev', 'instance']
```

#### 8.5.2. Alert Rules

**alert-rules.yaml:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: application-alerts
  namespace: production
spec:
  groups:
    - name: application.rules
      rules:
        - alert: HighErrorRate
          expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High error rate detected"
            description: "Error rate is {{ $value }} errors per second"

        - alert: HighCPUUsage
          expr: container_cpu_usage_seconds_total > 0.8
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High CPU usage"
            description: "CPU usage is {{ $value }}%"

        - alert: PodCrashLooping
          expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Pod is crash looping"
            description: "Pod {{ $labels.pod }} is crash looping"
```

---

## 9. چالش‌ها و راه‌حل‌ها

### 9.1. چالش‌های عملیاتی

#### 9.1.1. پیچیدگی بالا

**چالش:**

- Kubernetes یک سیستم پیچیده است و یادگیری آن زمان‌بر است
- نیاز به دانش عمیق در networking، storage، security

**راه‌حل:**

- استفاده از managed Kubernetes (EKS, GKE, AKS)
- آموزش تیم و استفاده از documentation
- شروع از محیط stage و سپس production
- استفاده از tools مدیریتی مانند Lens, k9s

#### 9.1.2. Resource Management

**چالش:**

- تعیین دقیق resource requests و limits دشوار است
- Over-provisioning یا under-provisioning منابع

**راه‌حل:**

- استفاده از VPA (Vertical Pod Autoscaler) برای تنظیم خودکار
- Monitoring و profiling applications
- استفاده از ResourceQuota برای محدودیت منابع
- Load testing برای تعیین نیازهای واقعی

**مثال ResourceQuota:**

```yaml
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
```

#### 9.1.3. Storage Management

**چالش:**

- مدیریت persistent storage پیچیده است
- Stateful applications نیاز به storage پایدار دارند

**راه‌حل:**

- استفاده از StorageClass برای dynamic provisioning
- استفاده از StatefulSet برای stateful applications
- Backup و restore strategy با Velero
- استفاده از cloud storage (EBS, GCE Persistent Disk)

**مثال StorageClass:**

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  fsType: ext4
allowVolumeExpansion: true
```

#### 9.1.4. Networking Complexity

**چالش:**

- Networking در Kubernetes پیچیده است
- Service discovery و load balancing نیاز به درک عمیق دارد

**راه‌حل:**

- استفاده از CNI plugins محبوب (Calico, Flannel)
- استفاده از Service و Ingress برای routing
- Network Policies برای security
- استفاده از Service Mesh (Istio, Linkerd) برای مدیریت پیچیده‌تر

#### 9.1.5. Security

**چالش:**

- امنیت در Kubernetes چند لایه است
- نیاز به RBAC، Network Policies، Pod Security Policies

**راه‌حل:**

- پیاده‌سازی RBAC مناسب
- استفاده از Network Policies برای محدود کردن ترافیک
- Secret management با Vault یا Sealed Secrets
- Regular security audits و updates
- استفاده از Pod Security Standards

**مثال RBAC:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer-role
  namespace: production
rules:
  - apiGroups: [ "" ]
    resources: [ "pods", "services" ]
    verbs: [ "get", "list", "watch" ]
  - apiGroups: [ "apps" ]
    resources: [ "deployments" ]
    verbs: [ "get", "list", "create", "update" ]
---
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
```

### 9.2. چالش‌های مربوط به پروژه

#### 9.2.1. Migration از Docker Compose به Kubernetes

**چالش:**

- تبدیل docker-compose.yml به Kubernetes manifests
- تفاوت در networking و service discovery

**راه‌حل:**

- استفاده از Kompose برای تبدیل خودکار
- بازنویسی دستی برای کنترل بهتر
- تست در محیط stage قبل از production
- Migration تدریجی

**استفاده از Kompose:**

```bash
# نصب Kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.28.0/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo mv kompose /usr/local/bin/

# تبدیل docker-compose.yml
kompose convert

# یا با output به فایل
kompose convert -o k8s/
```

#### 9.2.2. Database Deployment

**چالش:**

- CockroachDB و ClickHouse نیاز به stateful deployment دارند
- Backup و restore پیچیده است

**راه‌حل:**

- استفاده از StatefulSet برای databases
- Persistent Volumes برای data persistence
- Operator pattern برای مدیریت پیچیده (CockroachDB Operator)
- Backup strategy با cron jobs یا operators

#### 9.2.3. Kafka Deployment

**چالش:**

- Kafka نیاز به persistent storage دارد
- Zookeeper dependency
- Configuration پیچیده

**راه‌حل:**

- استفاده از StatefulSet برای Kafka
- استفاده از Kafka Operator (Strimzi)
- KRaft mode (بدون Zookeeper) در نسخه‌های جدید
- Persistent Volumes برای topics data

**مثال با Strimzi Operator:**

```yaml
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
```

#### 9.2.4. Spring Boot Application Configuration

**چالش:**

- Configuration management برای Spring Boot در Kubernetes
- Service discovery و connection strings

**راه‌حل:**

- استفاده از ConfigMap برای configuration
- استفاده از Secret برای sensitive data
- Service discovery با DNS names
- Spring Cloud Kubernetes برای integration بهتر

**مثال Service Discovery:**

```yaml
# application.yaml در Spring Boot
spring:
  datasource:
    url: jdbc:postgresql://cockroachdb.production.svc.cluster.local:26257/app_db
  kafka:
    bootstrap-servers: my-cluster-kafka-bootstrap.production.svc.cluster.local:9092
```

### 9.3. چالش‌های Performance

#### 9.3.1. Cold Start

**چالش:**

- Pods جدید نیاز به زمان برای start دارند
- JVM warmup برای Java applications

**راه‌حل:**

- استفاده از startupProbe برای wait برای readiness
- Pre-warming containers با init containers
- استفاده از HPA برای maintain minimum replicas
- JVM tuning برای کاهش startup time

#### 9.3.2. Resource Contention

**چالش:**

- Competition برای resources در cluster
- Noisy neighbor problem

**راه‌حل:**

- استفاده از ResourceQuota و LimitRange
- Node affinity و anti-affinity
- Quality of Service (QoS) classes
- Resource requests و limits مناسب

**مثال LimitRange:**

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
  namespace: production
spec:
  limits:
    - default:
        memory: "512Mi"
        cpu: "500m"
      defaultRequest:
        memory: "256Mi"
        cpu: "250m"
      type: Container
```

---