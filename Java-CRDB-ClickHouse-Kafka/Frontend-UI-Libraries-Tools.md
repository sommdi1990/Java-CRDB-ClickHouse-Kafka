# UI Libraries & Tools

<div align="right">

[← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

---

## معرفی

این مستندات کتابخانه‌ها و ابزارهای UI استفاده شده در پروژه را پوشش می‌دهد.

## React Query

### هدف

مدیریت state سرور (server state) به صورت بهینه و خودکار.

### مزایا

- **Automatic Caching**: Cache management خودکار
- **Background Updates**: به‌روزرسانی در پس‌زمینه
- **Optimistic Updates**: به‌روزرسانی خوشبینانه
- **Error Handling**: مدیریت خطا
- **Loading States**: مدیریت وضعیت loading

### استفاده

```typescript
import { useQuery, useMutation } from '@tanstack/react-query';

// Query
const { data, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers
});

// Mutation
const mutation = useMutation({
  mutationFn: createUser,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['users'] });
  }
});
```

### Integration با RTK Query

- React Query برای server state
- RTK Query برای API layer
- Redux Toolkit برای client state

## React Hook Form

### هدف

مدیریت فرم‌های پیچیده با performance بالا و validation.

### مزایا

- **Performance**: Re-render کمتر
- **Validation**: Built-in validation
- **Type Safety**: TypeScript support
- **Easy Integration**: Integration با validation libraries

### استفاده

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(1),
  email: z.string().email()
});

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema)
});
```

### Integration با Zod

- Schema-based validation
- Type inference
- Error messages

## AG Grid

### هدف

جداول پیشرفته با قابلیت‌های enterprise.

### مزایا

- **Performance**: Virtual scrolling
- **Features**: Sorting, filtering, grouping, pivoting
- **Customization**: Highly customizable
- **Export**: Excel, CSV export

### استفاده

```typescript
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

<AgGridReact
  rowData={data}
  columnDefs={columns}
  pagination={true}
  paginationPageSize={20}
/>
```

### جایگزین: TanStack Table

- **TanStack Table**: Lightweight alternative
- مناسب برای جداول ساده‌تر
- More flexible
- Better TypeScript support

## Recharts

### هدف

نمودارها و visualization با React.

### مزایا

- **React Native**: Built for React
- **Composable**: Composable components
- **Responsive**: Responsive charts
- **Customizable**: Highly customizable

### استفاده

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

<LineChart data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="name" />
  <YAxis />
  <Tooltip />
  <Legend />
  <Line type="monotone" dataKey="value" stroke="#8884d8" />
</LineChart>
```

### جایگزین: Chart.js

- **Chart.js**: Popular charting library
- React wrapper: `react-chartjs-2`
- More chart types
- Better documentation

## Storybook

### هدف

توسعه و مستندسازی کامپوننت‌ها به صورت isolated.

### مزایا

- **Isolated Development**: توسعه جداگانه کامپوننت‌ها
- **Documentation**: مستندسازی خودکار
- **Testing**: Visual testing
- **Sharing**: Share components

### Setup

```bash
npx storybook@latest init
```

### استفاده

```typescript
// Button.stories.tsx
import { Button } from './Button';

export default {
  title: 'Components/Button',
  component: Button,
};

export const Primary = {
  args: {
    label: 'Button',
  },
};
```

### Features

- **Controls**: Interactive controls
- **Actions**: Event handlers
- **Docs**: Auto-generated docs
- **Addons**: Extensions

## سایر کتابخانه‌های مفید

### UI Components

- **Material-UI (MUI)**: Material Design components
- **Ant Design**: Enterprise UI components
- **Chakra UI**: Simple and modular

### Form Validation

- **Zod**: Schema validation
- **Yup**: Alternative to Zod

### State Management

- **Redux Toolkit**: Client state
- **Zustand**: Lightweight alternative

### Utilities

- **Lodash**: Utility functions
- **Date-fns**: Date manipulation
- **Axios**: HTTP client

## لینک‌های مفید

- [React Query Documentation](https://tanstack.com/query/latest)
- [React Hook Form Documentation](https://react-hook-form.com/)
- [AG Grid Documentation](https://www.ag-grid.com/documentation/)
- [TanStack Table Documentation](https://tanstack.com/table/latest)
- [Recharts Documentation](https://recharts.org/)
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [Storybook Documentation](https://storybook.js.org/docs/)
- [Zod Documentation](https://zod.dev/)
- [Yup Documentation](https://github.com/jquense/yup)
- [Material-UI Documentation](https://mui.com/)
- [Ant Design Documentation](https://ant.design/)
- [Chakra UI Documentation](https://chakra-ui.com/)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)
- [Zustand Documentation](https://zustand-demo.pmnd.rs/)
- [Axios Documentation](https://axios-http.com/docs/intro)

---

<div align="center">

[↑ بازگشت به بالا](#ui-libraries--tools) | [← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

