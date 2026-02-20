# نسخه‌گذاری (Versioning)

<div align="right">

[← بازگشت به CI-CD](Home) | [← صفحه اصلی](Home)

</div>

---

## استراتژی

استفاده از **Semantic Versioning** (SemVer):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: تغییرات ناسازگار (breaking changes)
- **MINOR**: قابلیت‌های جدید (backward compatible)
- **PATCH**: رفع باگ‌ها (backward compatible)

## مثال

- `1.0.0` - نسخه اولیه
- `1.1.0` - اضافه شدن قابلیت جدید
- `1.1.1` - رفع باگ
- `2.0.0` - تغییرات ناسازگار

## Git Tags

```bash
# ایجاد tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# لیست tags
git tag -l

# حذف tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

## GitHub Releases

- استفاده از GitHub Releases برای release notes
- Automatic changelog generation
- Asset management

## Changelog

نگهداری فایل `CHANGELOG.md` برای tracking تغییرات:

```markdown
# Changelog

## [1.1.0] - 2024-01-15
### Added
- Feature X
- Feature Y

### Changed
- Improvement Z

### Fixed
- Bug fix A
```

## Automation

- استفاده از **Conventional Commits** برای automatic versioning
- استفاده از **semantic-release** برای automatic releases

## لینک‌های مفید

- [Semantic Versioning Specification](https://semver.org/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Releases Documentation](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [semantic-release Documentation](https://semantic-release.gitbook.io/semantic-release/)
- [Keep a Changelog](https://keepachangelog.com/)

---

<div align="center">

[↑ بازگشت به بالا](#نسخهگذاری-versioning) | [← بازگشت به CI-CD](Home) | [← صفحه اصلی](Home)

</div>

