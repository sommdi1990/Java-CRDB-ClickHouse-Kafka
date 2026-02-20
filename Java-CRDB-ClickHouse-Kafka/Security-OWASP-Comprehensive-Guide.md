# راهنمای جامع استانداردهای امنیتی OWASP

<div align="right">

[← بازگشت به Security](Security-Home) | [← صفحه اصلی](Home)

</div>

---

## فهرست مطالب

1. [معرفی OWASP](#معرفی-owasp)
2. [OWASP Top 10 (2021)](#owasp-top-10-2021)
3. [OWASP API Security Top 10](#owasp-api-security-top-10)
4. [OWASP Application Security Verification Standard (ASVS)](#owasp-application-security-verification-standard-asvs)
5. [OWASP Dependency Check](#owasp-dependency-check)
6. [OWASP ZAP (Zed Attack Proxy)](#owasp-zap-zed-attack-proxy)
7. [پیاده‌سازی عملی در پروژه](#پیادهسازی-عملی-در-پروژه)
8. [چک‌لیست امنیتی](#چکلیست-امنیتی)
9. [رفرنس‌ها و منابع](#رفرنسها-و-منابع)

---

## معرفی OWASP

**OWASP (Open Web Application Security Project)** یک سازمان غیرانتفاعی است که به بهبود امنیت نرم‌افزار اختصاص دارد.
OWASP استانداردها، ابزارها، مستندات و بهترین روش‌های امنیتی را برای توسعه نرم‌افزارهای امن ارائه می‌دهد.

### چرا OWASP مهم است؟

1. **استاندارد صنعتی**: OWASP به عنوان استاندارد صنعتی برای امنیت نرم‌افزار شناخته می‌شود
2. **رایگان و Open Source**: تمام منابع OWASP رایگان و در دسترس هستند
3. **جامعه بزرگ**: جامعه بزرگی از متخصصان امنیت از آن پشتیبانی می‌کنند
4. **به‌روزرسانی مداوم**: استانداردها به صورت منظم به‌روزرسانی می‌شوند
5. **قابل اجرا**: راهنمایی‌های عملی و قابل اجرا ارائه می‌دهد

### پروژه‌های اصلی OWASP

- **OWASP Top 10**: لیست 10 آسیب‌پذیری رایج در وب اپلیکیشن‌ها
- **OWASP API Security Top 10**: آسیب‌پذیری‌های رایج در APIها
- **OWASP ASVS**: استاندارد تایید امنیت اپلیکیشن
- **OWASP Dependency Check**: ابزار اسکن وابستگی‌ها
- **OWASP ZAP**: ابزار تست نفوذ خودکار
- **OWASP Cheat Sheet Series**: مجموعه cheat sheetهای امنیتی

### وب‌سایت رسمی

- **وب‌سایت اصلی**: https://owasp.org/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **OWASP API Security**: https://owasp.org/www-project-api-security/
- **OWASP ASVS**: https://owasp.org/www-project-application-security-verification-standard/
- **OWASP Dependency Check**: https://owasp.org/www-project-dependency-check/
- **OWASP ZAP**: https://www.zaproxy.org/

---

## OWASP Top 10 (2021)

OWASP Top 10 لیست 10 آسیب‌پذیری رایج و خطرناک در وب اپلیکیشن‌ها است که هر 3-4 سال به‌روزرسانی می‌شود. آخرین نسخه در سال
2021 منتشر شده است.

### A01:2021 – Broken Access Control

**تعریف**: نقض کنترل دسترسی زمانی رخ می‌دهد که کاربران بتوانند به منابع یا عملکردهایی دسترسی پیدا کنند که نباید داشته
باشند.

#### مثال‌های رایج:

1. **Vertical Privilege Escalation**: کاربر عادی به نقش مدیر دسترسی پیدا می‌کند
2. **Horizontal Privilege Escalation**: کاربر A به داده‌های کاربر B دسترسی پیدا می‌کند
3. **Missing Authorization**: عدم بررسی مجوز قبل از دسترسی به منابع
4. **Insecure Direct Object References (IDOR)**: دسترسی مستقیم به منابع با تغییر ID

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- استفاده از **Role-Based Access Control (RBAC)** و **Attribute-Based Access Control (ABAC)**
- بررسی مجوز در هر endpoint و قبل از هر عملیات
- استفاده از **Spring Security Method Security** برای کنترل دسترسی در سطح متد
- پیاده‌سازی **Resource-Based Authorization** برای بررسی مالکیت منابع
- استفاده از **Keycloak** برای مدیریت نقش‌ها و دسترسی‌ها
- لاگ کردن تمام تلاش‌های دسترسی غیرمجاز
- استفاده از **Principle of Least Privilege** (حداقل دسترسی لازم)

```java
// مثال: استفاده از Spring Security Method Security
@PreAuthorize("hasRole('ADMIN')")
@GetMapping("/admin/users")
public List<User> getAllUsers() {
    return userService.findAll();
}

@PreAuthorize("hasRole('USER') and #userId == authentication.principal.id")
@GetMapping("/users/{userId}")
public User getUser(@PathVariable Long userId) {
    return userService.findById(userId);
}

// بررسی مالکیت منبع
@PreAuthorize("@resourceAuthorizationService.isOwner(#resourceId, authentication.principal.id)")
@DeleteMapping("/resources/{resourceId}")
public void deleteResource(@PathVariable Long resourceId) {
    resourceService.delete(resourceId);
}

// بررسی دسترسی در Service Layer
@Service
public class UserService {
    public User getUserById(Long userId, String currentUsername) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException(userId));

        // بررسی دسترسی: کاربر فقط می‌تواند اطلاعات خودش را ببیند
        if (!user.getUsername().equals(currentUsername) &&
                !hasAdminRole(currentUsername)) {
            throw new AccessDeniedException("You don't have access to this user");
        }

        return user;
    }
}

// Logging و Audit Trail
@Aspect
@Component
public class AccessControlAspect {
    private static final Logger logger = LoggerFactory.getLogger(AccessControlAspect.class);

    @Around("@annotation(RequiresPermission)")
    public Object logAccess(ProceedingJoinPoint joinPoint) throws Throwable {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        String method = joinPoint.getSignature().getName();

        logger.info("Access attempt: user={}, method={}", username, method);

        try {
            Object result = joinPoint.proceed();
            logger.info("Access granted: user={}, method={}", username, method);
            return result;
        } catch (AccessDeniedException e) {
            logger.warn("Access denied: user={}, method={}", username, method);
            throw e;
        }
    }
}
```

❌ **نباید انجام شود:**

- اعتماد به کنترل دسترسی فقط در frontend
- استفاده از IDهای قابل پیش‌بینی (sequential IDs)
- عدم بررسی مجوز در backend
- افشای اطلاعات حساس در error messages
- استفاده از role-based checks بدون بررسی ownership

```java
// ❌ اشتباه: فقط Frontend بررسی می‌کند
// Frontend: if (user.role === 'ADMIN') { showAdminPanel(); }

// ✅ درست: بررسی در Backend
@PreAuthorize("hasRole('ADMIN')")
@GetMapping("/admin/panel")
public AdminPanel getAdminPanel() { ...}

// ❌ اشتباه: ID قابل پیش‌بینی
@GetMapping("/api/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow();
}

// ✅ درست: استفاده از UUID یا بررسی دسترسی
@GetMapping("/api/users/{uuid}")
public User getUser(@PathVariable UUID uuid, Authentication auth) {
    User user = userRepository.findByUuid(uuid).orElseThrow();
    if (!user.getUsername().equals(auth.getName()) && !hasAdminRole(auth)) {
        throw new AccessDeniedException();
    }
    return user;
}
```

#### ابزارهای تست

- **OWASP ZAP**: تست خودکار آسیب‌پذیری‌های کنترل دسترسی
- **Burp Suite**: تست دستی کنترل دسترسی
- **Postman/Newman**: تست API endpoints با نقش‌های مختلف

---

### A02:2021 – Cryptographic Failures

**تعریف**: آسیب‌پذیری‌های مرتبط با رمزنگاری که قبلاً "Sensitive Data Exposure" نامیده می‌شد.

#### مثال‌های رایج:

1. **Weak Encryption Algorithms**: استفاده از الگوریتم‌های رمزنگاری ضعیف (MD5, SHA1, DES)
2. **Insufficient Key Management**: مدیریت ضعیف کلیدهای رمزنگاری
3. **Plaintext Storage**: ذخیره داده‌های حساس به صورت plaintext
4. **Weak TLS Configuration**: پیکربندی ضعیف TLS/SSL
5. **Missing Encryption**: عدم رمزنگاری داده‌های حساس در transit یا at rest

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- استفاده از الگوریتم‌های رمزنگاری قوی:
    - **Hashing**: SHA-256, SHA-512, bcrypt, Argon2
    - **Encryption**: AES-256-GCM, ChaCha20-Poly1305
    - **TLS**: TLS 1.2+ (ترجیحاً TLS 1.3)
- استفاده از **Keycloak** برای مدیریت کلیدها و tokens
- رمزنگاری داده‌های حساس در database (Encryption at Rest)
- استفاده از HTTPS برای تمام ارتباطات (Encryption in Transit)
- استفاده از **Spring Security Crypto** برای رمزنگاری
- پیاده‌سازی **Key Rotation** برای کلیدهای رمزنگاری
- استفاده از **HashiCorp Vault** یا **AWS KMS** برای مدیریت کلیدها

```java
// ✅ استفاده از BCrypt برای hash کردن پسوردها
@Service
public class PasswordEncoderService {
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder(12);

    public String encode(String rawPassword) {
        return passwordEncoder.encode(rawPassword);
    }

    public boolean matches(String rawPassword, String encodedPassword) {
        return passwordEncoder.matches(rawPassword, encodedPassword);
    }
}

// رمزگذاری داده‌های حساس در Database
@Entity
public class User {
    @Id
    private Long id;

    @Column(nullable = false)
    private String username;

    // ✅ رمزگذاری فیلدهای حساس
    @Convert(converter = EncryptedStringConverter.class)
    @Column(name = "email")
    private String email;

    @Convert(converter = EncryptedStringConverter.class)
    @Column(name = "phone_number")
    private String phoneNumber;
}

@Converter
public class EncryptedStringConverter implements AttributeConverter<String, String> {
    private final AESUtil aesUtil = new AESUtil();

    @Override
    public String convertToDatabaseColumn(String attribute) {
        return aesUtil.encrypt(attribute);
    }

    @Override
    public String convertToEntityAttribute(String dbData) {
        return aesUtil.decrypt(dbData);
    }
}

// استفاده از TLS 1.3 برای انتقال
// application.yml
server:
ssl:
enabled:true
protocol:TLS
enabled-protocols:TLSv1.3
key-store:classpath:keystore.p12
key-store-password:

$ {
    KEYSTORE_PASSWORD
}

key-store-type:PKCS12

// مدیریت امن کلیدها
@Configuration

public class EncryptionConfig {
    // ✅ استفاده از Environment Variables یا Secret Management
    @Value("${encryption.key}")
    private String encryptionKey;

    @Bean
    public AESUtil aesUtil() {
        // استفاده از Key Management Service (KMS) در production
        return new AESUtil(encryptionKey);
    }
}

// استفاده از Secure Random
@Service
public class TokenGeneratorService {
    private final SecureRandom secureRandom = new SecureRandom();

    public String generateSecureToken() {
        byte[] bytes = new byte[32];
        secureRandom.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
}
```

❌ **نباید انجام شود:**

- استفاده از MD5, SHA1, DES, RC4
- ذخیره passwordها به صورت plaintext
- استفاده از HTTP برای ارتباطات حساس
- Hardcode کردن کلیدهای رمزنگاری در کد
- استفاده از الگوریتم‌های رمزنگاری ضعیف
- افشای کلیدهای رمزنگاری در logs یا error messages

```java
// ❌ اشتباه: استفاده از MD5
MessageDigest md = MessageDigest.getInstance("MD5");

// ❌ اشتباه: استفاده از SHA-1
MessageDigest md = MessageDigest.getInstance("SHA-1");

// ✅ درست: استفاده از SHA-256 یا BCrypt
MessageDigest md = MessageDigest.getInstance("SHA-256");

// ❌ اشتباه: ذخیره پسوردها به صورت plaintext
user.

setPassword(password); // بدون hash

// ✅ درست
user.

setPassword(passwordEncoder.encode(password));

// ❌ اشتباه: Hardcode کردن کلیدهای رمزنگاری
private static final String ENCRYPTION_KEY = "my-secret-key-123";

// ✅ درست: استفاده از Environment Variables یا Secret Management
@Value("${encryption.key}")
private String encryptionKey;
```

#### ابزارهای تست

- **OWASP Dependency Check**: بررسی استفاده از کتابخانه‌های آسیب‌پذیر
- **SSL Labs SSL Test**: تست پیکربندی SSL/TLS
- **Nmap**: اسکن پورت‌ها و پروتکل‌ها

---

### A03:2021 – Injection

**تعریف**: آسیب‌پذیری‌های تزریق زمانی رخ می‌دهد که داده‌های غیرقابل اعتماد به عنوان بخشی از یک command یا query ارسال
شوند.

#### انواع Injection:

1. **SQL Injection**: تزریق کد SQL در queryهای دیتابیس
2. **NoSQL Injection**: تزریق در دیتابیس‌های NoSQL
3. **Command Injection**: تزریق دستورات سیستم عامل
4. **LDAP Injection**: تزریق در queryهای LDAP
5. **XPath Injection**: تزریق در queryهای XPath
6. **Code Injection**: تزریق کد در runtime

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- استفاده از **Prepared Statements** و **Parameterized Queries**
- استفاده از **ORM** (JPA/Hibernate) برای دسترسی به دیتابیس
- **Input Validation**: اعتبارسنجی و sanitization تمام inputها
- استفاده از **Whitelist** به جای Blacklist
- استفاده از **Spring Data JPA** برای جلوگیری از SQL Injection
- **Output Encoding**: encode کردن output برای جلوگیری از XSS
- استفاده از **ESAPI** یا **OWASP Java Encoder** برای encoding

```java
// ✅ درست: استفاده از Parameterized Query
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    @Query("SELECT u FROM User u WHERE u.email = :email")
    User findByEmail(@Param("email") String email);
}

// ✅ درست: استفاده از JDBC Template
@Repository
public class UserDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    public User findByUsername(String username) {
        String sql = "SELECT * FROM users WHERE username = ?";
        return jdbcTemplate.queryForObject(sql, new Object[]{username}, userRowMapper);
    }
}

// ✅ درست: Input Validation
@RestController
@Validated
public class UserController {
    @PostMapping("/api/users")
    public ResponseEntity<User> createUser(@Valid @RequestBody CreateUserRequest request) {
        // Spring Validation به صورت خودکار اعتبارسنجی می‌کند
        User user = userService.createUser(request);
        return ResponseEntity.ok(user);
    }
}

public class CreateUserRequest {
    @NotBlank(message = "Username is required")
    @Size(min = 3, max = 50, message = "Username must be between 3 and 50 characters")
    @Pattern(regexp = "^[a-zA-Z0-9_]+$", message = "Username can only contain letters, numbers, and underscores")
    private String username;

    @NotBlank(message = "Email is required")
    @Email(message = "Email must be valid")
    private String email;
}

// استفاده از Whitelist برای Input
@Service
public class InputSanitizationService {
    private static final Pattern SAFE_STRING_PATTERN = Pattern.compile("^[a-zA-Z0-9_\\s-]+$");

    public String sanitizeString(String input) {
        if (input == null) {
            return null;
        }

        // حذف کاراکترهای خطرناک
        String sanitized = input.replaceAll("[<>\"'%;()&+]", "");

        // بررسی با whitelist
        if (!SAFE_STRING_PATTERN.matcher(sanitized).matches()) {
            throw new IllegalArgumentException("Invalid input format");
        }

        return sanitized.trim();
    }
}

// Escaping Output
@Service
public class OutputEncodingService {
    public String escapeHtml(String input) {
        if (input == null) {
            return null;
        }
        return StringEscapeUtils.escapeHtml4(input);
    }

    public String escapeJavaScript(String input) {
        if (input == null) {
            return null;
        }
        return StringEscapeUtils.escapeEcmaScript(input);
    }
}
```

❌ **نباید انجام شود:**

- استفاده از String concatenation برای ساخت queryها
- اعتماد به input validation فقط در frontend
- استفاده از `eval()` یا `execute()` با input کاربر
- استفاده از Blacklist برای validation
- افشای اطلاعات دیتابیس در error messages

```java
// ❌ اشتباه: SQL Injection vulnerability
String sql = "SELECT * FROM users WHERE username = '" + username + "'";

// ✅ درست: استفاده از Parameterized Query
String sql = "SELECT * FROM users WHERE username = ?";

// ❌ اشتباه: Command Injection
Runtime.

getRuntime().

exec("ping "+userInput);

// ✅ درست: استفاده از ProcessBuilder با whitelist
ProcessBuilder pb = new ProcessBuilder("ping", "-c", "1", sanitizedHost);
```

#### ابزارهای تست

- **OWASP ZAP**: تست خودکار SQL Injection
- **SQLMap**: تست تخصصی SQL Injection
- **Burp Suite**: تست دستی Injection
- **SonarQube**: تحلیل استاتیک کد

---

### A04:2021 – Insecure Design

**تعریف**: آسیب‌پذیری‌های طراحی که به دلیل عدم توجه به امنیت در مرحله طراحی ایجاد می‌شوند.

#### مثال‌های رایج:

1. **Missing Security Controls**: عدم وجود کنترل‌های امنیتی در طراحی
2. **Weak Authentication**: طراحی ضعیف سیستم احراز هویت
3. **Insecure Defaults**: تنظیمات پیش‌فرض ناامن
4. **Missing Threat Modeling**: عدم انجام Threat Modeling
5. **Insecure Architecture**: معماری ناامن

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- انجام **Threat Modeling** در مرحله طراحی
- استفاده از **Security by Design** principles
- پیاده‌سازی **Defense in Depth** (چند لایه امنیتی)
- استفاده از **Secure Defaults** (تنظیمات پیش‌فرض امن)
- انجام **Security Architecture Review**
- استفاده از **OWASP ASVS** برای طراحی امن
- پیاده‌سازی **Fail Secure** (در صورت خطا، سیستم باید در حالت امن باقی بماند)

```java
// ✅ درست: استفاده از Security by Design
@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id; // استفاده از UUID به جای sequential ID

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String passwordHash; // همیشه hash شده

    @Column(nullable = false)
    private Boolean enabled = true; // default secure

    @Column(nullable = false)
    private Boolean accountNonLocked = true;

    @Column(nullable = false)
    private Integer failedLoginAttempts = 0;

    @Column
    private LocalDateTime lastLoginAttempt;
}

// Secure Defaults
// application.yml - Secure Defaults
spring:
security:
        # ✅درست:
Secure defaults
require-ssl:true
headers:
frame:DENY
content-type:nosniff
xss-protection:1;mode=block
```

❌ **نباید انجام شود:**

- طراحی بدون در نظر گیری امنیت
- استفاده از تنظیمات پیش‌فرض ناامن

```java
// ❌ اشتباه: طراحی بدون امنیت
@Entity
public class User {
    @Id
    private Long id; // Sequential ID - قابل پیش‌بینی
    private String password; // Plaintext password
}
```

---

### A05:2021 – Security Misconfiguration

**تعریف**: پیکربندی نادرست یا ناقص امنیتی که می‌تواند منجر به آسیب‌پذیری شود.

#### مثال‌های رایج:

1. **Default Credentials**: استفاده از username/password پیش‌فرض
2. **Unnecessary Features**: فعال بودن ویژگی‌های غیرضروری
3. **Missing Security Headers**: عدم تنظیم Security Headers
4. **Verbose Error Messages**: پیام‌های خطای verbose که اطلاعات حساس افشا می‌کنند
5. **Insecure CORS Configuration**: پیکربندی نادرست CORS
6. **Missing HTTPS**: عدم استفاده از HTTPS

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- تغییر تمام credentialهای پیش‌فرض
- غیرفعال کردن ویژگی‌های غیرضروری
- تنظیم Security Headers:
    - `Content-Security-Policy`
    - `X-Content-Type-Options: nosniff`
    - `X-Frame-Options: DENY`
    - `Strict-Transport-Security`
    - `X-XSS-Protection`
- پیکربندی صحیح CORS
- استفاده از HTTPS برای تمام ارتباطات
- پیکربندی صحیح error handling
- استفاده از **Spring Boot Actuator Security**

```java
// تنظیم Security Headers
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .headers(headers -> headers
                        .contentSecurityPolicy(csp -> csp
                                .policyDirectives("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'")
                        )
                        .frameOptions(FrameOptionsConfig::deny)
                        .contentTypeOptions(ContentTypeOptionsConfig::and)
                        .httpStrictTransportSecurity(hsts -> hsts
                                .maxAgeInSeconds(31536000)
                                .includeSubdomains(true)
                        )
                        .xssProtection(xss -> xss
                                .headerValue(XXssProtectionHeaderWriter.HeaderValue.ENABLED_MODE_BLOCK)
                        )
                );
        return http.build();
    }
}

// پیکربندی CORS
@Configuration
public class CorsConfig {
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(Arrays.asList("https://example.com"));
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE"));
        configuration.setAllowedHeaders(Arrays.asList("*"));
        configuration.setAllowCredentials(true);
        configuration.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}

// Custom Error Handling
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception ex) {
        // ✅ درست: عدم افشای جزئیات خطا به کاربر
        ErrorResponse error = new ErrorResponse(
                "An error occurred",
                HttpStatus.INTERNAL_SERVER_ERROR.value()
        );

        // Log جزئیات کامل برای debugging
        logger.error("Error occurred", ex);

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}

// استفاده از Environment Variables برای Secrets
// application.yml
spring:
datasource:
url:

$ {
    DATABASE_URL
}

username:

$ {
    DATABASE_USERNAME
}

password:

$ {
    DATABASE_PASSWORD
}

// غیرفعال کردن ویژگی‌های غیرضروری
management:
endpoints:
web:
exposure:
include:health,info,metrics
exclude:"*" #
فقط endpoints
ضروری
endpoint:
shutdown:
enabled:false
```

❌ **نباید انجام شود:**

- استفاده از credentialهای پیش‌فرض
- فعال بودن ویژگی‌های debug در production
- افشای اطلاعات حساس در error messages
- پیکربندی CORS با `*` (allow all)
- استفاده از HTTP در production
- افشای version numbers در headers

---

### A06:2021 – Vulnerable and Outdated Components

**تعریف**: استفاده از کامپوننت‌ها، کتابخانه‌ها و frameworkهای آسیب‌پذیر یا قدیمی.

#### مثال‌های رایج:

1. **Outdated Dependencies**: وابستگی‌های قدیمی با آسیب‌پذیری‌های شناخته شده
2. **Missing Security Updates**: عدم به‌روزرسانی امنیتی
3. **Unverified Components**: استفاده از کامپوننت‌های تایید نشده
4. **License Issues**: مشکلات لایسنس

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- استفاده از **OWASP Dependency Check** برای اسکن وابستگی‌ها
- استفاده از **Snyk** یا **WhiteSource** برای مدیریت وابستگی‌ها
- به‌روزرسانی منظم تمام dependencies
- استفاده از **Dependabot** یا **Renovate** برای به‌روزرسانی خودکار
- بررسی **CVE (Common Vulnerabilities and Exposures)** برای تمام dependencies
- استفاده از **Maven Enforcer Plugin** برای جلوگیری از استفاده از نسخه‌های آسیب‌پذیر
- انجام **Software Composition Analysis (SCA)**

```xml
<!-- استفاده از OWASP Dependency Check در Maven -->
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>8.4.0</version>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
    <configuration>
        <failBuildOnCVSS>7</failBuildOnCVSS>
        <suppressionFiles>
            <suppressionFile>owasp-suppressions.xml</suppressionFile>
        </suppressionFiles>
    </configuration>
</plugin>

        <!-- Maven Enforcer Plugin -->
<plugin>
<groupId>org.apache.maven.plugins</groupId>
<artifactId>maven-enforcer-plugin</artifactId>
<version>3.3.0</version>
<executions>
    <execution>
        <id>enforce-versions</id>
        <goals>
            <goal>enforce</goal>
        </goals>
        <configuration>
            <rules>
                <requireJavaVersion>
                    <version>[17,)</version>
                </requireJavaVersion>
            </rules>
        </configuration>
    </execution>
</executions>
</plugin>
```

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "maven"
    directory: "/"
    schedule:
      interval: "weekly"
```

```bash
# بررسی dependencies قدیمی
mvn versions:display-dependency-updates

# به‌روزرسانی dependencies
mvn versions:use-latest-versions
```

❌ **نباید انجام شود:**

- استفاده از dependencies بدون بررسی آسیب‌پذیری‌ها
- عدم به‌روزرسانی dependencies
- استفاده از نسخه‌های قدیمی با آسیب‌پذیری‌های شناخته شده
- عدم بررسی لایسنس dependencies

---

### A07:2021 – Identification and Authentication Failures

**تعریف**: مشکلات در سیستم احراز هویت و شناسایی کاربران (قبلاً "Broken Authentication" نامیده می‌شد).

#### مثال‌های رایج:

1. **Weak Passwords**: passwordهای ضعیف
2. **Credential Stuffing**: استفاده از credentialهای لو رفته
3. **Session Fixation**: آسیب‌پذیری Session Fixation
4. **Weak Session Management**: مدیریت ضعیف sessionها
5. **Missing MFA**: عدم وجود Multi-Factor Authentication
6. **Insecure Password Recovery**: فرآیند بازیابی password ناامن

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- پیاده‌سازی **Password Policy** قوی:
    - حداقل 12 کاراکتر
    - ترکیب حروف بزرگ و کوچک، اعداد و کاراکترهای خاص
    - جلوگیری از استفاده از passwordهای رایج
- استفاده از **Multi-Factor Authentication (MFA)**
- پیاده‌سازی **Account Lockout** پس از تلاش‌های ناموفق
- استفاده از **Rate Limiting** برای جلوگیری از brute force
- استفاده از **Secure Session Management**:
    - HttpOnly و Secure flags برای cookies
    - Session timeout
    - Session rotation
- استفاده از **Keycloak** برای مدیریت احراز هویت
- پیاده‌سازی **Password Hashing** با bcrypt/Argon2
- استفاده از **OAuth 2.0 / OpenID Connect**

```java
// استفاده از Password Policy قوی
@Component
public class PasswordPolicyValidator {
    private static final Pattern PASSWORD_PATTERN = Pattern.compile(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{12,}$"
    );

    public void validatePassword(String password) {
        if (password == null || password.length() < 12) {
            throw new WeakPasswordException("Password must be at least 12 characters");
        }

        if (!PASSWORD_PATTERN.matcher(password).matches()) {
            throw new WeakPasswordException(
                    "Password must contain uppercase, lowercase, number, and special character"
            );
        }

        // بررسی common passwords
        if (isCommonPassword(password)) {
            throw new WeakPasswordException("Password is too common");
        }
    }
}

// پیاده‌سازی Multi-Factor Authentication (MFA)
@Service
public class MfaService {
    private final TotpService totpService;

    public void enableMfa(String username) {
        String secret = totpService.generateSecret();
        // ذخیره secret در database
        userRepository.updateMfaSecret(username, secret);
    }

    public boolean verifyMfa(String username, String code) {
        String secret = userRepository.getMfaSecret(username);
        return totpService.verifyCode(secret, code);
    }
}

// مدیریت امن Session
@Configuration
public class SessionConfig {
    @Bean
    public SessionRegistry sessionRegistry() {
        return new SessionRegistryImpl();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .sessionManagement(session -> session
                        .sessionCreationPolicy(SessionCreationPolicy.STATELESS) // برای JWT
                        .maximumSessions(1) // فقط یک session فعال
                        .maxSessionsPreventsLogin(true) // جلوگیری از login همزمان
                );
        return http.build();
    }
}

// Rate Limiting برای Login
@Service
public class LoginAttemptService {
    private final RedisTemplate<String, String> redisTemplate;
    private static final int MAX_ATTEMPTS = 5;
    private static final int LOCK_TIME_MINUTES = 15;

    public void recordFailedAttempt(String username) {
        String key = "login:attempts:" + username;
        String attempts = redisTemplate.opsForValue().get(key);

        if (attempts == null) {
            redisTemplate.opsForValue().set(key, "1", Duration.ofMinutes(LOCK_TIME_MINUTES));
        } else {
            int count = Integer.parseInt(attempts) + 1;
            if (count >= MAX_ATTEMPTS) {
                lockAccount(username);
            } else {
                redisTemplate.opsForValue().set(key, String.valueOf(count),
                        Duration.ofMinutes(LOCK_TIME_MINUTES));
            }
        }
    }
}

// Password Hashing با BCrypt
@Service
public class PasswordService {
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder(12);

    public String hashPassword(String rawPassword) {
        return passwordEncoder.encode(rawPassword);
    }

    public boolean verifyPassword(String rawPassword, String hashedPassword) {
        return passwordEncoder.matches(rawPassword, hashedPassword);
    }
}
```

❌ **نباید انجام شود:**

- استفاده از passwordهای ضعیف
- ذخیره passwordها به صورت plaintext
- استفاده از session IDهای قابل پیش‌بینی
- عدم پیاده‌سازی rate limiting
- افشای اطلاعات کاربر در error messages
- استفاده از HTTP برای authentication

---

### A08:2021 – Software and Data Integrity Failures

**تعریف**: آسیب‌پذیری‌های مرتبط با یکپارچگی نرم‌افزار و داده‌ها (قبلاً "Insecure Deserialization" نامیده می‌شد).

#### مثال‌های رایج:

1. **Insecure Deserialization**: deserialization ناامن
2. **CI/CD Pipeline Vulnerabilities**: آسیب‌پذیری‌های pipeline
3. **Supply Chain Attacks**: حملات زنجیره تامین
4. **Missing Integrity Checks**: عدم بررسی یکپارچگی
5. **Untrusted Data Sources**: استفاده از منابع داده غیرقابل اعتماد

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- استفاده از **Signed Commits** در Git
- پیاده‌سازی **Code Signing** برای artifacts
- استفاده از **Dependency Verification** (checksums)
- پیاده‌سازی **CI/CD Security**:
    - بررسی امنیتی در pipeline
    - استفاده از trusted registries
    - بررسی integrity قبل از deployment
- استفاده از **Container Image Signing**
- پیاده‌سازی **Software Bill of Materials (SBOM)**
- استفاده از **OWASP Dependency Check** در CI/CD

```java
// Safe Deserialization
@Service
public class SafeDeserializationService {
    private final ObjectMapper objectMapper;

    public <T> T deserialize(String json, Class<T> clazz) {
        // ✅ درست: استفاده از whitelist
        objectMapper.setPolymorphicTypeValidator(
                BasicPolymorphicTypeValidator.builder()
                        .allowIfSubType(clazz)
                        .build()
        );

        return objectMapper.readValue(json, clazz);
    }
}

// ❌ ناامن: استفاده از ObjectInputStream
public Object unsafeDeserialize(byte[] data) throws Exception {
    ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
    return ois.readObject(); // خطرناک!
}
```

```bash
# Sign Docker image
docker trust sign myapp:latest
```

```yaml
# .github/workflows/ci.yml
name: CI
on: [ push ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: mvn clean package
      - name: Security Scan
        run: mvn org.owasp:dependency-check-maven:check
```

❌ **نباید انجام شود:**

- استفاده از deserialization ناامن
- عدم بررسی integrity در CI/CD
- استفاده از dependencies از منابع غیرقابل اعتماد
- عدم استفاده از code signing

---

### A09:2021 – Security Logging and Monitoring Failures

**تعریف**: عدم وجود یا ناکافی بودن logging و monitoring امنیتی.

#### مثال‌های رایج:

1. **Missing Security Logs**: عدم ثبت logهای امنیتی
2. **Insufficient Logging**: logging ناکافی
3. **Missing Alerting**: عدم وجود سیستم هشدار
4. **Log Injection**: تزریق در logها
5. **Missing Audit Trail**: عدم وجود audit trail

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- ثبت تمام events امنیتی:
    - Login attempts (موفق و ناموفق)
    - Authorization failures
    - Data access
    - Configuration changes
    - Privilege escalations
- استفاده از **Structured Logging** (JSON)
- پیاده‌سازی **Centralized Logging** (ELK Stack, Loki)
- استفاده از **SIEM (Security Information and Event Management)**
- پیاده‌سازی **Alerting** برای events مهم
- محافظت از logها در برابر tampering
- استفاده از **Audit Logging** برای compliance

```java
// Security Event Logging
@Aspect
@Component
public class SecurityLoggingAspect {
    private static final Logger securityLogger = LoggerFactory.getLogger("SECURITY");

    @AfterReturning("@annotation(RequiresPermission)")
    public void logSuccessfulAccess(JoinPoint joinPoint) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        String method = joinPoint.getSignature().getName();

        securityLogger.info("SUCCESS: user={}, method={}, timestamp={}",
                username, method, Instant.now());
    }

    @AfterThrowing(value = "@annotation(RequiresPermission)", throwing = "ex")
    public void logFailedAccess(JoinPoint joinPoint, Exception ex) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        String method = joinPoint.getSignature().getName();

        securityLogger.warn("FAILED: user={}, method={}, error={}, timestamp={}",
                username, method, ex.getMessage(), Instant.now());
    }
}

// Audit Trail
@Entity
@EntityListeners(AuditingEntityListener.class)
public class AuditLog {
    @Id
    @GeneratedValue
    private Long id;

    private String username;
    private String action;
    private String resource;
    private String ipAddress;
    private LocalDateTime timestamp;
    private String result; // SUCCESS, FAILED
}

// Security Monitoring با Prometheus
@Component
public class SecurityMetrics {
    private final Counter failedLoginAttempts;
    private final Counter successfulLogins;

    public SecurityMetrics(MeterRegistry meterRegistry) {
        this.failedLoginAttempts = Counter.builder("security.login.failed")
                .description("Number of failed login attempts")
                .register(meterRegistry);

        this.successfulLogins = Counter.builder("security.login.successful")
                .description("Number of successful logins")
                .register(meterRegistry);
    }

    public void recordFailedLogin() {
        failedLoginAttempts.increment();
    }

    public void recordSuccessfulLogin() {
        successfulLogins.increment();
    }
}

// Structured Logging با Logback
// logback-spring.xml
/*
<configuration>
    <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
            <providers>
                <timestamp/>
                <version/>
                <logLevel/>
                <message/>
                <mdc/>
                <stackTrace/>
            </providers>
        </encoder>
    </appender>
    
    <logger name="SECURITY" level="INFO" additivity="false">
        <appender-ref ref="JSON"/>
    </logger>
</configuration>
*/

// Centralized Logging با ELK Stack
@Configuration
public class LoggingConfig {
    @Bean
    public LogstashTcpSocketAppender logstashAppender() {
        LogstashTcpSocketAppender appender = new LogstashTcpSocketAppender();
        appender.setDestination("logstash:5044");
        appender.setEncoder(new LogstashEncoder());
        return appender;
    }
}
```

❌ **نباید انجام شود:**

- عدم ثبت logهای امنیتی
- افشای اطلاعات حساس در logها
- عدم محافظت از logها
- عدم پیاده‌سازی alerting
- عدم بررسی logها به صورت منظم

```java
// ❌ اشتباه: عدم ثبت log
public void login(String username, String password) {
    // هیچ logی ثبت نمی‌شود
    authenticate(username, password);
}

// ✅ درست: ثبت log
public void login(String username, String password) {
    logger.info("Login attempt: username={}", username);
    try {
        authenticate(username, password);
        logger.info("Login successful: username={}", username);
    } catch (AuthenticationException e) {
        logger.warn("Login failed: username={}, error={}", username, e.getMessage());
        throw e;
    }
}

// ❌ اشتباه: افشای اطلاعات حساس در log
logger.

info("User password: {}",password); // خطرناک!

// ✅ درست: عدم افشای اطلاعات حساس
logger.

info("Login attempt: username={}",username);
```

#### ابزارهای تست

- **ELK Stack**: Centralized Logging
- **Prometheus + Grafana**: Monitoring و Alerting
- **SIEM Tools**: Splunk, ArcSight
- **Audit Logging Tools**: برای compliance

---

### A10:2021 – Server-Side Request Forgery (SSRF)

**تعریف**: آسیب‌پذیری SSRF زمانی رخ می‌دهد که یک اپلیکیشن وب درخواست‌های HTTP را از سمت سرور به یک URL مشخص شده توسط
کاربر ارسال می‌کند.

#### مثال‌های رایج:

1. **Internal Network Access**: دسترسی به شبکه داخلی
2. **Cloud Metadata API Access**: دسترسی به Cloud Metadata APIs
3. **Port Scanning**: اسکن پورت‌های داخلی
4. **File Access**: دسترسی به فایل‌های محلی
5. **Protocol Smuggling**: استفاده از پروتکل‌های مختلف (file://, gopher://)

#### راه‌حل‌ها:

✅ **باید انجام شود:**

- اعتبارسنجی و فیلتر کردن URLهای ورودی
- استفاده از **Whitelist** برای allowed domains
- غیرفعال کردن redirects
- استفاده از **URL Parser** امن
- محدود کردن پروتکل‌ها (فقط HTTP/HTTPS)
- استفاده از **Network Segmentation**
- پیاده‌سازی **Outbound Firewall Rules**

```java
// ✅ درست: اعتبارسنجی URL
@Service
public class SafeUrlValidator {
    private static final List<String> ALLOWED_DOMAINS = Arrays.asList(
            "api.example.com",
            "cdn.example.com"
    );

    private static final List<String> BLOCKED_PROTOCOLS = Arrays.asList(
            "file", "gopher", "jar", "ldap", "ldaps"
    );

    public URL validateUrl(String urlString) throws MalformedURLException {
        URL url = new URL(urlString);

        // بررسی پروتکل
        String protocol = url.getProtocol().toLowerCase();
        if (BLOCKED_PROTOCOLS.contains(protocol)) {
            throw new IllegalArgumentException("Protocol not allowed: " + protocol);
        }

        if (!protocol.equals("http") && !protocol.equals("https")) {
            throw new IllegalArgumentException("Only HTTP/HTTPS allowed");
        }

        // بررسی domain
        String host = url.getHost().toLowerCase();
        boolean isAllowed = ALLOWED_DOMAINS.stream()
                .anyMatch(domain -> host.equals(domain) || host.endsWith("." + domain));

        if (!isAllowed) {
            throw new IllegalArgumentException("Domain not allowed: " + host);
        }

        // بررسی IPهای داخلی
        if (isInternalIp(host)) {
            throw new IllegalArgumentException("Internal IP not allowed");
        }

        return url;
    }

    private boolean isInternalIp(String host) {
        try {
            InetAddress address = InetAddress.getByName(host);
            return address.isLoopbackAddress() ||
                    address.isLinkLocalAddress() ||
                    address.isSiteLocalAddress() ||
                    isPrivateIp(address);
        } catch (UnknownHostException e) {
            return false;
        }
    }

    private boolean isPrivateIp(InetAddress address) {
        byte[] bytes = address.getAddress();
        if (bytes.length == 4) { // IPv4
            return (bytes[0] == 10) ||
                    (bytes[0] == (byte) 172 && bytes[1] >= 16 && bytes[1] <= 31) ||
                    (bytes[0] == (byte) 192 && bytes[1] == (byte) 168);
        }
        return false;
    }
}

// ✅ درست: استفاده از HttpClient با محدودیت
@Service
public class SafeHttpClientService {
    private final RestTemplate restTemplate;
    private final SafeUrlValidator urlValidator;

    public SafeHttpClientService(SafeUrlValidator urlValidator) {
        this.urlValidator = urlValidator;
        this.restTemplate = new RestTemplate();

        // غیرفعال کردن redirects
        HttpComponentsClientHttpRequestFactory factory =
                new HttpComponentsClientHttpRequestFactory();
        factory.setConnectTimeout(5000);
        factory.setReadTimeout(5000);
        restTemplate.setRequestFactory(factory);
    }

    public String fetchUrl(String urlString) {
        try {
            URL validatedUrl = urlValidator.validateUrl(urlString);

            HttpHeaders headers = new HttpHeaders();
            headers.set("User-Agent", "MyApp/1.0");

            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<String> response = restTemplate.exchange(
                    validatedUrl.toString(),
                    HttpMethod.GET,
                    entity,
                    String.class
            );

            return response.getBody();
        } catch (Exception e) {
            logger.error("Error fetching URL: {}", urlString, e);
            throw new RuntimeException("Failed to fetch URL", e);
        }
    }
}

// ✅ درست: استفاده از DNS Resolution برای بررسی
@Service
public class DnsValidationService {
    public void validateDns(String hostname) {
        try {
            InetAddress[] addresses = InetAddress.getAllByName(hostname);

            for (InetAddress address : addresses) {
                if (isInternalIp(address)) {
                    throw new SecurityException("Internal IP detected: " + address);
                }
            }
        } catch (UnknownHostException e) {
            throw new IllegalArgumentException("Invalid hostname: " + hostname);
        }
    }

    private boolean isInternalIp(InetAddress address) {
        return address.isLoopbackAddress() ||
                address.isLinkLocalAddress() ||
                address.isSiteLocalAddress();
    }
}
```

❌ **نباید انجام شود:**

- اعتماد به URLهای ورودی کاربر
- اجازه دادن به پروتکل‌های خطرناک (file://, gopher://)
- عدم بررسی IPهای داخلی
- اجازه دادن به redirects
- عدم محدودیت domainها

```java
// ❌ اشتباه: عدم اعتبارسنجی URL
@GetMapping("/fetch")
public String fetchUrl(@RequestParam String url) {
    RestTemplate restTemplate = new RestTemplate();
    return restTemplate.getForObject(url, String.class); // خطرناک!
}

// ✅ درست: اعتبارسنجی URL
@GetMapping("/fetch")
public String fetchUrl(@RequestParam String url) {
    URL validatedUrl = urlValidator.validateUrl(url);
    return safeHttpClientService.fetchUrl(validatedUrl.toString());
}

// ❌ اشتباه: اجازه دادن به file://
String url = "file:///etc/passwd"; // خطرناک!

// ✅ درست: فقط HTTP/HTTPS
if(!url.

startsWith("http://") &&!url.

startsWith("https://")){
        throw new

IllegalArgumentException("Only HTTP/HTTPS allowed");
}
```

#### ابزارهای تست

- **Burp Suite**: تست دستی SSRF
- **OWASP ZAP**: تست خودکار SSRF
- **SSRFmap**: ابزار تخصصی تست SSRF

---

## OWASP API Security Top 10

OWASP API Security Top 10 لیست 10 آسیب‌پذیری رایج در APIها است که در سال 2019 منتشر شده است.

### API1:2019 – Broken Object Level Authorization

**تعریف**: APIها اغلب endpointهایی را در معرض قرار می‌دهند که object identifiers را دریافت می‌کنند و کنترل دسترسی در سطح
object را انجام نمی‌دهند.

#### راه‌حل‌ها:

```java
// ✅ درست: بررسی دسترسی در سطح object
@PreAuthorize("@resourceAuthorizationService.canAccess(#resourceId, authentication.principal.id)")
@GetMapping("/api/resources/{resourceId}")
public Resource getResource(@PathVariable Long resourceId) {
    return resourceService.findById(resourceId);
}

@Service
public class ResourceAuthorizationService {
    public boolean canAccess(Long resourceId, Long userId) {
        Resource resource = resourceRepository.findById(resourceId)
                .orElseThrow(() -> new ResourceNotFoundException(resourceId));

        // بررسی مالکیت یا نقش
        return resource.getOwnerId().equals(userId) ||
                hasAdminRole(userId);
    }
}
```

---

### API2:2019 – Broken User Authentication

**تعریف**: مکانیزم‌های احراز هویت اغلب به صورت نادرست پیاده‌سازی می‌شوند و به مهاجمان اجازه می‌دهند که هویت کاربران را
جعل کنند.

#### راه‌حل‌ها:

```java
// ✅ درست: استفاده از JWT با expiration
@Service
public class JwtTokenService {
    private final long JWT_EXPIRATION = 3600000; // 1 hour

    public String generateToken(UserDetails userDetails) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + JWT_EXPIRATION);

        return Jwts.builder()
                .setSubject(userDetails.getUsername())
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .signWith(SignatureAlgorithm.HS512, secretKey)
                .compact();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(secretKey).parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
}
```

---

### API3:2019 – Excessive Data Exposure

**تعریف**: APIها اغلب تمام properties یک object را برمی‌گردانند بدون اینکه بررسی کنند که کاربر به چه داده‌هایی نیاز
دارد.

#### راه‌حل‌ها:

```java
// ✅ درست: استفاده از DTO برای فیلتر کردن داده‌ها
@GetMapping("/api/users/{userId}")
public UserPublicDTO getUser(@PathVariable Long userId) {
    User user = userService.findById(userId);
    return UserPublicDTO.from(user); // فقط داده‌های عمومی
}

public class UserPublicDTO {
    private String username;
    private String email;
    // بدون password, internalId, etc.

    public static UserPublicDTO from(User user) {
        UserPublicDTO dto = new UserPublicDTO();
        dto.setUsername(user.getUsername());
        dto.setEmail(user.getEmail());
        return dto;
    }
}

// ✅ درست: استفاده از @JsonView
public class Views {
    public static class Public {
    }

    public static class Internal extends Public {
    }
}

@Entity
public class User {
    @JsonView(Views.Public.class)
    private String username;

    @JsonView(Views.Internal.class)
    private String internalId;
}
```

---

### API4:2019 – Lack of Resources & Rate Limiting

**تعریف**: APIها اغلب محدودیت‌هایی برای تعداد یا اندازه درخواست‌ها ندارند که می‌تواند منجر به DoS شود.

#### راه‌حل‌ها:

```java
// ✅ درست: Rate Limiting با Bucket4j
@Configuration
public class RateLimitingConfig {
    @Bean
    public RateLimiter rateLimiter() {
        return RateLimiter.of("api", RateLimiterConfig.custom()
                .limitRefreshPeriod(Duration.ofSeconds(1))
                .limitForPeriod(10)
                .timeoutDuration(Duration.ofSeconds(1))
                .build());
    }
}

@RestController
@RateLimiter(name = "api")
public class ApiController {
    @GetMapping("/api/data")
    public ResponseEntity<Data> getData() {
        return ResponseEntity.ok(dataService.getData());
    }
}

// ✅ درست: Rate Limiting با Redis
@Service
public class RedisRateLimitingService {
    private final RedisTemplate<String, String> redisTemplate;

    public boolean isAllowed(String key, int maxRequests, Duration window) {
        String countKey = "rate_limit:" + key;
        String current = redisTemplate.opsForValue().get(countKey);

        if (current == null) {
            redisTemplate.opsForValue().set(countKey, "1", window);
            return true;
        }

        int count = Integer.parseInt(current);
        if (count >= maxRequests) {
            return false;
        }

        redisTemplate.opsForValue().increment(countKey);
        return true;
    }
}
```

---

### API5:2019 – Broken Function Level Authorization

**تعریف**: کنترل دسترسی در سطح function اغلب پیچیده است و می‌تواند منجر به اشتباهات شود.

#### راه‌حل‌ها:

```java
// ✅ درست: استفاده از Method Security
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/api/users/{userId}")
public void deleteUser(@PathVariable Long userId) {
    userService.delete(userId);
}

@PreAuthorize("hasAnyRole('ADMIN', 'MODERATOR')")
@PutMapping("/api/users/{userId}/status")
public void updateUserStatus(@PathVariable Long userId, @RequestBody StatusUpdate update) {
    userService.updateStatus(userId, update);
}
```

---

### API6:2019 – Mass Assignment

**تعریف**: استفاده از توابعی که به صورت خودکار input کاربر را به متغیرهای داخلی object یا دیتابیس bind می‌کنند.

#### راه‌حل‌ها:

```java
// ✅ درست: استفاده از DTO و Whitelist
@PostMapping("/api/users")
public User createUser(@Valid @RequestBody CreateUserRequest request) {
    // فقط فیلدهای مجاز در DTO
    User user = new User();
    user.setUsername(request.getUsername());
    user.setEmail(request.getEmail());
    // role, isAdmin, etc. تنظیم نمی‌شوند
    return userService.save(user);
}

public class CreateUserRequest {
    @NotBlank
    private String username;

    @Email
    private String email;

    // بدون role, isAdmin, etc.
}

// ✅ درست: استفاده از @JsonIgnoreProperties
@Entity
public class User {
    private String username;
    private String email;

    @JsonIgnoreProperties(ignoreUnknown = true)
    private String role; // نمی‌تواند از JSON set شود
}
```

---

### API7:2019 – Security Misconfiguration

**تعریف**: پیکربندی نادرست امنیتی که می‌تواند در هر لایه از stack رخ دهد.

#### راه‌حل‌ها:

- استفاده از Security Headers
- غیرفعال کردن debug mode در production
- پیکربندی صحیح CORS
- استفاده از HTTPS

---

### API8:2019 – Injection

**تعریف**: آسیب‌پذیری‌های تزریق در APIها مشابه وب اپلیکیشن‌ها است.

#### راه‌حل‌ها:

- استفاده از Parameterized Queries
- Input Validation
- Output Encoding

---

### API9:2019 – Improper Assets Management

**تعریف**: APIها اغلب نسخه‌های قدیمی‌تری دارند که آسیب‌پذیری‌های شناخته شده دارند.

#### راه‌حل‌ها:

```java
// ✅ درست: Versioning API
@RestController
@RequestMapping("/api/v1")
public class UserControllerV1 {
    // ...
}

@RestController
@RequestMapping("/api/v2")
public class UserControllerV2 {
    // ...
}

// ✅ درست: Deprecation Headers
@GetMapping("/api/v1/users")
@Deprecated
public List<User> getUsers() {
    response.setHeader("Deprecation", "true");
    response.setHeader("Sunset", "Sat, 31 Dec 2023 23:59:59 GMT");
    return userService.findAll();
}
```

---

### API10:2019 – Insufficient Logging & Monitoring

**تعریف**: عدم وجود یا ناکافی بودن logging و monitoring که می‌تواند منجر به عدم تشخیص حملات شود.

#### راه‌حل‌ها:

- ثبت تمام API calls
- ثبت authentication failures
- ثبت authorization failures
- استفاده از Centralized Logging

---

## OWASP Application Security Verification Standard (ASVS)

OWASP ASVS یک استاندارد برای تایید امنیت اپلیکیشن‌ها است که شامل سطوح مختلف verification می‌شود.

### سطوح ASVS

1. **Level 1**: حداقل امنیت برای اپلیکیشن‌های با ریسک پایین
2. **Level 2**: امنیت استاندارد برای اکثر اپلیکیشن‌ها
3. **Level 3**: امنیت بالا برای اپلیکیشن‌های با ریسک بالا

### دسته‌بندی‌های اصلی ASVS

1. **V1: Architecture, Design and Threat Modeling**
2. **V2: Authentication**
3. **V3: Session Management**
4. **V4: Access Control**
5. **V5: Validation, Sanitization and Encoding**
6. **V6: Stored Cryptography**
7. **V7: Error Handling and Logging**
8. **V8: Data Protection**
9. **V9: Communications**
10. **V10: Malicious Code**
11. **V11: Business Logic**
12. **V12: Files and Resources**
13. **V13: API and Web Services**
14. **V14: Configuration**

---

## OWASP Dependency Check

OWASP Dependency Check یک ابزار open source است که وابستگی‌های پروژه را برای آسیب‌پذیری‌های شناخته شده اسکن می‌کند.

### نصب و استفاده

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>8.4.0</version>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
    <configuration>
        <failBuildOnCVSS>7</failBuildOnCVSS>
        <suppressionFiles>
            <suppressionFile>owasp-suppressions.xml</suppressionFile>
        </suppressionFiles>
        <formats>
            <format>HTML</format>
            <format>JSON</format>
        </formats>
    </configuration>
</plugin>
```

```bash
# اجرای Dependency Check
mvn org.owasp:dependency-check-maven:check

# مشاهده گزارش
open target/dependency-check-report.html
```

---

## OWASP ZAP (Zed Attack Proxy)

OWASP ZAP یک ابزار تست نفوذ خودکار برای وب اپلیکیشن‌ها است.

### استفاده از ZAP

```bash
# نصب ZAP
# Download from: https://www.zaproxy.org/download/

# اجرای ZAP در command line
zap-cli quick-scan --self-contained --start-options '-config api.disablekey=true' http://localhost:8080

# اجرای ZAP با Docker (استفاده از نسخه رسمی از GitHub Container Registry)
docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://localhost:8080

# یا با نسخه مشخص
docker run -t ghcr.io/zaproxy/zaproxy:2.14.0 zap-baseline.py -t http://localhost:8080
```

### پیکربندی ZAP در CI/CD

```yaml
# .github/workflows/security-scan.yml
name: Security Scan
on: [ push ]
jobs:
  zap-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: ZAP Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'http://localhost:8080'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      # یا استفاده مستقیم از Docker image
      - name: ZAP Baseline Scan
        run: |
          docker run --rm \
            -v $(pwd):/zap/wrk/:rw \
            -t ghcr.io/zaproxy/zaproxy:stable \
            zap-baseline.py \
            -t http://localhost:8080 \
            -J zap-report.json \
            -r zap-report.html
```

---

## پیاده‌سازی عملی در پروژه

### 1. پیکربندی Spring Security

```java

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf -> csrf.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()))
                .headers(headers -> headers
                        .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
                        .frameOptions(FrameOptionsConfig::deny)
                        .contentTypeOptions(ContentTypeOptionsConfig::and)
                )
                .sessionManagement(session -> session
                        .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                )
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/api/public/**").permitAll()
                        .requestMatchers("/api/admin/**").hasRole("ADMIN")
                        .anyRequest().authenticated()
                )
                .oauth2ResourceServer(oauth2 -> oauth2
                        .jwt(jwt -> jwt.jwtDecoder(jwtDecoder()))
                );

        return http.build();
    }

    @Bean
    public JwtDecoder jwtDecoder() {
        return NimbusJwtDecoder.withJwkSetUri("https://keycloak.example.com/realms/myapp/protocol/openid-connect/certs")
                .build();
    }
}
```

### 2. پیاده‌سازی Input Validation

```java

@RestController
@Validated
public class UserController {

    @PostMapping("/api/users")
    public ResponseEntity<User> createUser(@Valid @RequestBody CreateUserRequest request) {
        User user = userService.createUser(request);
        return ResponseEntity.ok(user);
    }
}

public class CreateUserRequest {
    @NotBlank(message = "Username is required")
    @Size(min = 3, max = 50)
    @Pattern(regexp = "^[a-zA-Z0-9_]+$")
    private String username;

    @NotBlank(message = "Email is required")
    @Email(message = "Email must be valid")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 12, message = "Password must be at least 12 characters")
    @Pattern(regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{12,}$")
    private String password;
}
```

### 3. پیاده‌سازی Logging و Monitoring

```java

@Aspect
@Component
@Slf4j
public class SecurityLoggingAspect {

    @AfterReturning("@annotation(org.springframework.security.access.prepost.PreAuthorize)")
    public void logSuccessfulAccess(JoinPoint joinPoint) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        String method = joinPoint.getSignature().getName();

        log.info("SUCCESS: user={}, method={}, timestamp={}",
                username, method, Instant.now());
    }

    @AfterThrowing(value = "@annotation(org.springframework.security.access.prepost.PreAuthorize)",
            throwing = "ex")
    public void logFailedAccess(JoinPoint joinPoint, Exception ex) {
        String username = SecurityContextHolder.getContext().getAuthentication().getName();
        String method = joinPoint.getSignature().getName();

        log.warn("FAILED: user={}, method={}, error={}, timestamp={}",
                username, method, ex.getMessage(), Instant.now());
    }
}
```

---

## چک‌لیست امنیتی

### چک‌لیست قبل از Deployment

- [ ] تمام dependencies به‌روزرسانی شده‌اند
- [ ] OWASP Dependency Check اجرا شده و هیچ آسیب‌پذیری بالای 7 وجود ندارد
- [ ] تمام Security Headers تنظیم شده‌اند
- [ ] HTTPS فعال است
- [ ] CORS به درستی پیکربندی شده است
- [ ] Input Validation در تمام endpoints پیاده‌سازی شده است
- [ ] Authentication و Authorization به درستی کار می‌کند
- [ ] Password Policy پیاده‌سازی شده است
- [ ] Rate Limiting فعال است
- [ ] Logging و Monitoring پیاده‌سازی شده است
- [ ] Error Handling به درستی انجام می‌شود (بدون افشای اطلاعات حساس)
- [ ] تمام credentialهای پیش‌فرض تغییر کرده‌اند
- [ ] Debug mode غیرفعال است
- [ ] OWASP ZAP scan انجام شده است

### چک‌لیست OWASP Top 10

- [ ] **A01**: Broken Access Control - کنترل دسترسی در تمام endpoints بررسی می‌شود
- [ ] **A02**: Cryptographic Failures - از الگوریتم‌های قوی استفاده می‌شود
- [ ] **A03**: Injection - از Parameterized Queries استفاده می‌شود
- [ ] **A04**: Insecure Design - Threat Modeling انجام شده است
- [ ] **A05**: Security Misconfiguration - Security Headers تنظیم شده‌اند
- [ ] **A06**: Vulnerable Components - Dependencies به‌روزرسانی شده‌اند
- [ ] **A07**: Authentication Failures - Password Policy و MFA پیاده‌سازی شده است
- [ ] **A08**: Software Integrity Failures - Code Signing و Dependency Verification انجام می‌شود
- [ ] **A09**: Logging Failures - Security Logging پیاده‌سازی شده است
- [ ] **A10**: SSRF - URL Validation پیاده‌سازی شده است

---

## رفرنس‌ها و منابع

### منابع رسمی OWASP

- **OWASP Website**: https://owasp.org/
- **OWASP Top 10 (2021)**: https://owasp.org/www-project-top-ten/
- **OWASP API Security Top 10**: https://owasp.org/www-project-api-security/
- **OWASP ASVS**: https://owasp.org/www-project-application-security-verification-standard/
- **OWASP Dependency Check**: https://owasp.org/www-project-dependency-check/
- **OWASP ZAP**: https://www.zaproxy.org/
- **OWASP Cheat Sheet Series**: https://cheatsheetseries.owasp.org/

### مستندات Spring Security

- **Spring Security Reference**: https://docs.spring.io/spring-security/reference/
- **Spring Security OAuth2**: https://docs.spring.io/spring-security/reference/servlet/oauth2/index.html

### ابزارهای امنیتی

- **Snyk**: https://snyk.io/
- **WhiteSource**: https://www.whitesourcesoftware.com/
- **SonarQube**: https://www.sonarqube.org/
- **Burp Suite**: https://portswigger.net/burp

### کتاب‌ها و مقالات

- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/
- **Secure Coding Practices**: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/

---

<div align="right">

[← بازگشت به Security](Security-Home) | [← صفحه اصلی](Home)

</div>