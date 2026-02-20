# Accounting Service

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

سیستم حسابداری کامل با مدیریت اسناد، حساب‌ها و دفاتر سالیانه.

## قابلیت‌ها

### 1. مدیریت اسناد حسابداری

#### انواع اسناد

- **سند حسابداری**: سند اصلی حسابداری
- **فاکتور خرید**: فاکتورهای خرید کالا و خدمات
- **فاکتور فروش**: فاکتورهای فروش کالا و خدمات
- **چک**: چک‌های دریافتی و پرداختی
- **سفته**: سفته‌های دریافتی و پرداختی
- **اسناد دریافتنی**: مطالبات از مشتریان
- **اسناد پرداختنی**: بدهی‌ها به تامین‌کنندگان
- **سند افتتاحیه**: برای شروع سال مالی
- **سند اختتامیه**: برای پایان سال مالی

#### ویژگی‌های اسناد

- شماره‌گذاری خودکار
- تاریخ سند
- شرح سند
- بدهکار و بستانکار
- تایید و تصویب
- Integration با WorkFlow برای approval

### 2. مدیریت حساب‌ها

#### ساختار حساب‌ها

```
حساب کل (Level 1)
  └── حساب معین (Level 2)
      └── حساب تفصیلی (Level 3)
```

#### انواع حساب‌ها

- **حساب کل**: حساب‌های اصلی (دارایی، بدهی، سرمایه، درآمد، هزینه)
- **حساب معین**: زیرمجموعه حساب کل
- **حساب تفصیلی**: جزئیات بیشتر

#### کدینگ حساب‌ها

- ساختار سلسله‌مراتبی
- کد منحصر به فرد
- نام حساب
- نوع حساب (دارایی، بدهی، سرمایه، درآمد، هزینه)
- حساب کل معین تفصیلی

### 3. دفاتر سالیانه

#### دفتر روزنامه

- ثبت تمام اسناد به ترتیب تاریخ
- شامل: شماره سند، تاریخ، شرح، بدهکار، بستانکار

#### دفتر کل

- ثبت تمام حساب‌های کل
- شامل: مانده ابتدای دوره، گردش بدهکار، گردش بستانکار، مانده

#### دفتر معین

- ثبت حساب‌های معین
- جزئیات بیشتر از دفتر کل

#### تراز آزمایشی

- لیست تمام حساب‌ها با مانده
- جمع بدهکار = جمع بستانکار
- بررسی صحت ثبت‌ها

#### ترازنامه

- نمایش دارایی‌ها و بدهی‌ها
- در یک تاریخ مشخص
- معادله حسابداری: دارایی = بدهی + سرمایه

#### سود و زیان

- نمایش درآمدها و هزینه‌ها
- در یک دوره زمانی
- محاسبه سود/زیان خالص

### 4. گزارشات حسابداری

#### گزارشات اصلی

- **ترازنامه**: وضعیت مالی در یک تاریخ
- **سود و زیان**: عملکرد مالی در یک دوره
- **گردش حساب**: گردش یک حساب خاص
- **دفتر کل**: جزئیات حساب‌های کل
- **دفتر معین**: جزئیات حساب‌های معین
- **دفتر روزنامه**: تمام اسناد

#### گزارشات تکمیلی

- گزارشات تحلیلی
- گزارشات مقایسه‌ای
- گزارشات بودجه
- گزارشات مالیاتی

## معماری DDD

### Domain Model

```
Accounting Domain
├── Document (Aggregate Root)
│   ├── DocumentItem
│   ├── DocumentNumber
│   └── DocumentStatus
├── Account (Aggregate Root)
│   ├── AccountCode
│   ├── AccountName
│   └── AccountType
├── Ledger (Aggregate Root)
│   ├── LedgerEntry
│   └── Balance
└── FinancialStatement
    ├── BalanceSheet
    └── IncomeStatement
```

### Entities

- **Document**: سند حسابداری
- **Account**: حساب
- **LedgerEntry**: ردیف دفتر
- **FinancialStatement**: صورت مالی

### Value Objects

- **Money**: مقدار پولی
- **AccountCode**: کد حساب
- **DocumentNumber**: شماره سند
- **DateRange**: بازه زمانی

## تکنولوژی‌ها

- **Spring Boot 4.0.1** (با پشتیبانی از GraalVM Native)
- **Spring Data JPA**
- **DDD Architecture**
- **JasperReports**: برای گزارشات
- **DynamicReports**: برای گزارشات پویا

## API Endpoints

### Documents

- `POST /api/accounting/documents` - ایجاد سند جدید
- `GET /api/accounting/documents/{id}` - دریافت سند
- `PUT /api/accounting/documents/{id}` - به‌روزرسانی سند
- `DELETE /api/accounting/documents/{id}` - حذف سند
- `POST /api/accounting/documents/{id}/approve` - تایید سند

### Accounts

- `GET /api/accounting/accounts` - لیست حساب‌ها
- `POST /api/accounting/accounts` - ایجاد حساب جدید
- `GET /api/accounting/accounts/{id}` - دریافت حساب
- `PUT /api/accounting/accounts/{id}` - به‌روزرسانی حساب

### Ledgers

- `GET /api/accounting/ledgers/journal` - دفتر روزنامه
- `GET /api/accounting/ledgers/general` - دفتر کل
- `GET /api/accounting/ledgers/subsidiary` - دفتر معین
- `GET /api/accounting/ledgers/trial-balance` - تراز آزمایشی

### Financial Statements

- `GET /api/accounting/statements/balance-sheet` - ترازنامه
- `GET /api/accounting/statements/income-statement` - سود و زیان

## Integration

### با Report Manager

- گزارشات حسابداری از طریق Report Manager
- استفاده از JasperReports و DynamicReports
- Template management

### با Document Archive

- ذخیره اسناد حسابداری
- Attachment management

### با eSignature

- امضای دیجیتال اسناد حسابداری
- Approval workflow

### با WorkFlow

- Approval workflow برای اسناد
- Business rules برای validation

## Business Rules

### Validation Rules

- معادله حسابداری: جمع بدهکار = جمع بستانکار
- تاریخ سند باید در بازه سال مالی باشد
- حساب‌ها باید معتبر باشند
- مانده حساب‌ها باید صحیح باشند

### Accounting Principles

- اصل بدهکار و بستانکار
- اصل دوره مالی
- اصل تحقق درآمد
- اصل تطابق هزینه با درآمد

## لینک‌های مفید

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Spring Data JPA Documentation](https://spring.io/projects/spring-data-jpa)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [DDD Patterns](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [JasperReports Documentation](https://community.jaspersoft.com/documentation)
- [DynamicReports Documentation](https://www.dynamicreports.org/documentation)
- [Accounting Principles](https://www.accountingcoach.com/accounting-basics/explanation)
- [Double-Entry Bookkeeping](https://www.investopedia.com/terms/d/double-entry.asp)

---

<div align="center">

[↑ بازگشت به بالا](#accounting-service) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

