# تست‌های Frontend

<div align="right">

[← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

---

## هدف

تست‌های Frontend برای اطمینان از کیفیت و عملکرد UI.

## انواع تست

### 1. Unit Tests

- تست components
- تست utilities
- تست hooks
- تست reducers

### 2. Integration Tests

- تست component interactions
- تست API integration
- تست routing

### 3. E2E Tests

- تست user workflows
- تست complete scenarios
- تست cross-browser

## تکنولوژی‌ها

### Testing Frameworks

- **Jest**: Testing framework
- **React Testing Library**: Component testing
- **Cypress**: E2E testing
- **MSW**: API mocking

## Unit Testing

### Component Test

```typescript
import { render, screen } from '@testing-library/react';
import { OrderList } from './OrderList';

test('renders order list', () => {
  render(<OrderList orders={mockOrders} />);
  expect(screen.getByText('Order #1')).toBeInTheDocument();
});
```

### Hook Test

```typescript
import { renderHook } from '@testing-library/react';
import { useOrders } from './useOrders';

test('fetches orders', async () => {
  const { result } = renderHook(() => useOrders());
  await waitFor(() => {
    expect(result.current.data).toBeDefined();
  });
});
```

## Integration Testing

### API Integration

```typescript
test('creates order and updates list', async () => {
  render(<OrderPage />);
  fireEvent.click(screen.getByText('Create Order'));
  // Fill form
  fireEvent.click(screen.getByText('Submit'));
  await waitFor(() => {
    expect(screen.getByText('Order created')).toBeInTheDocument();
  });
});
```

## E2E Testing

### Cypress Test

```typescript
describe('Order Creation', () => {
  it('creates a new order', () => {
    cy.visit('/orders');
    cy.get('[data-testid="create-order"]').click();
    cy.get('[name="customer"]').type('John Doe');
    cy.get('[name="amount"]').type('100');
    cy.get('[type="submit"]').click();
    cy.contains('Order created successfully').should('be.visible');
  });
});
```

## Best Practices

1. **Test User Behavior**: تست از دید کاربر
2. **Accessibility**: تست accessibility
3. **Performance**: تست performance
4. **Coverage**: حداقل 80% coverage

## لینک‌های مفید

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [React Testing Library Documentation](https://testing-library.com/react)
- [Cypress Documentation](https://docs.cypress.io/)
- [MSW Documentation](https://mswjs.io/docs/)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Accessibility Testing](https://www.w3.org/WAI/test-evaluate/)

---

<div align="center">

[↑ بازگشت به بالا](#تستهای-frontend) | [← بازگشت به Frontend](Frontend-Home) | [← صفحه اصلی](Frontend-Home)

</div>

