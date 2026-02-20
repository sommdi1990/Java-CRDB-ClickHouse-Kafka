# Schedule & Event Manager Service

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

مدیریت Scheduleها و Eventها با استفاده از تقویم برای اجرای خودکار تسک‌ها. همچنین پیاده‌سازی یک سیستم تقویم پیشرفته شبیه
Google Calendar با پشتیبانی از تقویم شمسی و میلادی برای ثبت و مدیریت رویدادها و اطلاع‌رسانی به کاربران.

## قابلیت‌ها

### 1. Job Scheduling

- Scheduled jobs
- Cron expressions
- Recurring tasks
- One-time tasks

### 2. Calendar Management (Google Calendar-like System)

- **پشتیبانی از تقویم‌های مختلف**:
    - تقویم شمسی (Persian/Jalali Calendar)
    - تقویم میلادی (Gregorian Calendar)
    - تبدیل خودکار بین تقویم‌ها
    - نمایش همزمان هر دو تقویم

- **تقویم‌های اشتراکی**:
    - تقویم شخصی (Personal Calendar)
    - تقویم گروهی (Group Calendar)
    - تقویم سازمانی (Organization Calendar)
    - اشتراک‌گذاری تقویم با کاربران دیگر
    - مدیریت دسترسی (خواندن/نوشتن)

- **تعطیلات و رویدادهای خاص**:
    - تعطیلات رسمی ایران (شمسی)
    - تعطیلات بین‌المللی (میلادی)
    - رویدادهای سازمانی
    - Business days
    - رویدادهای قابل تنظیم

### 3. Event Management (Google Calendar-like)

- **ایجاد و مدیریت رویدادها**:
    - ایجاد، ویرایش و حذف رویدادها
    - رویدادهای تک‌باره (One-time events)
    - رویدادهای تکراری (Recurring events)
    - رویدادهای تمام‌روزه (All-day events)
    - رویدادهای با زمان مشخص (Timed events)
    - رویدادهای چندروزه (Multi-day events)
    - رنگ‌بندی رویدادها
    - دسته‌بندی رویدادها (Categories/Tags)
    - مکان رویداد (Location)
    - توضیحات و یادداشت‌ها
    - ضمیمه‌ها (Attachments)

- **اطلاع‌رسانی و یادآوری**:
    - اطلاع‌رسانی به کاربران برای رویدادها
    - یادآوری‌های چندگانه (Multiple reminders)
    - یادآوری از طریق Email
    - یادآوری از طریق SMS
    - Push Notifications
    - In-app Notifications
    - یادآوری‌های قابل تنظیم (قبل از رویداد)

- **نمایش و جستجو**:
    - نمایش تقویم به صورت روزانه، هفتگی، ماهانه
    - جستجوی رویدادها
    - فیلتر رویدادها بر اساس نوع، تاریخ، کاربر

- **همگام‌سازی**:
    - Export به iCal format
    - Import از iCal format
    - همگام‌سازی با Google Calendar (در صورت نیاز)
    - همگام‌سازی با Outlook Calendar (در صورت نیاز)

### 4. Task Execution

- اجرای خودکار tasks
- Retry mechanism
- Error handling
- Job history

## تکنولوژی‌ها

- **Quartz Scheduler**: برای job scheduling
- **Spring Scheduler**: برای simple scheduling
- **Persian Calendar Libraries**:
    - `time4j` یا `persian-calendar` برای مدیریت تقویم شمسی
    - تبدیل بین تقویم شمسی و میلادی
- **REST API**: برای Frontend integration
- **WebSocket**: برای Real-time updates
- **Integration با Messaging Service**: برای اطلاع‌رسانی

## Job Scheduling

### Quartz Configuration

```java
@Configuration
public class QuartzConfig {
    @Bean
    public JobDetail documentArchiveJob() {
        return JobBuilder.newJob(DocumentArchiveJob.class)
            .withIdentity("documentArchiveJob")
            .storeDurably()
            .build();
    }
    
    @Bean
    public Trigger documentArchiveTrigger() {
        return TriggerBuilder.newTrigger()
            .forJob(documentArchiveJob())
            .withIdentity("documentArchiveTrigger")
            .withSchedule(CronScheduleBuilder.cronSchedule("0 0 2 * * ?")) // Daily at 2 AM
            .build();
    }
}
```

### Spring Scheduler

```java
@Component
public class ScheduledTasks {
    @Scheduled(cron = "0 0 0 * * ?") // Daily at midnight
    public void dailyReport() {
        // Generate daily report
    }
    
    @Scheduled(fixedDelay = 900000) // Every 15 minutes
    public void processBuffer() {
        // Process Redis buffer to ClickHouse
    }
}
```

## Calendar Management

### Persian Calendar Support

```java
@Service
public class CalendarService {
    public boolean isBusinessDay(LocalDate date) {
        // Check if date is business day
        // Consider weekends and holidays
    }
    
    public LocalDate getNextBusinessDay(LocalDate date) {
        // Get next business day
    }
    
    // Convert between Persian and Gregorian calendars
    public PersianDate toPersianDate(LocalDate gregorianDate) {
        // Convert Gregorian to Persian
    }
    
    public LocalDate toGregorianDate(PersianDate persianDate) {
        // Convert Persian to Gregorian
    }
    
    public List<Holiday> getHolidays(int year, CalendarType type) {
        // Get holidays for a specific year and calendar type
    }
}
```

### Calendar Sharing

```java
@Entity
public class Calendar {
    @Id
    private UUID id;
    private String name;
    private CalendarType type; // PERSONAL, GROUP, ORGANIZATION
    private String ownerId;
    private List<CalendarShare> shares; // Users with access
    private CalendarColor color;
}

@Entity
public class CalendarShare {
    @Id
    private UUID id;
    private UUID calendarId;
    private String userId;
    private Permission permission; // READ, WRITE
}
```

## Event Management

### Event Entity

```java
@Entity
public class Event {
    @Id
    private UUID id;
    private String title;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private String description;
    private EventType type; // ONE_TIME, RECURRING, ALL_DAY
    private RecurrenceRule recurrenceRule; // For recurring events
    private String location;
    private EventColor color;
    private List<String> categories;
    private List<String> tags;
    private UUID calendarId;
    private String organizerId;
    private List<String> attendeeIds;
    private EventStatus status; // CONFIRMED, TENTATIVE, CANCELLED
    private List<Reminder> reminders;
    private List<Attachment> attachments;
    private boolean isAllDay;
    private String timezone;
}

@Entity
public class RecurrenceRule {
    private RecurrenceFrequency frequency; // DAILY, WEEKLY, MONTHLY, YEARLY
    private int interval;
    private LocalDate until;
    private int count;
    private List<DayOfWeek> byDay;
    private List<Integer> byMonthDay;
    private List<Integer> byMonth;
}

@Entity
public class Reminder {
    @Id
    private UUID id;
    private UUID eventId;
    private ReminderType type; // EMAIL, SMS, PUSH, IN_APP
    private Duration beforeEvent; // How long before event
    private boolean isSent;
    private LocalDateTime sentAt;
}
```

### Event Notifications

```java
@Service
public class EventNotificationService {
    
    @Autowired
    private MessagingService messagingService;
    
    public void sendEventReminder(Event event, Reminder reminder) {
        // Send reminder based on type
        switch (reminder.getType()) {
            case EMAIL:
                messagingService.sendEmail(/* ... */);
                break;
            case SMS:
                messagingService.sendSMS(/* ... */);
                break;
            case PUSH:
                messagingService.sendPushNotification(/* ... */);
                break;
            case IN_APP:
                messagingService.sendInAppNotification(/* ... */);
                break;
        }
    }
    
    public void notifyEventCreated(Event event) {
        // Notify attendees about new event
        for (String attendeeId : event.getAttendeeIds()) {
            messagingService.sendInAppNotification(attendeeId, 
                "New event: " + event.getTitle());
        }
    }
    
    public void notifyEventUpdated(Event event) {
        // Notify attendees about event update
    }
    
    public void notifyEventCancelled(Event event) {
        // Notify attendees about event cancellation
    }
}
```

### Reminders

- **Email Reminders**: ارسال ایمیل از طریق Messaging Service
- **SMS Reminders**: ارسال SMS از طریق Messaging Service
- **Push Notifications**: Push notifications از طریق Messaging Service
- **In-app Notifications**: In-app notifications از طریق Messaging Service
- **Multiple Reminders**: امکان تنظیم چندین یادآوری برای یک رویداد
- **Customizable Timing**: تنظیم زمان یادآوری (قبل از رویداد)

## API Endpoints

### Scheduling

- `POST /api/schedule/jobs` - ایجاد job جدید
- `GET /api/schedule/jobs` - لیست jobs
- `PUT /api/schedule/jobs/{id}` - به‌روزرسانی job
- `DELETE /api/schedule/jobs/{id}` - حذف job
- `POST /api/schedule/jobs/{id}/trigger` - Trigger job manually

### Events

- `POST /api/events` - ایجاد event جدید
- `GET /api/events` - لیست events
- `GET /api/events/{id}` - دریافت event
- `PUT /api/events/{id}` - به‌روزرسانی event
- `DELETE /api/events/{id}` - حذف event

### Calendar

- `GET /api/calendar/business-days` - لیست business days
- `GET /api/calendar/holidays` - لیست تعطیلات
- `GET /api/calendar/events` - Events در بازه زمانی
- `GET /api/calendars` - لیست تقویم‌های کاربر
- `POST /api/calendars` - ایجاد تقویم جدید
- `PUT /api/calendars/{id}` - به‌روزرسانی تقویم
- `DELETE /api/calendars/{id}` - حذف تقویم
- `POST /api/calendars/{id}/share` - اشتراک‌گذاری تقویم
- `GET /api/calendars/{id}/events` - رویدادهای یک تقویم
- `GET /api/calendar/view` - نمایش تقویم (روزانه/هفتگی/ماهانه)
- `GET /api/calendar/search` - جستجوی رویدادها
- `POST /api/calendar/export/ical` - Export به iCal format
- `POST /api/calendar/import/ical` - Import از iCal format

## Integration

- **Messaging Service**:
    - برای ارسال Email، SMS و Notifications
    - اطلاع‌رسانی رویدادها به کاربران
    - یادآوری‌های رویدادها
- **WorkFlow Service**:
    - برای workflow execution
    - رویدادهای مرتبط با workflow
- **Report Manager**:
    - برای scheduled reports
    - گزارشات تقویمی
- **Document Archive Service**:
    - برای ضمیمه‌های رویدادها
    - ذخیره فایل‌های مرتبط با رویدادها

## لینک‌های مفید

### Scheduling & Job Management

- [Quartz Scheduler Documentation](https://www.quartz-scheduler.org/documentation/)
- [Quartz Tutorial](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/)
- [Spring Scheduler Documentation](https://docs.spring.io/spring-framework/reference/integration/scheduling.html)
- [Cron Expression Guide](https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html)
- [Cron Expression Generator](https://www.freeformatter.com/cron-expression-generator-quartz.html)

### Calendar & Date Libraries

- [Persian Calendar Libraries - starcal](https://github.com/ilius/starcal)
- [Persian Calendar - time4j](https://github.com/MenoData/Time4J)
- [Persian Calendar - persian-calendar](https://github.com/omid/Persian-Calendar)
- [Joda-Time Documentation](https://www.joda.org/joda-time/)
- [Java 8 Date/Time API](https://docs.oracle.com/javase/8/docs/api/java/time/package-summary.html)

### Calendar Standards & Formats

- [iCal Specification](https://icalendar.org/)
- [RFC 5545 - iCalendar](https://datatracker.ietf.org/doc/html/rfc5545)
- [RFC 7986 - iCalendar Extensions](https://datatracker.ietf.org/doc/html/rfc7986)
- [CalDAV Protocol](https://datatracker.ietf.org/doc/html/rfc4791)

### Calendar APIs & Integration

- [Google Calendar API](https://developers.google.com/calendar/api)
- [Google Calendar API Java Client](https://developers.google.com/api-client-library/java/apis/calendar/v3)
- [Microsoft Graph Calendar API](https://learn.microsoft.com/en-us/graph/api/resources/calendar)
- [Outlook Calendar API](https://learn.microsoft.com/en-us/outlook/rest/calendar-rest)

### Calendar UI Components

- [FullCalendar - JavaScript Calendar](https://fullcalendar.io/)
- [React Big Calendar](https://github.com/jquense/react-big-calendar)
- [React Calendar](https://github.com/wojtekmaj/react-calendar)
- [Material-UI Date Picker](https://mui.com/x/react-date-pickers/)

### Event Management

- [Event Sourcing Pattern](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

### Notification & Reminders

- [Spring Mail Documentation](https://docs.spring.io/spring-framework/reference/integration/email.html)
- [Push Notifications Guide](https://web.dev/push-notifications-overview/)
- [Web Notifications API](https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API)

---

<div align="center">

[↑ بازگشت به بالا](#schedule--event-manager-service) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

