# Document Archive Service

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

آرشیو و مدیریت اسناد، داکیومنت‌ها، نامه‌ها، عکس‌ها و فایل‌ها با قابلیت full-text search و versioning. همچنین استفاده از
Mayan EDMS به عنوان سیستم مدیریت اسناد یکپارچه و اتصال آن به پروژه‌های Java و Frontend.

## قابلیت‌ها

### 1. File Storage

- ذخیره‌سازی فایل‌ها در Object Storage
- پشتیبانی از انواع فایل (PDF, DOCX, Images, etc.)
- Metadata management
- File organization (folders, categories)

### 2. Full-text Search

- Indexing محتوای فایل‌ها
- Search در metadata
- Advanced search queries
- Faceted search

### 3. Document Management

- Categorization و tagging
- Access control
- Document versioning integration
- Document lifecycle management

### 4. Processing

- Thumbnail generation برای images
- Preview generation برای documents
- OCR برای scanned documents
- Metadata extraction

## تکنولوژی‌ها

### Document Management System

- **Mayan EDMS**: سیستم مدیریت اسناد یکپارچه (به عنوان بخشی از Docker container)
    - مدیریت کامل اسناد و فایل‌ها
    - Version control برای اسناد
    - Metadata management
    - Full-text search
    - Document indexing
    - OCR capabilities
    - Document preview
    - Access control و permissions
    - Document types و categories
    - Workflow integration
    - Document check-in/check-out
    - Document approval workflows
    - Audit trail
    - Document retention policies

### Storage

- **Mayan EDMS Storage**: Storage داخلی Mayan EDMS
- **MinIO**: S3-compatible object storage (self-hosted) - برای backup یا alternative storage
- **AWS S3**: Cloud storage - برای backup یا alternative storage
- **Azure Blob Storage**: جایگزین Azure
- **Local File System**: برای development

### Search

- **Mayan EDMS Search**: Full-text search داخلی Mayan EDMS
- **Elasticsearch**: برای full-text search پیشرفته (در صورت نیاز)
- **Apache Solr**: جایگزین Elasticsearch
- **PostgreSQL Full-text Search**: برای simple search

### Processing

- **Mayan EDMS Processing**: OCR و processing داخلی Mayan EDMS
- **Apache Tika**: برای metadata extraction (در صورت نیاز)
- **ImageMagick**: برای image processing (در صورت نیاز)
- **Tesseract OCR**: برای OCR (در صورت نیاز)
- **PDFBox**: برای PDF processing (در صورت نیاز)

## ساختار Service

```
document-archive-service/
├── storage/
│   ├── s3/
│   ├── minio/
│   └── local/
├── search/
│   ├── elasticsearch/
│   └── indexing/
├── processing/
│   ├── thumbnail/
│   ├── preview/
│   └── ocr/
└── metadata/
    ├── extraction/
    └── management/
```

## API Endpoints

### File Operations

- `POST /api/documents/upload` - آپلود فایل
- `GET /api/documents/{id}` - دریافت فایل
- `DELETE /api/documents/{id}` - حذف فایل
- `GET /api/documents/{id}/download` - دانلود فایل

### Search

- `GET /api/documents/search` - جستجوی فایل‌ها
- `GET /api/documents/{id}/content` - محتوای فایل (برای search)

### Metadata

- `GET /api/documents/{id}/metadata` - دریافت metadata
- `PUT /api/documents/{id}/metadata` - به‌روزرسانی metadata
- `POST /api/documents/{id}/tags` - اضافه کردن tag

### Processing

- `GET /api/documents/{id}/thumbnail` - دریافت thumbnail
- `GET /api/documents/{id}/preview` - دریافت preview
- `POST /api/documents/{id}/ocr` - OCR processing

## Document Versioning

Integration با Document Versioning Service:

- هر نسخه جدید به عنوان یک document جدید ذخیره می‌شود
- Link بین versions
- Version history

## Access Control

- Role-based access control (RBAC)
- Permission management
- Audit logging
- Encryption برای sensitive documents

## Configuration

```yaml
document-archive:
  storage:
    type: minio
    minio:
      endpoint: http://localhost:9000
      access-key: ${MINIO_ACCESS_KEY}
      secret-key: ${MINIO_SECRET_KEY}
      bucket: documents
  search:
    elasticsearch:
      hosts: http://localhost:9200
  processing:
    thumbnail:
      enabled: true
      sizes: [100x100, 200x200, 500x500]
    ocr:
      enabled: true
      language: fas,eng
```

## Mayan EDMS Integration

### معماری Integration

```
┌─────────────────────────────────────────┐
│         Docker Compose Network         │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │  Java        │    │  Mayan EDMS  │  │
│  │  Services    │◄──►│  Container   │  │
│  └──────────────┘    └──────────────┘  │
│         │                    │         │
│         │                    │         │
│  ┌──────▼────────────────────▼──────┐  │
│  │      Frontend (React)            │  │
│  └──────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

### Java Integration

```java
@Service
public class MayanEDMSService {
    
    @Autowired
    private RestTemplate restTemplate;
    
    private String mayanEDMSBaseUrl = "http://mayan-edms:8000";
    
    public Document uploadDocument(MultipartFile file, Map<String, String> metadata) {
        // Upload document to Mayan EDMS via REST API
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", file.getResource());
        metadata.forEach(body::add);
        
        HttpEntity<MultiValueMap<String, Object>> requestEntity = 
            new HttpEntity<>(body, headers);
        
        ResponseEntity<Document> response = restTemplate.postForEntity(
            mayanEDMSBaseUrl + "/api/documents/", 
            requestEntity, 
            Document.class
        );
        
        return response.getBody();
    }
    
    public Document getDocument(String documentId) {
        // Get document from Mayan EDMS
        return restTemplate.getForObject(
            mayanEDMSBaseUrl + "/api/documents/" + documentId + "/",
            Document.class
        );
    }
    
    public void deleteDocument(String documentId) {
        // Delete document from Mayan EDMS
        restTemplate.delete(mayanEDMSBaseUrl + "/api/documents/" + documentId + "/");
    }
    
    public List<Document> searchDocuments(String query) {
        // Search documents in Mayan EDMS
        return restTemplate.exchange(
            mayanEDMSBaseUrl + "/api/search/documents/?q=" + query,
            HttpMethod.GET,
            null,
            new ParameterizedTypeReference<List<Document>>() {}
        ).getBody();
    }
}
```

### Frontend Integration

```typescript
// Mayan EDMS API Client
class MayanEDMSClient {
  private baseUrl = 'http://mayan-edms:8000/api';
  
  async uploadDocument(file: File, metadata: Record<string, string>) {
    const formData = new FormData();
    formData.append('file', file);
    Object.entries(metadata).forEach(([key, value]) => {
      formData.append(key, value);
    });
    
    const response = await fetch(`${this.baseUrl}/documents/`, {
      method: 'POST',
      body: formData,
    });
    
    return response.json();
  }
  
  async getDocument(documentId: string) {
    const response = await fetch(`${this.baseUrl}/documents/${documentId}/`);
    return response.json();
  }
  
  async searchDocuments(query: string) {
    const response = await fetch(`${this.baseUrl}/search/documents/?q=${query}`);
    return response.json();
  }
}
```

### Configuration

```yaml
mayan-edms:
  enabled: true
  base-url: http://mayan-edms:8000
  api-token: ${MAYAN_EDMS_API_TOKEN}
  integration:
    java:
      enabled: true
      rest-client: true
    frontend:
      enabled: true
      direct-api: true
```

## Integration با سایر سرویس‌ها

- **Mayan EDMS**:
    - استفاده به عنوان primary Document Management System
    - Integration از طریق REST API
    - Event-driven integration با Kafka برای document events
- **Document Versioning Service**:
    - Integration با Mayan EDMS version control
    - یا استفاده از Mayan EDMS versioning
- **eSignature Service**:
    - Integration با Mayan EDMS برای signed documents
    - ذخیره اسناد امضا شده در Mayan EDMS
- **Report Manager**:
    - Integration با Mayan EDMS برای report attachments
    - ذخیره گزارشات در Mayan EDMS
- **Messaging Service**:
    - Integration با Mayan EDMS برای email attachments
    - ارسال اسناد از Mayan EDMS
- **Schedule & Event Manager**:
    - Integration برای ضمیمه‌های رویدادها

## لینک‌های مفید

### Mayan EDMS

- [Mayan EDMS Official Documentation](https://docs.mayan-edms.com/)
- [Mayan EDMS Installation Guide](https://docs.mayan-edms.com/topics/installation.html)
- [Mayan EDMS REST API Documentation](https://docs.mayan-edms.com/topics/api.html)
- [Mayan EDMS Docker Image](https://hub.docker.com/r/mayanedms/mayanedms)
- [Mayan EDMS GitHub Repository](https://github.com/mayan-edms/mayan-edms)
- [Mayan EDMS API Reference](https://docs.mayan-edms.com/topics/api.html#api-reference)
- [Mayan EDMS User Guide](https://docs.mayan-edms.com/topics/user_guide.html)
- [Mayan EDMS Developer Guide](https://docs.mayan-edms.com/topics/developer_guide.html)

### Object Storage

- [MinIO Documentation](https://min.io/docs/)
- [MinIO Java SDK](https://docs.min.io/docs/java-client-quickstart-guide.html)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS S3 Java SDK](https://docs.aws.amazon.com/sdk-for-java/)
- [Azure Blob Storage Documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/)
- [Object Storage Best Practices](https://www.min.io/resources/docs/Object-Storage-Checklist)

### Search & Indexing

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Elasticsearch Java Client](https://www.elastic.co/guide/en/elasticsearch/client/java-api-client/current/)
- [Apache Solr Documentation](https://solr.apache.org/guide/)
- [PostgreSQL Full-text Search](https://www.postgresql.org/docs/current/textsearch.html)

### Document Processing

- [Apache Tika Documentation](https://tika.apache.org/)
- [Apache Tika Java API](https://tika.apache.org/1.28/api/)
- [ImageMagick Documentation](https://imagemagick.org/script/index.php)
- [ImageMagick Java API](https://imagemagick.org/script/api.php)
- [Tesseract OCR Documentation](https://github.com/tesseract-ocr/tesseract)
- [Tesseract Java Wrapper](https://github.com/nguyenq/tess4j)
- [PDFBox Documentation](https://pdfbox.apache.org/)
- [PDFBox Java API](https://pdfbox.apache.org/docs/2.0.28/javadocs/)

### File Management

- [Spring File Upload](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/multipart.html)
- [Multipart File Handling](https://www.baeldung.com/spring-file-upload)
- [File Storage Best Practices](https://www.baeldung.com/java-file-storage)
- [Content-Type Detection](https://www.baeldung.com/java-file-mime-type)

---

<div align="center">

[↑ بازگشت به بالا](#document-archive-service) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

