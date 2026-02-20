# CockroachDB

<div align="right">

[← بازگشت به Database](Database-Home) | [← صفحه اصلی](Database-Home)

</div>

---

## نقش

دیتابیس اصلی سیستم که همه ماژول‌ها به صورت یکپارچه از آن استفاده می‌کنند.

## ویژگی‌ها

- Distributed SQL database
- ACID compliance
- Horizontal scalability
- PostgreSQL compatibility
- Multi-region support

## ساختار

- هر ماژول schema مخصوص به خود را دارد
- Shared tables برای داده‌های مشترک
- Foreign keys برای integrity

## Connection Pooling

- استفاده از HikariCP
- Configuration در application.yml

## Backup & Recovery

- Automated backups
- Point-in-time recovery
- Replication strategy

## Monitoring

- CockroachDB Admin UI
- Integration با Prometheus
- Query performance monitoring

## لینک‌های مفید

- [CockroachDB Documentation](https://www.cockroachlabs.com/docs/)
- [CockroachDB University](https://university.cockroachlabs.com/)
- [CockroachDB Architecture](https://www.cockroachlabs.com/docs/stable/architecture/overview.html)
- [PostgreSQL Compatibility](https://www.cockroachlabs.com/docs/stable/postgresql-compatibility.html)
- [HikariCP Documentation](https://github.com/brettwooldridge/HikariCP)
- [Database Design Best Practices](https://www.cockroachlabs.com/docs/stable/performance-best-practices-overview.html)

---

<div align="center">

[↑ بازگشت به بالا](#cockroachdb) | [← بازگشت به Database](Database-Home) | [← صفحه اصلی](Database-Home)

</div>

