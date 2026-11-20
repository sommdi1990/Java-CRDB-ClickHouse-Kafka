# Enterprise service architecture notes

A Persian design collection examines transactional storage, analytical reporting and inter-service messaging. The repository pairs architectural examples with Python utilities for inspecting container images.

Read the transactional outbox example alongside the ClickHouse manager design to follow the proposed boundary between writes and analytics. The registry lister is executable source. The service descriptions and code fragments in the architecture chapters are design material.

- [Architecture-Transactional-Outbox-Pattern.md](Java-CRDB-ClickHouse-Kafka/Architecture-Transactional-Outbox-Pattern.md)
- [Backend-ClickHouse-Manager.md](Java-CRDB-ClickHouse-Kafka/Backend-ClickHouse-Manager.md)
- [docker_registry_lister.py](scripts/docker_registry_lister.py)

## راهنمای فارسی

فصل‌های معماری، طرح پیشنهادی ثبت تراکنش و انتقال رویداد به بخش گزارش‌گیری را توضیح می‌دهند. برای مرور، مثال polling در فصل Transactional Outbox را کنار فصل ClickHouse Manager بخوانید. اسکریپت‌های Python در پوشهٔ scripts برای بررسی imageها هستند.

## مجوز

در README مبنا مجوز MIT ذکر شده است.
