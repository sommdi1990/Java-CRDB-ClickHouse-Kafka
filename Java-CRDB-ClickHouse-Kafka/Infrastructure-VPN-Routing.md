# VPN Gateway و Routing هوشمند برای زیرساخت

<div align="right">

[← بازگشت به صفحه اصلی](Home) | [زیرساخت](Infrastructure-Setup)

</div>

---

## ۱. مقدمه و صورت مسئله

### ۱.۱. سناریو

در زیرساخت پروژه با دو سرور فیزیکی VMware ESXi 8.0 و تعداد زیادی VM با Rocky Linux 9، نیاز به یک سیستم VPN Gateway مرکزی
وجود دارد که:

- **تمام ترافیک اینترنت** از تمام VMها از طریق این Gateway عبور کند
- **Routing هوشمند**: در صورت قرار گرفتن مقصد در لیست VPNهای ثبت‌شده، ترافیک از طریق VPN مناسب مسیریابی شود
- **مثال عملی**: اتصال به Docker Hub، GitHub، و سایر سرویس‌های خارجی باید از طریق VPN عبور کند

### ۱.۲. معماری پیشنهادی

```
┌─────────────────────────────────────────────────────────┐
│               VMware ESXi Environment                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Rocky Linux  │  │ Rocky Linux  │  │ Rocky Linux  │  │
│  │  VM (Dev)    │  │  VM (Prod)   │  │  VM (DB)     │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│         └──────────────────┼──────────────────┘          │
│                            │                             │
│         ┌──────────────────▼──────────────────┐          │
│         │   VPN Gateway VM (Rocky Linux 9)    │          │
│         │   - OpenVPN / WireGuard / StrongSwan│          │
│         │   - Policy-based Routing            │          │
│         │   - VPN Client Connections          │          │
│         └──────────────────┬──────────────────┘          │
│                            │                             │
└────────────────────────────┼─────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Internet       │
                    │  + VPN Servers  │
                    └─────────────────┘
```

---

## ۲. ابزارهای پیشنهادی

### ۲.۱. VPN Gateway Solutions

#### ۱. **pfSense** (پیشنهاد اول)

**توضیح**: یک firewall/router distribution بر پایه FreeBSD که قابلیت‌های VPN Gateway قدرتمندی دارد.

**مزایا**:

- رابط کاربری وب گرافیکی (Web UI)
- پشتیبانی از OpenVPN، WireGuard، IPsec
- Policy-based routing و Rule-based routing
- Traffic shaping و Quality of Service (QoS)
- مانیتورینگ و Logging پیشرفته
- HA (High Availability) support
- مستندات جامع و جامعه بزرگ

**معایب**:

- بر پایه FreeBSD (نه Linux)
- نیاز به منابع سخت‌افزاری بیشتر

**لینک مستندات**: [pfSense Documentation](https://docs.netgate.com/pfsense/)

**کاربرد**: مناسب برای محیط‌های enterprise که نیاز به کنترل و مدیریت دقیق دارند.

---

#### ۲. **OPNsense** (جایگزین pfSense)

**توضیح**: Fork از pfSense با UI مدرن‌تر و پشتیبانی بهتر از ابزارهای مدرن.

**مزایا**:

- رابط کاربری مدرن و responsive
- پشتیبانی از WireGuard native
- Plugin system گسترده
- Security features پیشرفته
- Community و commercial support

**معایب**:

- منابع بیشتر نسبت به راهکارهای ساده‌تر
- بر پایه FreeBSD

**لینک مستندات**: [OPNsense Documentation](https://docs.opnsense.org/)

**کاربرد**: جایگزین مدرن‌تر pfSense برای محیط‌های enterprise.

---

#### ۳. **VyOS** (Linux-based Router)

**توضیح**: Router OS بر پایه Debian با CLI-based configuration.

**مزایا**:

- بر پایه Linux (Debian)
- CLI قدرتمند و scriptable
- پشتیبانی از OpenVPN، WireGuard، IPsec
- Policy-based routing
- Lightweight و efficient

**معایب**:

- فقط CLI (بدون Web UI)
- نیاز به دانش بیشتر برای configuration
- مستندات کمتر از pfSense

**لینک مستندات**: [VyOS Documentation](https://docs.vyos.io/)

**کاربرد**: مناسب برای کاربران حرفه‌ای که با CLI راحت هستند.

---

#### ۴. **Rocky Linux 9 با StrongSwan/OpenVPN** (راهکار سفارشی)

**توضیح**: استفاده از Rocky Linux 9 به عنوان VPN Gateway با نصب StrongSwan یا OpenVPN.

**مزایا**:

- استفاده از همان OS (Rocky Linux 9) برای consistency
- کنترل کامل روی configuration
- هزینه صفر (Open Source)
- امکان customization بالا

**معایب**:

- نیاز به configuration دستی بیشتر
- نیاز به دانش فنی بیشتر
- نیاز به setup مانیتورینگ جداگانه

**لینک مستندات**:

- [StrongSwan Documentation](https://docs.strongswan.org/)
- [OpenVPN Documentation](https://openvpn.net/community-resources/)

**کاربرد**: مناسب برای تیم‌هایی که نیاز به کنترل کامل و customization دارند.

---

### ۲.۲. Routing Solutions

#### ۱. **Policy-based Routing با `ip route` و `iptables`**

**توضیح**: استفاده از Linux native tools برای policy-based routing.

**مثال**:

```bash
# ایجاد routing table جدید
echo "200 vpn_routing" >> /etc/iproute2/rt_tables

# Rule برای routing بر اساس destination IP
ip rule add from 192.168.1.0/24 table vpn_routing
ip route add default via <VPN_GATEWAY_IP> dev <VPN_INTERFACE> table vpn_routing
```

**مزایا**:

- Native Linux tools
- Lightweight
- Highly customizable

**معایب**:

- Configuration پیچیده
- نیاز به scripting برای مدیریت

**لینک مستندات**: [Linux IP Route Documentation](https://linux.die.net/man/8/ip-route)

---

#### ۲. **FRR (Free Range Routing)**

**توضیح**: Routing protocol suite برای Linux که شامل OSPF, BGP, PBR و... است.

**مزایا**:

- Routing protocols پیشرفته
- Policy-based routing
- CLI interface
- مناسب برای شبکه‌های پیچیده

**معایب**:

- پیچیدگی بیشتر
- Overkill برای سناریوی ساده

**لینک مستندات**: [FRR Documentation](https://docs.frrouting.org/)

---

#### ۳. **systemd-networkd با routing policies**

**توضیح**: استفاده از systemd-networkd برای مدیریت شبکه و routing.

**مزایا**:

- Integrated با systemd
- Configuration file-based
- مناسب برای Rocky Linux 9

**معایب**:

- محدودیت‌های بیشتر نسبت به ip route
- مستندات کمتر

**لینک مستندات
**: [systemd-networkd Documentation](https://www.freedesktop.org/software/systemd/man/systemd.network.html)

---

### ۲.۳. VPN Client Solutions

#### ۱. **OpenVPN**

**توضیح**: پرکاربردترین VPN solution با پشتیبانی از TUN/TAP.

**مزایا**:

- پرکاربرد و mature
- پشتیبانی گسترده
- SSL/TLS based
- مستندات جامع

**معایب**:

- Performance کمتر از WireGuard
- Configuration پیچیده‌تر

**لینک مستندات**: [OpenVPN Documentation](https://openvpn.net/community-resources/)

---

#### ۲. **WireGuard**

**توضیح**: VPN protocol مدرن و سریع با cryptography مدرن.

**مزایا**:

- Performance بالا
- Configuration ساده
- Modern cryptography
- Lightweight kernel module

**معایب**:

- نسبتاً جدیدتر (اما stable)
- پشتیبانی محدود در برخی VPN providers

**لینک مستندات**: [WireGuard Documentation](https://www.wireguard.com/)

---

#### ۳. **StrongSwan (IPsec)**

**توضیح**: IPsec-based VPN solution با پشتیبانی از IKEv2.

**مزایا**:

- Standard-based (IPsec)
- مناسب برای site-to-site VPN
- پشتیبانی از certificate-based auth

**معایب**:

- Configuration پیچیده‌تر
- Performance کمتر از WireGuard

**لینک مستندات**: [StrongSwan Documentation](https://docs.strongswan.org/)

---

## ۳. مشکلات رایج و راهکارها

### ۳.۱. مشکل: Routing Loop یا ترافیک از VPN Gateway خارج نمی‌شود

**علت**:

- Configuration نادرست routing tables
- Default gateway تنظیم نشده
- Firewall rules مسدود کننده

**راهکار**:

```bash
# بررسی routing table
ip route show
ip route show table vpn_routing

# بررسی default gateway
ip route get 8.8.8.8

# بررسی firewall rules
iptables -L -n -v
iptables -t nat -L -n -v

# Test connectivity
ping -I <VPN_INTERFACE> 8.8.8.8
```

---

### ۳.۲. مشکل: DNS Resolution در VMها کار نمی‌کند

**علت**:

- DNS server از طریق VPN در دسترس نیست
- DNS configuration در VPN Gateway نادرست است

**راهکار**:

```bash
# تنظیم DNS در VPN Gateway
# /etc/resolv.conf
nameserver 1.1.1.1
nameserver 8.8.8.8

# یا استفاده از dnsmasq/unbound برای DNS forwarding
# نصب dnsmasq
dnf install dnsmasq

# تنظیم DNS forwarding
echo "server=1.1.1.1" >> /etc/dnsmasq.conf
echo "server=8.8.8.8" >> /etc/dnsmasq.conf
systemctl enable --now dnsmasq
```

---

### ۳.۳. مشکل: Performance پایین VPN Connection

**علت**:

- VPN server overloaded
- Network congestion
- Encryption overhead
- MTU size نادرست

**راهکار**:

```bash
# تنظیم MTU مناسب
ip link set <VPN_INTERFACE> mtu 1420

# استفاده از WireGuard به جای OpenVPN (سرعت بیشتر)
# بررسی bandwidth
iperf3 -c <VPN_SERVER>

# استفاده از compression در OpenVPN (اگر supported)
comp-lzo adaptive
```

---

### ۳.۴. مشکل: VPN Connection قطع می‌شود (Connection Drops)

**علت**:

- Timeout configuration
- Network instability
- Firewall timeout
- VPN server issues

**راهکار**:

```bash
# تنظیم keepalive در OpenVPN
keepalive 10 60

# استفاده از auto-reconnect
# در systemd service
Restart=always
RestartSec=5

# بررسی logs
journalctl -u openvpn@<config> -f
```

---

### ۳.۵. مشکل: Policy-based Routing کار نمی‌کند

**علت**:

- Routing rules به ترتیب نادرست
- IP ranges در لیست VPN نادرست
- Routing table reference نادرست

**راهکار**:

```bash
# بررسی routing rules
ip rule show

# بررسی routing tables
ip route show table all

# Test routing برای IP خاص
ip route get <DESTINATION_IP>

# استفاده از iptables mark برای policy routing
iptables -t mangle -A OUTPUT -d <VPN_DESTINATION> -j MARK --set-mark 1
ip rule add fwmark 1 table vpn_routing
```

---

### ۳.۶. مشکل: NAT/Masquerading کار نمی‌کند

**علت**:

- iptables NAT rules نادرست
- IP forwarding غیرفعال است

**راهکار**:

```bash
# فعال‌سازی IP forwarding
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p

# تنظیم NAT
iptables -t nat -A POSTROUTING -o <VPN_INTERFACE> -j MASQUERADE
iptables -A FORWARD -i <LAN_INTERFACE> -o <VPN_INTERFACE> -j ACCEPT
iptables -A FORWARD -i <VPN_INTERFACE> -o <LAN_INTERFACE> -m state --state RELATED,ESTABLISHED -j ACCEPT

# ذخیره rules
iptables-save > /etc/iptables/rules.v4
```

---

### ۳.۷. مشکل: Docker Hub و سایر Container Registries از VPN عبور نمی‌کنند

**علت**:

- Docker از DNS خاص استفاده می‌کند
- Docker network configuration جدا از host network است

**راهکار**:

```bash
# تنظیم Docker daemon.json
cat > /etc/docker/daemon.json << EOF
{
  "dns": ["1.1.1.1", "8.8.8.8"],
  "dns-search": ["."]
}
EOF

# Restart Docker
systemctl restart docker

# استفاده از host network mode برای containers (در صورت نیاز)
docker run --network host <image>

# یا تنظیم proxy برای Docker
mkdir -p /etc/systemd/system/docker.service.d
cat > /etc/systemd/system/docker.service.d/http-proxy.conf << EOF
[Service]
Environment="HTTP_PROXY=http://<VPN_GATEWAY_IP>:3128"
Environment="HTTPS_PROXY=http://<VPN_GATEWAY_IP>:3128"
EOF
systemctl daemon-reload
systemctl restart docker
```

---

### ۳.۸. مشکل: Monitoring و Logging ناکافی

**علت**:

- Logging configuration نادرست
- Monitoring tools نصب نشده

**راهکار**:

```bash
# فعال‌سازی verbose logging در OpenVPN
verb 4
log-append /var/log/openvpn.log

# استفاده از vnstat برای monitoring traffic
dnf install vnstat
vnstat -i <VPN_INTERFACE>

# استفاده از Prometheus node_exporter برای metrics
# Integration با Grafana برای visualization
```

---

## ۴. سوالات متداول (Q&A)

### سوال ۱: آیا می‌توان از یک VM به عنوان VPN Gateway استفاده کرد؟

**پاسخ**: بله، اما باید توجه داشت که:

- این VM باید منابع کافی (CPU, RAM, Network) داشته باشد
- باید به عنوان default gateway برای سایر VMها تنظیم شود
- باید High Availability در نظر گرفته شود (در صورت نیاز)

**پیشنهاد**: استفاده از pfSense یا OPNsense VM که به صورت اختصاصی برای این کار طراحی شده‌اند.

---

### سوال ۲: آیا می‌توان چند VPN connection همزمان استفاده کرد؟

**پاسخ**: بله، با استفاده از policy-based routing می‌توان:

- چند VPN connection ایجاد کرد
- هر VPN را برای destination خاص استفاده کرد
- Load balancing بین VPNها انجام داد (در صورت نیاز)

**مثال**:

```bash
# VPN 1 برای Docker Hub
ip rule add to 54.230.0.0/16 table vpn1_routing

# VPN 2 برای GitHub
ip rule add to 140.82.0.0/16 table vpn2_routing
```

---

### سوال ۳: آیا می‌توان فقط ترافیک خاص را از VPN عبور داد و بقیه مستقیم به اینترنت برود؟

**پاسخ**: بله، این دقیقاً همان policy-based routing است:

- لیست IP ranges برای VPN را تعریف می‌کنید
- فقط ترافیک matching با این لیست از VPN عبور می‌کند
- بقیه ترافیک از default gateway (اینترنت مستقیم) عبور می‌کند

**مزیت**: صرفه‌جویی در bandwidth و هزینه VPN

---

### سوال ۴: چگونه می‌توان VPN Gateway را High Available کرد؟

**پاسخ**: چند راهکار:

1. **VRRP (Virtual Router Redundancy Protocol)**: استفاده از keepalived برای failover
2. **VMware HA**: استفاده از VMware High Availability برای VM failover
3. **Dual VPN Gateway**: دو VM با configuration یکسان و VRRP

**مثال با keepalived**:

```bash
# نصب keepalived
dnf install keepalived

# Configuration
# /etc/keepalived/keepalived.conf
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1
    virtual_ipaddress {
        192.168.1.1
    }
}
```

---

### سوال ۵: آیا می‌توان از Cloud VPN Services استفاده کرد؟

**پاسخ**: بله، می‌توان از سرویس‌های VPN تجاری مانند:

- **NordVPN**, **ExpressVPN**, **Surfshark** (با OpenVPN/WireGuard config)
- **AWS VPN**, **Azure VPN Gateway** (برای enterprise)
- **Private VPN Servers** (VPS-based)

**ملاحظات**:

- بررسی Terms of Service
- بررسی Logging policies
- بررسی Performance و Reliability

---

### سوال ۶: چگونه می‌توان Docker containers را به VPN Gateway متصل کرد؟

**پاسخ**: چند روش:

1. **Host Network Mode**: استفاده از `--network host` (ساده اما کمتر امن)
2. **Bridge Network با NAT**: تنظیم default gateway container به VPN Gateway
3. **Docker Proxy**: استفاده از HTTP proxy که از VPN عبور می‌کند

**مثال**:

```bash
# روش 1: Host network
docker run --network host nginx

# روش 2: Bridge network
docker network create --gateway 192.168.100.1 --subnet 192.168.100.0/24 vpn_network
docker run --network vpn_network --dns 192.168.100.1 nginx
```

---

### سوال ۷: آیا می‌توان VPN Gateway را در Docker container اجرا کرد؟

**پاسخ**: بله، اما:

- نیاز به `--cap-add=NET_ADMIN` و `--privileged` دارد
- نیاز به `--network host` یا custom network
- پیچیدگی بیشتر در configuration

**پیشنهاد**: استفاده از VM اختصاصی برای VPN Gateway (ساده‌تر و امن‌تر)

---

### سوال ۸: چگونه می‌توان performance VPN را monitor کرد?

**پاسخ**: استفاده از:

1. **vnstat**: Traffic statistics
2. **iftop**: Real-time bandwidth monitoring
3. **Prometheus + Grafana**: Comprehensive monitoring
4. **VPN connection logs**: بررسی connection status

**مثال**:

```bash
# نصب vnstat
dnf install vnstat
vnstat -i <VPN_INTERFACE>

# نصب iftop
dnf install iftop
iftop -i <VPN_INTERFACE>
```

---

## ۵. مراحل پیاده‌سازی پیشنهادی

### مرحله ۱: آماده‌سازی VPN Gateway VM

1. ایجاد VM جدید با Rocky Linux 9 (یا pfSense/OPNsense)
2. تخصیص منابع کافی (2+ CPU, 2GB+ RAM)
3. تنظیم network interfaces (LAN + WAN)
4. نصب و update سیستم

---

### مرحله ۲: نصب و Configuration VPN Client

1. نصب OpenVPN/WireGuard/StrongSwan
2. Import VPN configuration files
3. تنظیم VPN connections
4. تست اتصال VPN

---

### مرحله ۳: تنظیم Policy-based Routing

1. ایجاد routing tables
2. تعریف routing rules بر اساس destination IP
3. تنظیم NAT/Masquerading
4. تست routing

---

### مرحله ۴: تنظیم سایر VMها

1. تغییر default gateway به VPN Gateway IP
2. تنظیم DNS servers
3. تست connectivity
4. تست دسترسی به Docker Hub و سایر سرویس‌ها

---

### مرحله ۵: Monitoring و Maintenance

1. نصب monitoring tools
2. تنظیم logging
3. ایجاد backup از configurations
4. مستندسازی procedures

---

## ۶. لیست IP Ranges پیشنهادی برای VPN

### Docker Hub و Container Registries

```
# Docker Hub
54.230.0.0/16
52.84.0.0/15

# GitHub
140.82.0.0/16
185.199.0.0/16

# Google Container Registry
108.177.0.0/17

# Amazon ECR
52.0.0.0/15
```

### سایر سرویس‌های متداول

```
# npm registry
104.16.0.0/13

# PyPI
151.101.0.0/16

# Maven Central
151.101.0.0/16
```

**نکته**: این لیست باید بر اساس نیازهای پروژه به‌روزرسانی شود.

---

## ۷. منابع و مراجع

### مستندات رسمی

| ابزار              | توضیح                        | لینک Documentation                                               |
|--------------------|------------------------------|------------------------------------------------------------------|
| **pfSense**        | Firewall/Router Distribution | [pfSense Docs](https://docs.netgate.com/pfsense/)                |
| **OPNsense**       | Modern Firewall/Router       | [OPNsense Docs](https://docs.opnsense.org/)                      |
| **VyOS**           | Linux-based Router OS        | [VyOS Docs](https://docs.vyos.io/)                               |
| **OpenVPN**        | VPN Solution                 | [OpenVPN Docs](https://openvpn.net/community-resources/)         |
| **WireGuard**      | Modern VPN Protocol          | [WireGuard Docs](https://www.wireguard.com/)                     |
| **StrongSwan**     | IPsec VPN Solution           | [StrongSwan Docs](https://docs.strongswan.org/)                  |
| **Linux IP Route** | Policy-based Routing         | [IP Route Man Page](https://linux.die.net/man/8/ip-route)        |
| **FRR**            | Routing Protocol Suite       | [FRR Docs](https://docs.frrouting.org/)                          |
| **keepalived**     | VRRP Implementation          | [keepalived Docs](https://www.keepalived.org/documentation.html) |

### راهنماها و Tutorials

| موضوع                         | لینک                                                                                   |
|-------------------------------|----------------------------------------------------------------------------------------|
| Policy-based Routing در Linux | [Linux Advanced Routing](https://lartc.org/howto/)                                     |
| OpenVPN Setup Guide           | [OpenVPN Howto](https://openvpn.net/community-resources/how-to/)                       |
| WireGuard Setup Guide         | [WireGuard Quick Start](https://www.wireguard.com/quickstart/)                         |
| pfSense VPN Guide             | [pfSense VPN Documentation](https://docs.netgate.com/pfsense/en/latest/vpn/index.html) |

### Community Resources

| منبع           | لینک                                                      |
|----------------|-----------------------------------------------------------|
| pfSense Forum  | [pfSense Forum](https://forum.netgate.com/)               |
| OPNsense Forum | [OPNsense Forum](https://forum.opnsense.org/)             |
| r/VPN          | [Reddit VPN Community](https://www.reddit.com/r/VPN/)     |
| r/networking   | [Reddit Networking](https://www.reddit.com/r/networking/) |

---

## ۸. خلاصه و توصیه‌ها

### توصیه نهایی

**برای محیط Enterprise**: استفاده از **pfSense** یا **OPNsense** به دلیل:

- Web UI ساده و قدرتمند
- Policy-based routing built-in
- Monitoring و Logging پیشرفته
- Community support قوی
- Documentation جامع

**برای تیم‌های حرفه‌ای**: استفاده از **Rocky Linux 9 + StrongSwan/WireGuard** به دلیل:

- کنترل کامل
- Consistency با سایر VMها
- Cost-effective
- Highly customizable

**برای شروع سریع**: استفاده از **pfSense VM** با OpenVPN/WireGuard client configuration.

---

<div align="center">

[↑ بازگشت به بالا](#vpn-gateway-و-routing-هوشمند-برای-زیرساخت) | [← بازگشت به صفحه اصلی](Home) | [زیرساخت](Infrastructure-Setup)

</div>

