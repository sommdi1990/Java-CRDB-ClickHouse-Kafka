# Messaging Service

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

ارسال پیام‌ها از طریق SMS، Email و Notification با قابلیت template management و delivery tracking.

## قابلیت‌ها

### 1. SMS

- ارسال پیامک از طریق gatewayهای مختلف
- پشتیبانی از چندین provider
- Delivery status tracking
- Retry mechanism

### 2. Email

- ارسال ایمیل با template management
- HTML و Plain text support
- Attachment support
- Bulk email sending
- Email queue management

### 3. Notification

- **Push Notifications**: FCM, OneSignal, APNS
- **In-app Notifications**: Real-time notifications در application
- **Web Notifications**: Browser push notifications
- Notification preferences

## تکنولوژی‌ها

### SMS

- **Twilio**: Cloud-based SMS service
- **Kavenegar**: سرویس ایرانی
- **SMS Gateway**: Generic gateway interface

### Email

- **Spring Mail**: برای ارسال email
- **JavaMailSender**: SMTP integration
- **SendGrid** یا **Mailgun**: Cloud-based email service

### Notifications

- **Firebase Cloud Messaging (FCM)**: برای Android و Web
- **Apple Push Notification Service (APNS)**: برای iOS
- **OneSignal**: Multi-platform push notifications
- **WebSocket**: برای in-app notifications

### Queue Management

- **Apache Kafka / Redpanda**: برای message queue (توصیه: Redpanda برای performance بهتر)
- **RabbitMQ**: جایگزین Kafka
- **Redis Queue**: برای lightweight queues
- برای مقایسه Kafka و Redpanda، به [مقایسه تفصیلی Redpanda و Kafka](Kafka-Redpanda-Comparison) مراجعه کنید

## ساختار Service

```
messaging-service/
├── sms/
│   ├── provider/
│   ├── template/
│   └── delivery/
├── email/
│   ├── provider/
│   ├── template/
│   └── delivery/
└── notification/
    ├── push/
    ├── in-app/
    └── preferences/
```

## Template Management

### SMS Templates

```java
@Template(name = "welcome-sms")
public class WelcomeSmsTemplate {
    private String userName;
    private String activationCode;
}
```

### Email Templates

- استفاده از **Thymeleaf** یا **Freemarker**
- HTML templates
- Variable substitution
- Multi-language support

## API Endpoints

### SMS

- `POST /api/messaging/sms/send` - ارسال SMS
- `GET /api/messaging/sms/status/{id}` - بررسی وضعیت

### Email

- `POST /api/messaging/email/send` - ارسال Email
- `POST /api/messaging/email/bulk` - ارسال Bulk Email
- `GET /api/messaging/email/status/{id}` - بررسی وضعیت

### Notification

- `POST /api/messaging/notification/push` - ارسال Push Notification
- `POST /api/messaging/notification/in-app` - ارسال In-app Notification
- `GET /api/messaging/notification/preferences` - تنظیمات Notification

## Delivery Tracking

- Tracking delivery status
- Retry failed messages
- Delivery reports
- Analytics و statistics

## Configuration

```yaml
messaging:
  sms:
    provider: twilio
    twilio:
      account-sid: ${TWILIO_ACCOUNT_SID}
      auth-token: ${TWILIO_AUTH_TOKEN}
  email:
    provider: smtp
    smtp:
      host: smtp.gmail.com
      port: 587
      username: ${EMAIL_USERNAME}
      password: ${EMAIL_PASSWORD}
  notification:
    fcm:
      server-key: ${FCM_SERVER_KEY}
```

## Integration با سایر سرویس‌ها

- Integration با WorkFlow Service (برای workflow notifications)
- Integration با Document Archive Service (برای email attachments)
- Integration با eSignature Service (برای email notifications)

## لینک‌های مفید

- [Spring Mail Documentation](https://docs.spring.io/spring-framework/reference/integration/email.html)
- [Twilio Documentation](https://www.twilio.com/docs)
- [Twilio SMS API](https://www.twilio.com/docs/sms)
- [SendGrid Documentation](https://docs.sendgrid.com/)
- [Mailgun Documentation](https://documentation.mailgun.com/)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
- [OneSignal Documentation](https://documentation.onesignal.com/)
- [Apple Push Notification Service](https://developer.apple.com/documentation/usernotifications)
- [Thymeleaf Documentation](https://www.thymeleaf.org/documentation.html)
- [Freemarker Documentation](https://freemarker.apache.org/docs/)

---

<div align="center">

[↑ بازگشت به بالا](#messaging-service) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

