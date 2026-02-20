# Web Responsive & PWA

<div align="right">

[← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

---

## هدف

پیاده‌سازی Web Responsive و Progressive Web App (PWA) برای دسترسی بهینه از موبایل و تبلت.

## Web Responsive

### Mobile-First Design

- طراحی اول برای mobile
- سپس scale up برای desktop
- Breakpoints:
    - Mobile: < 768px
    - Tablet: 768px - 1024px
    - Desktop: > 1024px

### Responsive Techniques

- **Flexbox**: برای layouts
- **CSS Grid**: برای complex layouts
- **Media Queries**: برای responsive design
- **Viewport Meta Tag**: برای mobile optimization

### Touch-Friendly UI

- بزرگ بودن touch targets (min 44x44px)
- Gesture support
- Swipe actions
- Pull-to-refresh

## Progressive Web App (PWA)

### ویژگی‌های PWA

1. **Installable**
    - Web App Manifest
    - Add to Home Screen
    - App-like experience

2. **Offline Capability**
    - Service Workers
    - Caching strategies
    - Offline fallbacks

3. **Push Notifications**
    - Web Push API
    - Notification API
    - Badge API

4. **App-like Experience**
    - Full-screen mode
    - Splash screen
    - App icons

## تکنولوژی‌ها

### Core Technologies

- **React 18+**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool و development server

### Responsive CSS

- **Tailwind CSS**: Utility-first CSS
- **Material-UI**: Responsive components
- **Bootstrap**: Alternative option

### PWA Tools

- **Workbox**: Service worker library
- **PWA Builder**: PWA tools
- **Lighthouse**: PWA auditing

## Service Worker

### Caching Strategies

1. **Cache First**
    - برای static assets
    - Fast loading
    - Offline support

2. **Network First**
    - برای dynamic content
    - Fresh data
    - Fallback to cache

3. **Stale While Revalidate**
    - برای frequently updated content
    - Fast response
    - Background update

### Service Worker Registration

```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(registration => {
      console.log('SW registered');
    });
}
```

## Web App Manifest

```json
{
  "name": "My App",
  "short_name": "App",
  "description": "My Progressive Web App",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

## Offline Support

### IndexedDB

- Local database
- Structured data storage
- Async API

### Cache API

- HTTP response caching
- Request/Response storage
- Version management

## Push Notifications

### Web Push Setup

```javascript
// Request permission
const permission = await Notification.requestPermission();

// Subscribe to push
const subscription = await registration.pushManager.subscribe({
  userVisibleOnly: true,
  applicationServerKey: urlBase64ToUint8Array(publicVapidKey)
});
```

## Performance Optimization

1. **Lazy Loading**
    - Code splitting
    - Image lazy loading
    - Route-based splitting

2. **Optimization**
    - Image optimization
    - Minification
    - Compression

3. **Monitoring**
    - Lighthouse CI
    - Web Vitals
    - Performance monitoring

## Testing

- **Lighthouse**: PWA audit
- **Chrome DevTools**: PWA testing
- **Responsive Design Mode**: Mobile testing
- **Device Testing**: Real device testing

## لینک‌های مفید

- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Service Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)
- [Workbox Documentation](https://developers.google.com/web/tools/workbox)
- [PWA Builder](https://www.pwabuilder.com/)
- [Lighthouse Documentation](https://developer.chrome.com/docs/lighthouse/)
- [Responsive Design Guidelines](https://web.dev/responsive-web-design-basics/)
- [Mobile-First Design](https://www.smashingmagazine.com/2012/07/responsive-web-design-guidelines-tutorials/)

---

<div align="center">

[↑ بازگشت به بالا](#web-responsive--pwa) | [← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

