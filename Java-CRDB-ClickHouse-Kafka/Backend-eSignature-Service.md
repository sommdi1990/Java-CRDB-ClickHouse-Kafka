# eSignature Service

<div align="right">

[← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

---

## هدف

امضای دیجیتال اسناد و نامه‌ها با قابلیت audit trail و validation.

## قابلیت‌ها

### 1. Digital Signing

- امضای دیجیتال با certificate
- Multiple signers support
- Signing workflow
- Signature placement

### 2. Integration با سرویس‌های eSignature

- **DocuSign API**: Cloud-based eSignature
- **Adobe Sign API**: Adobe eSignature service
- **HelloSign API**: جایگزین open-source
- **Self-hosted**: استفاده از iText برای PDF signing

### 3. Validation و Verification

- Signature validation
- Certificate verification
- Document integrity check
- Timestamp verification

### 4. Audit Trail

- Complete audit log
- Signing history
- User actions tracking
- Compliance reporting

## تکنولوژی‌ها

### Cloud Services

- **DocuSign API**: Enterprise eSignature
- **Adobe Sign API**: Adobe solution
- **HelloSign API**: Open-source alternative

### Self-hosted

- **iText**: PDF library برای signing
- **Bouncy Castle**: Cryptographic library
- **Java Cryptography Extension (JCE)**: برای certificate management

## ساختار Service

```
esignature-service/
├── provider/
│   ├── docusign/
│   ├── adobe-sign/
│   └── itext/
├── certificate/
│   ├── management/
│   └── validation/
├── workflow/
│   ├── signing/
│   └── approval/
└── audit/
    └── trail/
```

## API Endpoints

### Signing

- `POST /api/esignature/sign` - ایجاد درخواست امضا
- `POST /api/esignature/sign/{id}/sign` - امضای document
- `GET /api/esignature/sign/{id}/status` - بررسی وضعیت

### Validation

- `POST /api/esignature/validate` - اعتبارسنجی امضا
- `GET /api/esignature/document/{id}/signatures` - لیست امضاها

### Audit

- `GET /api/esignature/audit/{documentId}` - Audit trail
- `GET /api/esignature/history/{userId}` - تاریخچه امضاهای کاربر

## Integration با DocuSign

```java
@Configuration
public class DocuSignConfig {
    @Value("${docusign.api.key}")
    private String apiKey;
    
    @Value("${docusign.base.url}")
    private String baseUrl;
    
    @Bean
    public DocuSignClient docuSignClient() {
        return new DocuSignClient(apiKey, baseUrl);
    }
}
```

## Self-hosted Signing با iText

```java
public class PdfSigner {
    public byte[] signPdf(byte[] pdfBytes, Certificate certificate, 
                          PrivateKey privateKey) {
        // Sign PDF using iText
        // Add signature field
        // Apply digital signature
    }
}
```

## Workflow

1. **Document Upload**: آپلود document برای امضا
2. **Signer Assignment**: تخصیص signerها
3. **Signing Request**: ارسال درخواست امضا
4. **Signing**: امضای document
5. **Completion**: تکمیل و validation
6. **Storage**: ذخیره signed document

## Security

- Certificate management
- Private key protection
- Encryption
- Secure storage
- Compliance (eIDAS, etc.)

## Configuration

```yaml
esignature:
  provider: docusign
  docusign:
    api-key: ${DOCUSIGN_API_KEY}
    base-url: https://demo.docusign.net
    account-id: ${DOCUSIGN_ACCOUNT_ID}
  self-hosted:
    certificate-store: classpath:keystore.jks
    certificate-password: ${CERT_PASSWORD}
```

## Integration با سایر سرویس‌ها

- Integration با Document Archive Service (برای signed documents)
- Integration با Messaging Service (برای email notifications)
- Integration با WorkFlow Service (برای signing workflows)
- Integration با Document Versioning Service (برای versioned signatures)

## لینک‌های مفید

- [DocuSign API Documentation](https://developers.docusign.com/)
- [Adobe Sign API Documentation](https://developer.adobe.com/document-services/apis/sign/)
- [HelloSign API Documentation](https://app.hellosign.com/api/documentation)
- [iText Documentation](https://itextpdf.com/en/resources/guides/itext-7)
- [Bouncy Castle Documentation](https://www.bouncycastle.org/documentation.html)
- [Digital Signature Standards](https://csrc.nist.gov/publications/detail/sp/800-106/final)
- [eIDAS Regulation](https://digital-strategy.ec.europa.eu/en/policies/eidas-regulation)

---

<div align="center">

[↑ بازگشت به بالا](#esignature-service) | [← بازگشت به Backend](Backend-Home) | [← صفحه اصلی](Backend-Home)

</div>

