# ClickHouse Manager Service

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

مدیریت و جستجوی لاگ‌ها و آمارها در ClickHouse.

## مسئولیت‌ها

### 1. Log Management

- جستجوی لاگ‌ها
- فیلتر کردن لاگ‌ها
- Export لاگ‌ها

### 2. Analytics

- تحلیل آمارها
- Aggregation queries
- Time-series analysis

### 3. Data Ingestion

- مدیریت ingestion از Redis buffer
- Batch processing
- Error handling

## استراتژی Insert

### مهم: هیچ سیستمی مستقیماً به ClickHouse نمی‌نویسد

```
Application Services
    ↓
Redis Buffer (Logs & Metrics)
    ↓
ClickHouse Manager (Every 15 minutes)
    ↓
ClickHouse Database
```

### Batch Processing

```java
@Scheduled(fixedDelay = 900000) // 15 minutes
public void processBuffer() {
    List<LogEntry> logs = redisBufferService.getPendingLogs();
    if (!logs.isEmpty()) {
        clickHouseRepository.batchInsert(logs);
        redisBufferService.clearProcessedLogs();
    }
}
```

## API Endpoints

### Log Search

- `GET /api/clickhouse/logs/search` - جستجوی لاگ‌ها
- `GET /api/clickhouse/logs/{id}` - دریافت لاگ خاص
- `POST /api/clickhouse/logs/export` - Export لاگ‌ها

### Analytics

- `GET /api/clickhouse/analytics/summary` - خلاصه آمارها
- `GET /api/clickhouse/analytics/time-series` - Time-series data
- `GET /api/clickhouse/analytics/aggregations` - Aggregations

## Query Examples

### Log Search

```sql
SELECT *
FROM logs
WHERE timestamp >= '2024-01-01'
  AND level = 'ERROR'
  AND service = 'order-service'
ORDER BY timestamp DESC
LIMIT 100
```

### Analytics

```sql
SELECT
    toStartOfHour(timestamp) as hour,
    service,
    count(*) as count,
    avg(response_time) as avg_response_time
FROM logs
WHERE timestamp >= now() - INTERVAL 24 HOUR
GROUP BY hour, service
ORDER BY hour DESC
```

## Performance Optimization

### Indexing

- **Primary Key**: timestamp, service
- **Secondary Indexes**: level, user_id
- **Materialized Views**: برای pre-aggregation

### Partitioning

- **By Date**: partitioning بر اساس تاریخ
- **TTL**: حذف داده‌های قدیمی

## Integration

- **Redis**: برای buffer
- **Grafana**: برای visualization
- **Prometheus**: برای metrics

## لینک‌های مفید

- [ClickHouse Documentation](https://clickhouse.com/docs)
- [ClickHouse SQL Reference](https://clickhouse.com/docs/en/sql-reference/)
- [ClickHouse Performance Tuning](https://clickhouse.com/docs/en/guides/improving-query-performance/)
- [ClickHouse Best Practices](https://clickhouse.com/docs/en/guides/best-practices/)
- [Grafana ClickHouse Integration](https://grafana.com/docs/grafana/latest/datasources/clickhouse/)
- [Redis Documentation](https://redis.io/docs/)
- [Spring Scheduler Documentation](https://docs.spring.io/spring-framework/reference/integration/scheduling.html)

---

<div align="center">

[↑ بازگشت به بالا](#clickhouse-manager-service) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

