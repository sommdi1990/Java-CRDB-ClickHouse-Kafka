# Apache Cassandra چیست و به چه دردی می‌خورد؟

## Cassandra به زبان ساده

**Apache Cassandra** یک دیتابیس **NoSQL توزیع‌شده (Distributed)** از نوع **Wide-Column Store** است که برای:

- حجم دیتای بسیار زیاد (Big Data)
- نوشتن‌های بسیار زیاد (High Write Throughput)
- دسترس‌پذیری بالا (High Availability)
- بدون Single Point of Failure

طراحی شده است.

Cassandra اول در **Facebook** ساخته شد و بعداً به پروژه Apache منتقل شد.

---

## Cassandra چه مشکلی را حل می‌کند؟

Cassandra عالی است وقتی که:

- دیتای خیلی زیاد داری (ترابایت / پتابایت)
- درخواست‌ها زیاد و همزمان هستند
- قطع شدن حتی یک نود نباید کل سیستم را بخواباند
- Consistency صددرصد لحظه‌ای برایت حیاتی نیست

نمونه کاربردها:

- لاگ‌ها و Eventها
- پیام‌رسان‌ها
- IoT و سنسورها
- Activity Feed (مثل اینستاگرام، توییتر)
- Time-Series Data

---

## مدل دیتای Cassandra

Cassandra شبیه SQL فکر نمی‌کند ❌  
بیشتر **Query-Based Design** است.

### ساختار:

- Keyspace (مثل Database)
- Table
- Partition Key (خیلی مهم)
- Clustering Key

📌 **اول Query را طراحی می‌کنی، بعد جدول را**

---

## Cassandra شبیه کدام دیتابیس‌هاست؟

بیشترین شباهت را دارد به:

- **HBase**
- **ScyllaDB**
- **DynamoDB (از نظر فلسفه)**

ولی شبیه این‌ها نیست:

- PostgreSQL ❌
- MySQL ❌
- MongoDB (نسبتاً) ❌

---

# مقایسه Cassandra با CockroachDB و ClickHouse

## 1️⃣ Cassandra vs CockroachDB

| ویژگی       | Cassandra             | CockroachDB        |
|-------------|-----------------------|--------------------|
| نوع         | NoSQL                 | NewSQL             |
| مدل داده    | Wide-Column           | Relational (SQL)   |
| Consistency | Eventually Consistent | Strong Consistency |
| Transaction | ❌ ندارد               | ✅ کامل             |
| SQL         | ❌                     | ✅                  |
| Scale Out   | عالی                  | عالی               |
| Use Case    | Write-heavy, Big Data | OLTP توزیع‌شده     |

### جمع‌بندی:

- اگر **بانکی / مالی / تراکنشی** → CockroachDB
- اگر **لاگ، Event، IoT** → Cassandra

---

## 2️⃣ Cassandra vs ClickHouse

| ویژگی               | Cassandra         | ClickHouse    |
|---------------------|-------------------|---------------|
| نوع                 | NoSQL             | Columnar OLAP |
| هدف                 | Write + Read سریع | Analytics     |
| Query پیچیده        | ❌ ضعیف            | ✅ بسیار قوی   |
| Aggregation         | ❌                 | ✅ عالی        |
| Real-time Analytics | ❌                 | ✅             |
| Storage             | Row/Wide Column   | Column-based  |

### جمع‌بندی:

- Cassandra = **Operational Data**
- ClickHouse = **تحلیل داده (Analytics)**

---

## چه زمانی Cassandra انتخاب بدی است؟

❌ وقتی:

- JOIN زیاد داری
- Queryهای ad-hoc می‌خواهی
- Transaction مهم است
- SQL دوست داری 😄

---

## چه زمانی Cassandra انتخاب عالی است؟

✅ وقتی:

- دیتای بسیار زیاد
- Write بسیار زیاد
- معماری Microservice
- Geo-Distributed System

---

## مقایسه نهایی خیلی خلاصه

| دیتابیس     | بهترین کاربرد                 |
|-------------|-------------------------------|
| Cassandra   | Big Data + High Write         |
| CockroachDB | Distributed SQL + Transaction |
| ClickHouse  | Analytics + BI                |

---

## جمله طلایی 😎

> Cassandra برای **تحلیل داده نیست**  
> Cassandra برای **زنده نگه داشتن سیستم تحت فشار شدید است**

---
