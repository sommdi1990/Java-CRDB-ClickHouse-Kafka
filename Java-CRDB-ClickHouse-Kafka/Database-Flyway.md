# Flyway - Database Migration

<div align="right">

[← بازگشت به Database](Database-Home) | [← صفحه اصلی](Database-Home)

</div>

---

## نقش

Flyway ابزار مدیریت migration دیتابیس است که برای مدیریت تغییرات schema و داده‌های دیتابیس در تمام محیط‌های توسعه، تست و
production استفاده می‌شود.

## ویژگی‌ها

- Version control برای database schema
- Migration scripts با versioning
- Automatic migration execution
- Rollback support (با Flyway Pro)
- Multiple database support (CockroachDB, PostgreSQL, MySQL, etc.)
- Integration با Spring Boot

## استراتژی Migration

### 1. Versioned Migrations

Migration scripts با نام‌گذاری versioned:

```
V{version}__{description}.sql
```

مثال:

- `V1__Create_users_table.sql`
- `V2__Add_email_to_users.sql`
- `V3__Create_orders_table.sql`

### 2. Repeatable Migrations

برای تغییرات قابل تکرار (مثل views, functions):

```
R__{description}.sql
```

مثال:

- `R__Create_user_view.sql`
- `R__Update_statistics_function.sql`

### 3. Undo Migrations (Flyway Pro)

برای rollback تغییرات (نیاز به Flyway Pro):

```
U{version}__{description}.sql
```

## ساختار پروژه

```
src/main/resources/db/migration/
├── V1__Initial_schema.sql
├── V2__Create_users_table.sql
├── V3__Create_orders_table.sql
├── V4__Add_indexes.sql
├── R__Create_views.sql
└── R__Create_functions.sql
```

## پیکربندی Spring Boot

### application.yml

```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
    baseline-version: 0
    validate-on-migrate: true
    clean-disabled: true  # برای production
    out-of-order: false   # برای production
    placeholders:
      schema_name: ${spring.flyway.schemas}
```

### پیکربندی برای CockroachDB

```yaml
spring:
  flyway:
    enabled: true
    schemas: public,accounting,workflow,infrastructure
    locations: classpath:db/migration
    baseline-on-migrate: true
    validate-on-migrate: true
    clean-disabled: true
    out-of-order: false
    sql-migration-prefix: V
    sql-migration-separator: __
    sql-migration-suffixes: .sql
    repeatable-sql-migration-prefix: R
    repeatable-sql-migration-separator: __
    repeatable-sql-migration-suffixes: .sql
```

## Best Practices

### 1. Naming Convention

- استفاده از version numbers واضح
- استفاده از underscores در نام فایل‌ها
- استفاده از نام‌های توصیفی

### 2. Migration Scripts

- هر migration باید idempotent باشد (در صورت امکان)
- استفاده از IF NOT EXISTS برای tables
- استفاده از transactions (CockroachDB از transactions پشتیبانی می‌کند)
- تست migration scripts قبل از commit

### 3. Schema Changes

- تغییرات schema باید backward compatible باشند (در صورت امکان)
- استفاده از feature flags برای gradual rollout
- Migration scripts باید قابل rollback باشند

### 4. Data Migrations

- جدا کردن schema migrations از data migrations
- استفاده از separate migration scripts برای data migrations
- Backup قبل از data migrations

### 5. Multiple Databases

برای پروژه‌های multi-database:

```yaml
spring:
  flyway:
    enabled: true
    locations: 
      - classpath:db/migration/cockroachdb
      - classpath:db/migration/clickhouse
```

## Integration با CockroachDB

### ویژگی‌های خاص CockroachDB

- پشتیبانی کامل از PostgreSQL syntax
- استفاده از transactions برای atomic migrations
- پشتیبانی از multiple schemas
- استفاده از UUID برای primary keys

### مثال Migration Script

```sql
-- V1__Create_users_table.sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
```

## Integration با ClickHouse

### نکات مهم

- ClickHouse از transactions پشتیبانی نمی‌کند
- Migration scripts باید با دقت نوشته شوند
- استفاده از IF NOT EXISTS برای tables
- استفاده از ON CLUSTER برای distributed tables

### مثال Migration Script

```sql
-- V1__Create_logs_table.sql
CREATE TABLE IF NOT EXISTS logs
(
    id UUID,
    timestamp DateTime,
    level String,
    message String,
    service String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, service)
TTL timestamp + INTERVAL 90 DAY;
```

## Migration Lifecycle

### Development

1. ایجاد migration script جدید
2. تست local migration
3. Commit به Git
4. Review و merge

### Staging

1. Automatic migration در deployment
2. Validation و testing
3. بررسی migration history

### Production

1. Backup database
2. Review migration scripts
3. Deploy با migration
4. Monitor migration execution
5. Verify schema changes

## Flyway Commands

### Command Line

```bash
# Migrate database
flyway migrate

# Validate migrations
flyway validate

# Info about migrations
flyway info

# Clean database (development only)
flyway clean

# Baseline existing database
flyway baseline

# Repair migration history
flyway repair
```

### Spring Boot Integration

Flyway به صورت خودکار در Spring Boot اجرا می‌شود:

- در startup، Flyway migrations را اجرا می‌کند
- اگر migration جدیدی وجود داشته باشد، آن را اجرا می‌کند
- اگر migration fail شود، application startup fail می‌شود

## Migration History Table

Flyway یک جدول `flyway_schema_history` ایجاد می‌کند که شامل:

- `installed_rank`: ترتیب نصب
- `version`: version migration
- `description`: توضیحات migration
- `type`: نوع migration (SQL, JDBC, etc.)
- `script`: نام فایل script
- `checksum`: checksum فایل
- `installed_on`: زمان نصب
- `execution_time`: زمان اجرا
- `success`: موفقیت یا عدم موفقیت

## Troubleshooting

### مشکل: Migration failed

**راه‌حل:**

1. بررسی error message
2. بررسی migration script
3. Repair migration history (در صورت نیاز)
4. Manual fix و baseline

### مشکل: Out of order migrations

**راه‌حل:**

- استفاده از `out-of-order: true` در development
- استفاده از `out-of-order: false` در production
- بررسی migration history

### مشکل: Checksum mismatch

**راه‌حل:**

- بررسی تغییرات در migration script
- استفاده از `flyway repair` برای update checksum
- یا manual update در `flyway_schema_history`

## Security Considerations

- Migration scripts نباید شامل sensitive data باشند
- استفاده از placeholders برای configuration
- استفاده از environment variables برای secrets
- محدود کردن دسترسی به migration scripts

## Monitoring

- بررسی `flyway_schema_history` برای migration status
- Integration با Spring Boot Actuator
- Alerting برای failed migrations
- Logging migration execution

## لینک‌های مفید

- [Flyway Documentation](https://flywaydb.org/documentation/)
- [Flyway Spring Boot Integration](https://flywaydb.org/documentation/usage/plugins/springboot)
- [Flyway Best Practices](https://flywaydb.org/documentation/concepts/migrations)
- [CockroachDB Migration Guide](https://www.cockroachlabs.com/docs/stable/migrate-from-postgres.html)
- [ClickHouse Migration Guide](https://clickhouse.com/docs/en/guides/migrating-data/)

---

<div align="center">

[↑ بازگشت به بالا](#flyway---database-migration) | [← بازگشت به Database](Database-Home) | [← صفحه اصلی](Database-Home)

</div>

