# معماری Micro Frontends

<div align="right">

[← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

---

## معرفی

معماری Micro Frontends به ما امکان توسعه مستقل ماژول‌های frontend را می‌دهد.

## ساختار

```
shell/                    # Container Application
├── main-page/            # Micro Frontend 1
├── user-panel/           # Micro Frontend 2
└── admin-panel/          # Micro Frontend 3
```

## تکنولوژی‌ها

- **Module Federation** (Webpack 5) یا **Vite Plugin Federation**
- **Single-SPA** (جایگزین)
- **qiankun** (جایگزین)

## مزایا

- توسعه مستقل
- Deploy مستقل
- استفاده از تکنولوژی‌های مختلف (در صورت نیاز)
- تیم‌های مستقل

## چالش‌ها

- State management بین micro frontends
- Routing
- Shared dependencies
- Styling conflicts

## راه‌حل‌ها

- استفاده از **Redux Toolkit** برای shared state
- استفاده از **React Router** برای routing
- استفاده از **Module Federation** برای shared dependencies
- استفاده از **CSS Modules** یا **Styled Components** برای styling

## مثال

```javascript
// shell/src/bootstrap.js
import { mount } from 'main-page/MainPage';
import { mount as mountUserPanel } from 'user-panel/UserPanel';

mount(document.getElementById('main-page'));
mountUserPanel(document.getElementById('user-panel'));
```

## لینک‌های مفید

- [Module Federation Documentation](https://webpack.js.org/concepts/module-federation/)
- [Single-SPA Documentation](https://single-spa.js.org/docs/getting-started-overview)
- [qiankun Documentation](https://qiankun.umijs.org/)
- [Micro Frontends Guide](https://micro-frontends.org/)
- [Webpack Module Federation](https://webpack.js.org/concepts/module-federation/)
- [Vite Plugin Federation](https://github.com/originjs/vite-plugin-federation)

---

<div align="center">

[↑ بازگشت به بالا](#معماری-micro-frontends) | [← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

