# ClickHouse

<div align="right">

[← بازگشت به Database](Database-Home) | [← صفحه اصلی](Database-Home)

</div>

---

## نقش

دیتابیس تحلیلی برای لاگ‌ها و آمارها که همه ماژول‌ها به صورت یکپارچه از آن استفاده می‌کنند.

## ویژگی‌ها

- Columnar database
- High performance analytical queries
- Excellent compression
- Real-time data ingestion

## استراتژی Insert

- **هیچ سیستمی مستقیماً به ClickHouse نمی‌نویسد**
- همه لاگ‌ها و آمارها ابتدا در Redis buffer می‌شوند
- هر 15 دقیقه یکبار، داده‌ها از Redis به ClickHouse منتقل می‌شوند

## ساختار Tables

- Partitioning بر اساس تاریخ
- TTL برای مدیریت داده‌های قدیمی
- Materialized views برای aggregation

## Query Optimization

- Indexing strategy
- Pre-aggregation
- Query caching

## Monitoring

- ClickHouse Admin UI
- Integration با Grafana
- Query performance monitoring

## لینک‌های مفید

- [ClickHouse Documentation](https://clickhouse.com/docs)
- [ClickHouse Tutorial](https://clickhouse.com/docs/en/getting-started/tutorial/)
- [ClickHouse Best Practices](https://clickhouse.com/docs/en/guides/best-practices/)
- [ClickHouse Performance Tuning](https://clickhouse.com/docs/en/guides/improving-query-performance/)
- [Grafana ClickHouse Integration](https://grafana.com/docs/grafana/latest/datasources/clickhouse/)
- [ClickHouse Admin UI](https://github.com/ClickHouse/ClickHouse/tree/master/programs/server)

---

<div align="center">

[↑ بازگشت به بالا](#clickhouse) | [← بازگشت به Database](Database-Home) | [← صفحه اصلی](Database-Home)

</div>

