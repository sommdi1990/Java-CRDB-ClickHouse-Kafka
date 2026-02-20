# Prometheus

<div align="right">

[← بازگشت به Monitoring](Monitoring-Home) | [← صفحه اصلی](Monitoring-Home)

</div>

---

## هدف

Collection و storage metrics برای monitoring.

## قابلیت‌ها

### 1. Metrics Collection

- Pull-based metrics
- Push-based metrics
- Service discovery
- Scraping configuration

### 2. Storage

- Time-series database
- Data retention
- Compression
- Query language (PromQL)

### 3. Alerting

- Alert rules
- Alert manager
- Notification routing

## Setup

### Spring Boot Integration

```yaml
management:
  endpoints:
    web:
      exposure:
        include: prometheus
  metrics:
    export:
      prometheus:
        enabled: true
```

### Prometheus Configuration

```yaml
scrape_configs:
  - job_name: 'spring-boot-app'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['localhost:8080']
```

## Metrics

### JVM Metrics

- Memory usage
- GC metrics
- Thread metrics
- Class loading

### HTTP Metrics

- Request count
- Response time
- Error rate
- Status codes

### Custom Metrics

```java
@RestController
public class OrderController {
    private final Counter orderCounter;
    
    public OrderController(MeterRegistry registry) {
        this.orderCounter = Counter.builder("orders.total")
            .description("Total number of orders")
            .register(registry);
    }
    
    @PostMapping("/orders")
    public Order createOrder() {
        orderCounter.increment();
        // ...
    }
}
```

## PromQL Queries

### Rate Calculation

```promql
rate(http_requests_total[5m])
```

### Aggregation

```promql
sum(rate(http_requests_total[5m])) by (service)
```

## Best Practices

1. **Metric Naming**: نام‌گذاری استاندارد
2. **Label Cardinality**: مدیریت label cardinality
3. **Retention**: تنظیم retention
4. **Scraping Interval**: تنظیم interval

## لینک‌های مفید

- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Prometheus Getting Started](https://prometheus.io/docs/prometheus/latest/getting_started/)
- [PromQL Query Language](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Micrometer Documentation](https://micrometer.io/docs)
- [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)

---

<div align="center">

[↑ بازگشت به بالا](#prometheus) | [← بازگشت به Monitoring](Monitoring-Home) | [← صفحه اصلی](Monitoring-Home)

</div>

