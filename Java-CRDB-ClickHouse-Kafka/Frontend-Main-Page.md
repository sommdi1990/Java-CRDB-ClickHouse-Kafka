# صفحه اصلی سایت

<div align="right">

[← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

---

## هدف

صفحه اصلی سایت که نقطه ورود کاربران به سیستم است.

## قابلیت‌ها

### 1. Landing Page

- معرفی سیستم
- ویژگی‌های کلیدی
- Call-to-action buttons
- Navigation menu

### 2. Authentication

- Login form
- Registration (در صورت نیاز)
- Password recovery
- Social login options

### 3. Public Information

- درباره ما
- تماس با ما
- مستندات عمومی
- FAQ

## ساختار

### Components

```
main-page/
├── Header/
│   ├── Navigation
│   ├── User Menu
│   └── Language Selector
├── Hero Section/
│   ├── Title
│   ├── Description
│   └── CTA Buttons
├── Features Section/
│   └── Feature Cards
├── Footer/
│   ├── Links
│   └── Social Media
└── Login Modal/
    ├── Login Form
    └── Registration Form
```

## تکنولوژی‌ها

- **React 18+**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool و development server
- **React Router**: Routing
- **Material-UI**: UI components
- **React Hook Form**: Form management

## Routing

```typescript
<Routes>
  <Route path="/" element={<HomePage />} />
  <Route path="/about" element={<AboutPage />} />
  <Route path="/contact" element={<ContactPage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route path="/register" element={<RegisterPage />} />
</Routes>
```

## State Management

- **React Query**: برای server state
- **Context API**: برای global state
- **Local State**: برای component state

## Responsive Design

- **Mobile-first**: طراحی اول برای mobile
- **Breakpoints**:
    - Mobile: < 768px
    - Tablet: 768px - 1024px
    - Desktop: > 1024px

## SEO

- **Meta Tags**: برای SEO
- **Structured Data**: Schema.org
- **Sitemap**: XML sitemap
- **Robots.txt**: برای crawlers

## لینک‌های مفید

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [React Router Documentation](https://reactrouter.com/)
- [Material-UI Documentation](https://mui.com/)
- [React Hook Form Documentation](https://react-hook-form.com/)
- [React Query Documentation](https://tanstack.com/query/latest)
- [SEO Best Practices](https://developers.google.com/search/docs/beginner/seo-starter-guide)
- [Schema.org](https://schema.org/) - Structured data

---

<div align="center">

[↑ بازگشت به بالا](#صفحه-اصلی-سایت) | [← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

