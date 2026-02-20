# Git Workflow

<div align="right">

[← بازگشت به Development](Development-Home) | [← صفحه اصلی](Development-Home)

</div>

---

## هدف

Git workflow برای collaboration.

## Branch Strategy

### Main Branches

- **main**: Production code
- **develop**: Development branch

### Feature Branches

- **feature/**: برای features جدید
- **bugfix/**: برای bug fixes
- **hotfix/**: برای urgent fixes

## Workflow

### Feature Development

```bash
git checkout develop
git pull
git checkout -b feature/new-feature
# Develop feature
git commit -m "Add new feature"
git push origin feature/new-feature
# Create Pull Request
```

### Code Review

- Pull Request creation
- Code review
- Approval
- Merge

## Commit Messages

### Format

```
type(scope): subject

body

footer
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **refactor**: Code refactoring

## Best Practices

1. **Small Commits**: commits کوچک
2. **Clear Messages**: پیام‌های واضح
3. **Regular Pulls**: pull منظم
4. **Code Reviews**: بررسی کد

## لینک‌های مفید

- [Git Documentation](https://git-scm.com/doc)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pull Request Best Practices](https://github.com/blog/1943-how-to-write-the-perfect-pull-request)

---

<div align="center">

[↑ بازگشت به بالا](#git-workflow) | [← بازگشت به Development](Development-Home) | [← صفحه اصلی](Development-Home)

</div>

