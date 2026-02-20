# Redis

<div align="right">

[← بازگشت به Database](Database-Home) | [← صفحه اصلی](Database-Home)

</div>

---

## نقش

- Cache management
- Session storage
- Temporary data storage
- Buffer برای ClickHouse

## استفاده‌ها

### 1. Caching

- API response caching
- Database query caching
- Session caching

### 2. Buffer برای ClickHouse

- لاگ‌ها و آمارها در Redis ذخیره می‌شوند
- هر 15 دقیقه یکبار به ClickHouse منتقل می‌شوند
- استفاده از Redis Streams یا List structure

### 3. Session Management

- User sessions
- Temporary tokens
- Rate limiting counters

## Configuration

- Redis Cluster برای high availability
- Redis Sentinel برای failover
- TTL management

## Monitoring

- Redis Insight
- Integration با Prometheus
- Memory usage monitoring

## لینک‌های مفید

- [Redis Documentation](https://redis.io/docs/)
- [Redis University](https://university.redis.com/)
- [Redis Commands](https://redis.io/commands/)
- [Redis Data Types](https://redis.io/docs/manual/data-types/)
- [Redis Streams](https://redis.io/docs/manual/data-types/streams/)
- [Redis Sentinel](https://redis.io/docs/manual/sentinel/)
- [Redis Cluster](https://redis.io/docs/manual/scaling/)
- [Redis Insight](https://redis.io/insight/)

---

<div align="center">

[↑ بازگشت به بالا](#redis) | [← بازگشت به Database](Database-Home) | [← صفحه اصلی](Database-Home)

</div>

