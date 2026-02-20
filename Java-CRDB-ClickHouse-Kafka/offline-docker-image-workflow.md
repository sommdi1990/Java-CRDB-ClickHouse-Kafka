# راهنمای آفلاین مدیریت ایمیج‌های Docker با رجیستری ایران

این راهنما برای شرایطی نوشته شده که **سرور ایران دسترسی مستقیم و پایدار به Docker Hub ندارد**  
و شما از یک **سرور واسط (مثلاً هلند)** برای دریافت ایمیج‌ها استفاده می‌کنید.

---

## سناریوی کلی

1. پیدا کردن ایمیج مناسب در وب
2. Pull ایمیج روی سرور هلند
3. Tag کردن ایمیج برای رجیستری ایران
4. Push ایمیج به رجیستری ایران
5. اطمینان از وجود ایمیج در رجیستری ایران
6. پاکسازی کامل سرور هلند (به‌دلیل محدودیت فضا)

---

## 1️⃣ پیدا کردن ایمیج در وب

### سایت‌های معتبر برای پیدا کردن ایمیج

#### 🔹 Docker Hub (پیشنهادی)

🌐 https://hub.docker.com

مراحل:

1. وارد سایت شو
2. اسم سرویس مورد نظر رو جستجو کن (مثلاً: `docker-registry-ui`)
3. روی نتیجه رسمی یا محبوب کلیک کن
4. این موارد رو بررسی کن:
    - تعداد Pull
    - آخرین Update
    - بخش **Tags**
    - توضیحات (Overview)

📌 مثال:

```
joxit/docker-registry-ui
```

و Tag:

```
2.0.0
```

---

## 2️⃣ Pull ایمیج روی سرور هلند

روی سرور هلند که اینترنت آزاد داره:

```bash
docker pull joxit/docker-registry-ui:2.0.0
```

بررسی ایمیج:

```bash
docker images | grep docker-registry-ui
```

---

## 3️⃣ Tag کردن ایمیج برای رجیستری ایران

فرمت استاندارد:

```
<registry-domain>/<image-name>:<tag>
```

مثال:

```bash
docker tag joxit/docker-registry-ui:2.0.0 reg.alefba2.ir/joxit/docker-registry-ui:2.0.0
```

---

## 4️⃣ Push ایمیج به رجیستری ایران

### لاگین (در صورت داشتن Auth):

```bash
docker login reg.alefba2.ir
```

### Push:

```bash
docker push reg.alefba2.ir/joxit/docker-registry-ui:2.0.0
```

📌 اگر رجیستری بدون Auth است، مرحله login نیاز نیست.

---

## 5️⃣ اطمینان از وجود ایمیج در رجیستری ایران

### روش 1: API رجیستری (پیشنهادی)

```bash
curl http://reg.alefba2.ir/v2/_catalog
```

بررسی Tag:

```bash
curl http://reg.alefba2.ir/v2/joxit/docker-registry-ui/tags/list
```

### روش 2: Docker Registry UI

- باز کردن UI رجیستری در مرورگر
- دیدن Repository و Tag

### روش 3: Pull تست روی سرور ایران

```bash
nerdctl pull reg.alefba2.ir/joxit/docker-registry-ui:2.0.0
```

اگر Pull شد ✅ یعنی ایمیج سالمه

---

## 6️⃣ پاکسازی کامل سرور هلند (خیلی مهم)

### حذف کانتینرهای متوقف‌شده

```bash
docker container prune -f
```

### حذف ایمیج خاص

```bash
docker rmi joxit/docker-registry-ui:2.0.0
docker rmi reg.alefba2.ir/joxit/docker-registry-ui:2.0.0
```

### حذف تمام ایمیج‌های بدون استفاده

```bash
docker image prune -a -f
```

### بررسی فضای آزاد

```bash
df -h
docker system df
```

---

## 🧠 نکات حرفه‌ای

- همیشه **versioned tag** استفاده کن (از latest دوری کن)
- رجیستری ایران رو **Single Source of Truth** بدون
- Pull مستقیم روی ایران = ❌
- هلند فقط نقش **Bridge** داره، نه انبار

---

## 📦 الگوی آماده برای هر ایمیج

```text
Docker Hub Image: <name>
Version: <tag>

docker pull <name>:<tag>
docker tag <name>:<tag> reg.alefba2.ir/<name>:<tag>
docker push reg.alefba2.ir/<name>:<tag>
```

---

✍️ تهیه شده برای استفاده عملی در محیط‌های با محدودیت اینترنت
