# مدیریت کاربران

<div align="right">

[← بازگشت به Security](Security-Home) | [← صفحه اصلی](Security-Home)

</div>

---

## هدف

مدیریت کاربران و پروفایل‌ها در سیستم.

## قابلیت‌ها

### 1. User CRUD

- ایجاد کاربر
- ویرایش کاربر
- حذف کاربر
- مشاهده لیست کاربران

### 2. Profile Management

- ویرایش پروفایل
- تغییر رمز عبور
- آپلود تصویر پروفایل
- تنظیمات شخصی

### 3. User Roles

- تخصیص نقش
- مدیریت نقش‌ها
- سلسله مراتب نقش‌ها

### 4. User Status

- فعال/غیرفعال کردن کاربر
- Lock/Unlock account
- Expiration management

## Integration با Keycloak

### User Synchronization

```java
@Service
public class UserService {
    public void createUser(CreateUserCommand command) {
        // Create in Keycloak
        keycloakService.createUser(command);
        
        // Create in local database
        User user = new User(command);
        userRepository.save(user);
    }
}
```

## API Endpoints

- `GET /api/users` - لیست کاربران
- `POST /api/users` - ایجاد کاربر
- `GET /api/users/{id}` - دریافت کاربر
- `PUT /api/users/{id}` - به‌روزرسانی کاربر
- `DELETE /api/users/{id}` - حذف کاربر
- `POST /api/users/{id}/roles` - تخصیص نقش

## Security

- **Password Policy**: قوانین رمز عبور
- **Account Lockout**: قفل کردن account بعد از تلاش‌های ناموفق
- **Password Expiration**: انقضای رمز عبور

## لینک‌های مفید

- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [Keycloak User Management](https://www.keycloak.org/docs/latest/server_admin/#_user-management)
- [Spring Security Documentation](https://spring.io/projects/spring-security)
- [Password Policy Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Account Lockout Strategies](https://owasp.org/www-community/controls/Account_Lockout)

---

<div align="center">

[↑ بازگشت به بالا](#مدیریت-کاربران) | [← بازگشت به Security](Security-Home) | [← صفحه اصلی](Security-Home)

</div>

