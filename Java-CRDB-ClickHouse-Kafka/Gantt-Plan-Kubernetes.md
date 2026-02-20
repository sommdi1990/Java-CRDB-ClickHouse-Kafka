# گانت‌چارت بر مبنای پروپوزال Kubernetes – ۴ اسپرینت سه‌هفته‌ای (هر اسپرینت ۱۰۸ ساعت)

- ظرفیت: شنبه تا چهارشنبه روزی ۴ ساعت (۵ روز) + پنج‌شنبه و جمعه روزی ۸ ساعت → ۳۶ ساعت در هفته → ۱۰۸ ساعت در هر اسپرینت
  سه‌هفته‌ای.
- محدوده: راه‌اندازی کامل Kubernetes Cluster روی دو سرور فیزیکی (64GB RAM هر کدام) با VMware ESXi 8، Rocky Linux 10، و
  استقرار تمام سرویس‌ها و ابزارهای زیرساختی در Kubernetes. یک نفر توسعه‌دهنده.
- هر اسپرینت شامل زمان مستندسازی/گزارش جداگانه است.

## اسپرینت ۰ (آماده‌سازی زیرساخت فیزیکی، VMware ESXi 8، Rocky Linux 10، و Kubernetes Cluster پایه) – ۱۰۸ ساعت

| ردیف | فعالیت                                                                                                                   | تخمین (ساعت) | پیش‌نیاز / هم‌نیاز |
|------|--------------------------------------------------------------------------------------------------------------------------|--------------|--------------------|
| 0.1  | راه‌اندازی و تست iDRAC/iLO روی دو سرور فیزیکی (64GB RAM هر کدام)، تنظیم IP و دسترسی از راه دور                           | 6            | —                  |
| 0.2  | نصب VMware ESXi 8.0 از راه دور (Remote Media Mount یا PXE) روی هر دو سرور و کانفیگ Management Network                    | 12           | 0.1                |
| 0.3  | تنظیم vSphere Client/Web Client و دسترسی از راه دور به ESXi، تست Remote Console و vMotion                                | 4            | 0.2                |
| 0.4  | طراحی شبکه داخلی VMها و VLAN مناسب برای Kubernetes Cluster، تنظیم Firewall و Network Segmentation                        | 6            | 0.2                |
| 0.5  | راه‌اندازی VM template با Rocky Linux 10 (Cloud-init/Kickstart) و تهیه کلون محیط آماده                                   | 8            | 0.3–0.4            |
| 0.6  | ایجاد VMها برای Kubernetes: Master Node (سرور 1)، Worker Node 1 (سرور 1)، Worker Node 2 (سرور 2)، Management VM (سرور 2) | 8            | 0.5                |
| 0.7  | نصب و تنظیم Rocky Linux 10 روی همه VMهای Kubernetes (Master + Workers + Management) از راه دور                           | 10           | 0.6                |
| 0.8  | تنظیم SSH Key-based Authentication روی همه VMها و غیرفعال کردن Password Authentication                                   | 4            | 0.7                |
| 0.9  | تنظیمات اولیه همه Nodes: غیرفعال کردن Swap، تنظیمات Kernel (overlay, br_netfilter, ip_forward)                           | 4            | 0.8                |
| 0.10 | تنظیمات Firewall روی همه Nodes (پورت‌های Kubernetes: 6443, 2379-2380, 10250-10252, 30000-32767)                          | 4            | 0.9                |
| 0.11 | نصب Container Runtime (containerd) روی همه Nodes و تنظیم SystemdCgroup                                                   | 6            | 0.9                |
| 0.12 | نصب kubeadm, kubelet, kubectl روی همه Nodes از Kubernetes Repository                                                     | 4            | 0.11               |
| 0.13 | Initialize Kubernetes Master Node با kubeadm و تنظیم pod-network-cidr                                                    | 6            | 0.12               |
| 0.14 | تنظیم kubeconfig روی Master Node و Management VM                                                                         | 2            | 0.13               |
| 0.15 | Join Worker Node 1 و Worker Node 2 به Cluster                                                                            | 4            | 0.13               |
| 0.16 | نصب CNI Plugin (Flannel یا Calico) و بررسی اتصال Nodes                                                                   | 4            | 0.15               |
| 0.17 | نصب Nginx Ingress Controller (با Helm یا kubectl)                                                                        | 4            | 0.16               |
| 0.18 | نصب Metrics Server برای HPA و بررسی top nodes/pods                                                                       | 2            | 0.16               |
| 0.19 | نصب Helm روی Management VM و اضافه کردن Helm Repositories (prometheus, grafana, ingress-nginx)                           | 4            | 0.14               |
| 0.20 | راه‌اندازی Monitoring Stack پایه: Prometheus Operator و Grafana با Helm                                                  | 6            | 0.19               |
| 0.21 | ایجاد Namespaces برای environments (dev, stage, production, infrastructure, system)                                      | 2            | 0.16               |
| 0.22 | تست کلی Cluster: بررسی Nodes، Pods، Services، و Network Connectivity                                                     | 4            | 0.16–0.21          |
| 0.23 | Harden و SecOps پایه: تنظیم RBAC اولیه، Network Policies پایه، Pod Security Standards                                    | 4            | 0.16               |
| 0.24 | آماده‌سازی Runbook مستند زیرساخت Kubernetes، mapping شبکه، مستند دسترسی‌های از راه دور                                   | 4            | 0.5–0.23           |
| 0.25 | بافر/ریسک‌پذیری برای رفع موارد پیش‌بینی‌نشده                                                                             | 2            | 0.1–0.24           |
| 0.26 | مستندسازی و گزارش اسپرینت                                                                                                | 2            | 0.1–0.25           |

## اسپرینت ۱ (استقرار Databases، Messaging، و Backend Services در Kubernetes) – ۱۰۸ ساعت

| ردیف | فعالیت                                                                                                | تخمین (ساعت) | پیش‌نیاز / هم‌نیاز |
|------|-------------------------------------------------------------------------------------------------------|--------------|--------------------|
| 1.1  | ایجاد StorageClass برای Persistent Volumes و تست Dynamic Provisioning                                 | 4            | 0.x                |
| 1.2  | استقرار CockroachDB با StatefulSet (3 replicas) در namespace production، Persistent Volumes، Services | 10           | 1.1                |
| 1.3  | استقرار ClickHouse با StatefulSet یا Helm Chart (3 replicas) در namespace production                  | 8            | 1.1                |
| 1.4  | استقرار Redis با Deployment (3 replicas) و Sentinel برای HA در namespace production                   | 8            | 1.1                |
| 1.5  | ایجاد ConfigMaps و Secrets برای Databases (CockroachDB, ClickHouse, Redis)                            | 4            | 1.2–1.4            |
| 1.6  | تست اتصال Databases و بررسی Health Checks                                                             | 4            | 1.2–1.5            |
| 1.7  | **ارزیابی و انتخاب**: مطالعه مقایسه Redpanda و Kafka، تصمیم‌گیری (توصیه: Redpanda)                    | 2            | 0.x                |
| 1.8  | استقرار Redpanda با Helm Chart (3 replicas) یا Kafka با Strimzi Operator در namespace production      | 10           | 1.7                |
| 1.9  | استقرار Schema Registry (Redpanda Built-in یا Confluent) و تعریف قرارداد رویدادهای پایه               | 6            | 1.8                |
| 1.10 | اسکریپت‌های مدیریت Topic (ایجاد، Retention، Partition) و تست end-to-end                               | 6            | 1.8–1.9            |
| 1.11 | مانیتورینگ Databases و Messaging: ServiceMonitors برای Prometheus، Dashboards در Grafana              | 6            | 1.2–1.8, 0.20      |
| 1.12 | اسکلت Backend Services: Infrastructure Service، Gateway UI/External/Input با Helm Charts              | 10           | 1.5                |
| 1.13 | ایجاد ConfigMaps و Secrets برای Backend Services (Database URLs, JWT Secrets, و غیره)                 | 6            | 1.5, 1.12          |
| 1.14 | Deploy Infrastructure Service در namespace production با Deployment، Service، HPA                     | 8            | 1.12–1.13          |
| 1.15 | Deploy Gateway Services (UI, External, Input) در namespace production                                 | 8            | 1.12–1.13          |
| 1.16 | تنظیم Health Checks (liveness, readiness, startup probes) برای Backend Services                       | 4            | 1.14–1.15          |
| 1.17 | تست اتصال Backend Services به Databases و Messaging                                                   | 4            | 1.14–1.16          |
| 1.18 | تنظیم Resource Requests/Limits و ResourceQuota برای namespace production                              | 4            | 1.14–1.15          |
| 1.19 | بافر/ریسک‌پذیری برای رفع موارد پیش‌بینی‌نشده                                                          | 2            | 1.1–1.18           |
| 1.20 | مستندسازی و گزارش اسپرینت                                                                             | 2            | 1.1–1.19           |

**نکته**: با توجه به مزایای Redpanda (performance بالا، operational simplicity، بدون ZooKeeper)، **توصیه می‌شود از
Redpanda استفاده شود**.

## اسپرینت ۲ (استقرار Frontend، Infrastructure Tools، و Security) – ۱۰۸ ساعت

| ردیف | فعالیت                                                                                     | تخمین (ساعت) | پیش‌نیاز / هم‌نیاز |
|------|--------------------------------------------------------------------------------------------|--------------|--------------------|
| 2.1  | Deploy Frontend Services (Main Page, User Panel, Admin Panel) در namespace production      | 10           | 1.x                |
| 2.2  | تنظیم Ingress Rules برای Frontend و Backend Services (dev, stage, production environments) | 8            | 2.1, 0.17          |
| 2.3  | تنظیم SSL/TLS با Cert-Manager و Let's Encrypt برای Ingress                                 | 6            | 2.2                |
| 2.4  | Deploy Jira با Helm Chart در namespace infrastructure                                      | 8            | 1.x                |
| 2.5  | Deploy Confluence با Helm Chart در namespace infrastructure                                | 8            | 1.x                |
| 2.6  | Deploy Git Server (GitLab یا Bitbucket) با Helm Chart در namespace infrastructure          | 8            | 1.x                |
| 2.7  | Deploy CI/CD Tools: Jenkins با Helm Chart در namespace infrastructure                      | 6            | 2.6                |
| 2.8  | Deploy ArgoCD برای GitOps در namespace infrastructure                                      | 6            | 2.6                |
| 2.9  | Deploy File Management: Nextcloud با Helm Chart در namespace infrastructure                | 6            | 1.x                |
| 2.10 | Deploy Mayan EDMS در namespace infrastructure (در صورت نیاز)                               | 4            | 1.x                |
| 2.11 | راه‌اندازی Keycloak با Helm Chart در namespace infrastructure (2 replicas)                 | 8            | 1.x                |
| 2.12 | تنظیم Keycloak: Realm, Clients, Roles, Users automation (seed scripts)                     | 6            | 2.11               |
| 2.13 | Integration Keycloak با Backend Services: OAuth2/OIDC configuration                        | 6            | 2.11–2.12          |
| 2.14 | تنظیم RBAC در Kubernetes: Roles, RoleBindings, ClusterRoles برای developers و admins       | 6            | 0.16               |
| 2.15 | تنظیم Network Policies برای جداسازی ترافیک بین namespaces و pods                           | 6            | 0.16               |
| 2.16 | تنظیم Pod Security Standards و Security Contexts برای Pods                                 | 4            | 0.16               |
| 2.17 | تست Security: RBAC, Network Policies, Pod Security                                         | 4            | 2.14–2.16          |
| 2.18 | بافر/ریسک‌پذیری برای رفع موارد پیش‌بینی‌نشده                                               | 2            | 2.1–2.17           |
| 2.19 | مستندسازی و گزارش اسپرینت                                                                  | 2            | 2.1–2.18           |

## اسپرینت ۳ (Monitoring، Observability، Backup/DR، و بهینه‌سازی) – ۱۰۸ ساعت

| ردیف | فعالیت                                                                                     | تخمین (ساعت) | پیش‌نیاز / هم‌نیاز |
|------|--------------------------------------------------------------------------------------------|--------------|--------------------|
| 3.1  | راه‌اندازی کامل Prometheus Stack: ServiceMonitors برای تمام Backend Services               | 8            | 1.x, 0.20          |
| 3.2  | ایجاد Custom Dashboards در Grafana برای Backend Services، Databases، Messaging             | 8            | 3.1                |
| 3.3  | راه‌اندازی Distributed Tracing: Jaeger یا Zipkin در namespace monitoring                   | 6            | 1.x                |
| 3.4  | Integration OpenTelemetry با Backend Services برای Tracing                                 | 6            | 3.3                |
| 3.5  | راه‌اندازی Centralized Logging: ELK Stack یا Loki در namespace monitoring                  | 8            | 1.x                |
| 3.6  | تنظیم Fluentd/Fluent Bit DaemonSet برای Log Collection                                     | 4            | 3.5                |
| 3.7  | تنظیم Alertmanager و Alert Rules برای Critical Events (High CPU, Pod Crash, Database Down) | 6            | 3.1                |
| 3.8  | نصب Velero CLI روی Management VM                                                           | 2            | 0.14               |
| 3.9  | نصب Velero در Cluster و تنظیم Backup Location (S3-compatible storage)                      | 6            | 3.8                |
| 3.10 | ایجاد Backup Schedule با Velero برای تمام namespaces (daily backup)                        | 4            | 3.9                |
| 3.11 | ایجاد CronJobs برای Database Backups: CockroachDB, ClickHouse, Redis                       | 6            | 1.2–1.4            |
| 3.12 | تست Backup و Restore: Velero restore test، Database restore test                           | 6            | 3.10–3.11          |
| 3.13 | تنظیم Disaster Recovery Plan: RTO/RPO definitions، Recovery Procedures                     | 4            | 3.12               |
| 3.14 | Deploy Services در namespace dev و stage (کپی از production با تنظیمات متفاوت)             | 8            | 1.x, 2.x           |
| 3.15 | تنظیم ResourceQuota و LimitRange برای namespaces (dev, stage, production)                  | 4            | 3.14               |
| 3.16 | تنظیم HPA (Horizontal Pod Autoscaler) برای Backend Services                                | 6            | 1.14–1.15          |
| 3.17 | Performance Tuning: JVM tuning برای Java Services، Database tuning                         | 6            | 1.x                |
| 3.18 | Load Testing: تست Load با k6 یا Apache JMeter و بررسی Auto-scaling                         | 6            | 3.16               |
| 3.19 | بهینه‌سازی Resource Allocation: بررسی و تنظیم Resource Requests/Limits                     | 4            | 3.18               |
| 3.20 | Port Management: مستندسازی Port Allocation برای تمام Services و Environments               | 2            | 2.2                |
| 3.21 | Runbook کامل: SOPهای Restart، Backup/Restore، Capacity Planning، Troubleshooting           | 6            | 3.1–3.20           |
| 3.22 | بافر/ریسک‌پذیری برای رفع موارد پیش‌بینی‌نشده                                               | 2            | 3.1–3.21           |
| 3.23 | مستندسازی و گزارش اسپرینت                                                                  | 2            | 3.1–3.22           |

## اسپرینت ۴ (تست نهایی، بهینه‌سازی، و Go-Live) – ۱۰۸ ساعت

| ردیف | فعالیت                                                                            | تخمین (ساعت) | پیش‌نیاز / هم‌نیاز |
|------|-----------------------------------------------------------------------------------|--------------|--------------------|
| 4.1  | تست Integration کامل: تست اتصال تمام Services به Databases و Messaging            | 8            | 1.x, 2.x           |
| 4.2  | تست End-to-End: تست کامل Flow از Frontend تا Backend تا Database                  | 8            | 2.1–2.2            |
| 4.3  | تست Security: Penetration Testing، RBAC Testing، Network Policy Testing           | 8            | 2.14–2.16          |
| 4.4  | تست Load و Stress: Load Testing با ترافیک واقعی، بررسی Performance و Auto-scaling | 8            | 3.18               |
| 4.5  | تست Disaster Recovery: تست کامل Backup/Restore، Failover Testing                  | 6            | 3.12–3.13          |
| 4.6  | تست High Availability: تست Pod Failure، Node Failure، Service Recovery            | 6            | 1.x, 2.x           |
| 4.7  | تست Rolling Updates: تست Zero-Downtime Deployment و Rollback                      | 4            | 1.x                |
| 4.8  | بررسی و رفع مشکلات Performance: Optimization بر اساس نتایج Load Testing           | 8            | 4.4                |
| 4.9  | بررسی و رفع مشکلات Security: Security Audit و Hardening                           | 6            | 4.3                |
| 4.10 | بررسی و رفع مشکلات Monitoring: بهبود Dashboards و Alerts                          | 4            | 3.1–3.7            |
| 4.11 | مستندسازی کامل: Architecture Documentation، Deployment Guide، Operations Manual   | 10           | 1.x–3.x            |
| 4.12 | آموزش تیم: آموزش Kubernetes Basics، Deployment Procedures، Troubleshooting        | 8            | 4.11               |
| 4.13 | Production Readiness Checklist: بررسی تمام موارد برای Go-Live                     | 4            | 4.1–4.12           |
| 4.14 | Production Deployment: Deploy نهایی در Production Environment                     | 6            | 4.13               |
| 4.15 | Post-Deployment Monitoring: مانیتورینگ 24-48 ساعت اول پس از Go-Live               | 4            | 4.14               |
| 4.16 | بافر/ریسک‌پذیری برای رفع موارد پیش‌بینی‌نشده                                      | 4            | 4.1–4.15           |
| 4.17 | مستندسازی و گزارش نهایی اسپرینت                                                   | 2            | 4.1–4.16           |

## وابستگی‌ها (خلاصه)

- اسپرینت ۰ باید پیش از سایر اسپرینت‌ها کامل شود (زیرساخت فیزیکی، VMware ESXi 8، Rocky Linux 10، و Kubernetes Cluster
  پایه).
- اسپرینت ۱ به آماده بودن Kubernetes Cluster (اسپرینت ۰) متکی است و شامل استقرار Databases، Messaging، و Backend
  Services است.
- اسپرینت ۲ به استقرار Databases و Backend Services (اسپرینت ۱) متکی است و شامل Frontend، Infrastructure Tools، و
  Security است.
- اسپرینت ۳ به تمام Services مستقر (اسپرینت ۱ و ۲) متکی است و شامل Monitoring، Observability، Backup/DR، و بهینه‌سازی
  است.
- اسپرینت ۴ (تست نهایی و Go-Live) پس از آماده بودن تمام Services و Infrastructure (اسپرینت ۰–۳) شروع می‌شود.

## نکات برنامه‌ریزی

- ظرفیت هر اسپرینت ۱۰۸ ساعت است (۳۶ ساعت در هفته × ۳ هفته)؛ جمع فعالیت‌ها در هر اسپرینت <= ۱۰۸ ساعت نگه داشته شده است.
- برای هر فعالیت، خروجی قابل تحویل (deployment + چک‌لیست تست + مستند) تعریف شود تا ورود به اسپرینت بعدی بدون بدهی انجام
  شود.
- مستندسازی و گزارش در انتهای هر اسپرینت به صورت جداگانه لحاظ شده تا نیاز به فاز مجزا نباشد.
- با توجه به پیچیدگی Kubernetes و نیاز به تخصص، توصیه می‌شود تیم فنی آموزش‌های لازم را ببیند.
- برای Production Environment، توصیه می‌شود حداقل 2-3 نفر با تخصص Kubernetes در دسترس باشند.

## تفاوت‌های کلیدی با گانت چارت قبلی

1. **تمرکز بر Kubernetes**: تمام فعالیت‌ها حول محور Kubernetes و استقرار در Kubernetes است.
2. **زیرساخت فیزیکی**: شامل راه‌اندازی دو سرور فیزیکی با VMware ESXi 8 و Rocky Linux 10.
3. **Infrastructure Tools در Kubernetes**: Jira، Confluence، Git، CI/CD، File Management همه در Kubernetes deploy
   می‌شوند.
4. **Monitoring و Observability پیشرفته**: Prometheus Stack، Jaeger، ELK Stack/Loki.
5. **Backup و DR**: Velero برای Kubernetes resources و Database backup scripts.
6. **Security پیشرفته**: RBAC، Network Policies، Pod Security Standards.
7. **Multi-Environment**: dev، stage، production با Namespace separation.

---

<div align="center">

[↑ بازگشت به بالا](#گانتچارت-بر-مبنای-پروپوزال-kubernetes--۴-اسپرینت-سههفتهای-هر-اسپرینت-۱۰۸-ساعت) | [← بازگشت به صفحه اصلی](Home) | [پروپوزال Kubernetes](Proposal-Kubernetes) | [راهنمای فنی پیاده‌سازی](Kubernetes-Implementation-Guide)

</div>

