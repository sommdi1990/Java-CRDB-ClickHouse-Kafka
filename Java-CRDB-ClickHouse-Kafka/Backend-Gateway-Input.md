# Gateway Input

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

Gateway برای مدیریت سرویس‌های ورودی و Webhookها از سیستم‌های خارجی.

## مسئولیت‌ها

### 1. Webhook Management

- دریافت webhookها از external services
- Validation و verification
- Event routing

### 2. External Service Integration

- Integration با سرویس‌های خارجی
- API client management
- Error handling و retry

### 3. Event Processing

- Process incoming events
- Transform events
- Route to appropriate services

### 4. Security

- Webhook signature verification
- IP whitelisting
- Rate limiting

## تکنولوژی‌ها

- **Spring Cloud Gateway**: Gateway framework
- **Spring WebFlux**: Reactive programming
- **Kafka**: Event streaming
- **Webhook Signature Verification**: Security

## Webhook Endpoints

### Payment Gateway

- `POST /api/webhooks/payment/success` - Payment success
- `POST /api/webhooks/payment/failure` - Payment failure
- `POST /api/webhooks/payment/refund` - Refund notification

### Email Service

- `POST /api/webhooks/email/delivered` - Email delivered
- `POST /api/webhooks/email/bounced` - Email bounced
- `POST /api/webhooks/email/opened` - Email opened

### SMS Service

- `POST /api/webhooks/sms/delivered` - SMS delivered
- `POST /api/webhooks/sms/failed` - SMS failed

## Webhook Signature Verification

```java
public boolean verifySignature(String payload, String signature, String secret) {
    String expectedSignature = hmacSha256(payload, secret);
    return MessageDigest.isEqual(
        expectedSignature.getBytes(),
        signature.getBytes()
    );
}
```

## Event Processing

```java
@PostMapping("/webhooks/{provider}")
public ResponseEntity<Void> handleWebhook(
    @PathVariable String provider,
    @RequestBody String payload,
    @RequestHeader("X-Signature") String signature
) {
    // Verify signature
    if (!verifySignature(payload, signature, getSecret(provider))) {
        return ResponseEntity.status(401).build();
    }
    
    // Process event
    WebhookEvent event = parseEvent(payload);
    kafkaTemplate.send("webhook-events", event);
    
    return ResponseEntity.ok().build();
}
```

## Error Handling

- **Retry Logic**: برای failed webhooks
- **Dead Letter Queue**: برای unprocessable events
- **Alerting**: برای critical failures

## Security

- **Signature Verification**: برای webhook authenticity
- **IP Whitelisting**: برای trusted sources
- **Rate Limiting**: جلوگیری از abuse

## Monitoring

- **Webhook Delivery**: tracking delivery status
- **Error Rates**: monitoring errors
- **Processing Time**: performance metrics

## لینک‌های مفید

- [Spring Cloud Gateway Documentation](https://spring.io/projects/spring-cloud-gateway)
- [Spring WebFlux Documentation](https://docs.spring.io/spring-framework/reference/web/webflux.html)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Webhook Security Best Practices](https://webhooks.fyi/best-practices/security)
- [HMAC Signature Verification](https://en.wikipedia.org/wiki/HMAC)
- [Dead Letter Queue Pattern](https://www.enterpriseintegrationpatterns.com/patterns/messaging/DeadLetterChannel.html)

---

<div align="center">

[↑ بازگشت به بالا](#gateway-input) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

