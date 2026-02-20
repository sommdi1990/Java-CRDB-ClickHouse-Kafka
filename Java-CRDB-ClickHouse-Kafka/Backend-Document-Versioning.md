# Document Versioning

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

مدیریت نسخه‌های اسناد با قابلیت tracking تغییرات، diff viewing و rollback.

## قابلیت‌ها

### 1. Version Control

- ایجاد نسخه‌های جدید
- Version history
- Version metadata
- Version comparison

### 2. Change Tracking

- Track تغییرات در documents
- Diff viewing
- Change annotations
- Author tracking

### 3. Rollback

- Rollback به نسخه‌های قبلی
- Restore deleted versions
- Version branching (در صورت نیاز)
- Version merging (در صورت نیاز)

### 4. Version Metadata

- Version number
- Creation date
- Author
- Change description
- Tags

## تکنولوژی‌ها

### Versioning Strategies

1. **Database-based Versioning**
    - ذخیره هر version در database
    - استفاده از version number
    - مناسب برای metadata-heavy documents

2. **File System Versioning**
    - ذخیره هر version به صورت فایل جداگانه
    - استفاده از naming convention
    - مناسب برای file-based documents

3. **Git-like Versioning**
    - استفاده از Git برای versioning
    - Full history و branching
    - مناسب برای code-like documents

4. **Delta Storage**
    - ذخیره فقط تغییرات (deltas)
    - کاهش storage space
    - نیاز به reconstruction

## ساختار Service

```
document-versioning-service/
├── version/
│   ├── creation/
│   ├── storage/
│   └── retrieval/
├── diff/
│   ├── calculation/
│   └── visualization/
├── history/
│   └── tracking/
└── rollback/
    └── restoration/
```

## API Endpoints

### Version Management

- `POST /api/versions` - ایجاد version جدید
- `GET /api/versions/{documentId}` - لیست versions
- `GET /api/versions/{documentId}/{version}` - دریافت version خاص
- `DELETE /api/versions/{documentId}/{version}` - حذف version

### Diff & Comparison

- `GET /api/versions/{documentId}/diff` - مقایسه دو version
- `GET /api/versions/{documentId}/{version1}/diff/{version2}` - Diff بین دو version

### Rollback

- `POST /api/versions/{documentId}/rollback/{version}` - Rollback به version خاص
- `POST /api/versions/{documentId}/restore/{version}` - Restore version

## Version Schema

```sql
CREATE TABLE document_versions (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL,
    version_number INTEGER NOT NULL,
    content BYTEA,
    metadata JSONB,
    created_at TIMESTAMP,
    created_by UUID,
    change_description TEXT,
    UNIQUE(document_id, version_number)
);
```

## Diff Algorithm

### Text Documents

- استفاده از **Myers Diff Algorithm**
- Line-by-line comparison
- Character-level diff (در صورت نیاز)

### Binary Documents

- Metadata comparison
- File hash comparison
- Size comparison

## Best Practices

1. **Version Naming**
    - Semantic versioning: `MAJOR.MINOR.PATCH`
    - یا Sequential: `1, 2, 3, ...`

2. **Storage Optimization**
    - Delta storage برای large documents
    - Compression
    - Archiving old versions

3. **Access Control**
    - Version-level permissions
    - Audit logging
    - Change approval workflow

## Configuration

```yaml
document-versioning:
  strategy: database
  storage:
    type: database
    max-versions: 100
    auto-archive: true
  diff:
    algorithm: myers
    show-context: true
```

## Integration با سایر سرویس‌ها

- Integration با Document Archive Service
- Integration با eSignature Service (برای signed document versions)
- Integration با WorkFlow Service (برای version approval)
- Integration با Report Manager (برای report versions)

## لینک‌های مفید

- [Git Documentation](https://git-scm.com/doc) - Version control system
- [Myers Diff Algorithm](https://en.wikipedia.org/wiki/Diff#Algorithm)
- [Delta Storage Pattern](https://en.wikipedia.org/wiki/Delta_encoding)
- [Version Control Best Practices](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [Database Versioning Strategies](https://martinfowler.com/articles/evodb.html)

---

<div align="center">

[↑ بازگشت به بالا](#document-versioning) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

