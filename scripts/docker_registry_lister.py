import requests
import json

def get_registry_images(registry_url, username=None, password=None):
    """
    لیست تمام ایمیج‌ها و تگ‌های آنها را از یک رجیستری داکر دریافت می‌کند.

    Args:
        registry_url (str): آدرس پایه رجیستری (مثال: https://rr.alefba2.ir)
        username (str, optional): نام کاربری برای رجیستری خصوصی.
        password (str, optional): رمز عبور برای رجیستری خصوصی.

    Returns:
        dict: یک دیکشنری ساختار یافته شامل تمام مخازن و تگ‌های آنها.
    """

    # نشست (Session) برای نگهداری کوکی‌ها و تنظیمات بین درخواست‌ها
    session = requests.Session()
    if username and password:
        session.auth = (username, password)

    # 1. دریافت توکن احراز هویت (در صورت نیاز)
    # ابتدا یک درخواست آزمایشی به نقطه پایانی catalog می‌زنیم
    catalog_url = f"{registry_url.rstrip('/')}/v2/_catalog"

    try:
        initial_response = session.get(catalog_url)
        initial_response.raise_for_status()

        # اگر موفق بود (مثلاً رجیستری عمومی)، توکنی لازم نیست
        token = None
        print("احراز هویت اولیه موفقیت‌آمیز بود. (رجیستری ممکن است عمومی باشد یا احراز پیشرفته‌تر نیاز داشته باشد)")

    except requests.exceptions.HTTPError as e:
        if initial_response.status_code == 401:
            # رجیستری نیاز به توکن دارد
            auth_header = initial_response.headers.get('WWW-Authenticate', '')
            print(f"نیاز به احراز هویت تشخیص داده شد. هدر: {auth_header}")

            # استخراج پارامترهای realm، service، و scope از هدر
            # این بخش ساده‌سازی شده است. در عمل ممکن است نیاز به تجزیه پیچیده‌تر رشته باشد.
            # برای اسکوپ کلی رجیستری، معمولاً از scope="registry:catalog:*" استفاده می‌شود.
            import re
            realm_match = re.search('realm="([^"]+)"', auth_header)
            service_match = re.search('service="([^"]+)"', auth_header)

            if realm_match and service_match:
                realm = realm_match.group(1)
                service = service_match.group(1)
                # برای دسترسی به catalog، scope مورد نیاز معمولاً این است:
                scope = "registry:catalog:*"

                # ساخت URL درخواست توکن
                token_url = f"{realm}?service={service}&scope={scope}"
                print(f"دریافت توکن از: {token_url}")

                # درخواست توکن
                # نکته: برخی سرورهای احراز هویت ممکن است از Basic Auth روی خود endpoint توکن استفاده کنند.
                token_response = session.get(token_url)
                token_response.raise_for_status()
                token_data = token_response.json()
                token = token_data.get('token') or token_data.get('access_token')

                if token:
                    print("توکن با موفقیت دریافت شد.")
                    # افزودن توکن به هدرهای نشست برای تمام درخواست‌های بعدی
                    session.headers.update({'Authorization': f'Bearer {token}'})
                else:
                    print("خطا: توکن در پاسخ سرور احراز هویت یافت نشد.")
                    return {}
            else:
                print("خطا: نتوانستم پارامترهای لازم (realm, service) را از هدر WWW-Authenticate استخراج کنم.")
                print("مستندات رجیستری را برای روش احراز هویت خاص آن بررسی کنید.")
                return {}
        else:
            # خطای HTTP دیگری رخ داده
            print(f"خطا در ارتباط با رجیستری: {e}")
            return {}

    # 2. دریافت لیست مخازن (repositories)
    print("\nدر حال دریافت لیست مخازن از رجیستری...")
    all_repos = []
    last_repo = None

    # پشتیبانی از صفحه‌بندی (pagination)
    while True:
        pagination_params = {'n': 100}  # تعداد در هر صفحه
        if last_repo:
            pagination_params['last'] = last_repo

        catalog_response = session.get(catalog_url, params=pagination_params)
        catalog_response.raise_for_status()
        catalog_data = catalog_response.json()

        repos_in_page = catalog_data.get('repositories', [])
        all_repos.extend(repos_in_page)

        # بررسی لینک صفحه بعد (در هدر Link)
        link_header = catalog_response.headers.get('Link', '')
        if 'rel="next"' in link_header:
            # در یک پیاده‌سازی کامل، می‌توان URL صفحه بعد را از هدر استخراج کرد.
            # برای سادگی، اگر تعداد مخازن برگشتی کمتر از درخواست بود، به انتها رسیده‌ایم.
            if len(repos_in_page) < pagination_params['n']:
                break
            last_repo = repos_in_page[-1]
        else:
            break

    print(f"تعداد {len(all_repos)} مخزن پیدا شد.")

    # 3. دریافت تگ‌های هر مخزن
    print("\nدر حال دریافت تگ‌های هر مخزن...")
    result = {}

    for repo in all_repos:
        print(f"  پردازش مخزن: {repo}")
        tags_url = f"{registry_url.rstrip('/')}/v2/{repo}/tags/list"

        try:
            tags_response = session.get(tags_url)
            tags_response.raise_for_status()
            tags_data = tags_response.json()
            repo_tags = tags_data.get('tags', [])
            result[repo] = repo_tags
            print(f"    تعداد {len(repo_tags)} تگ یافت شد.")
        except requests.exceptions.HTTPError as e:
            print(f"    خطا در دریافت تگ‌های {repo}: {e}")
            result[repo] = []  # مخزن بدون تگ یا خطای دسترسی
        except Exception as e:
            print(f"    خطای غیرمنتظره برای {repo}: {e}")
            result[repo] = []

    return result

def save_to_file(data, filename="docker_images_report.json"):
    """داده‌های دریافتی را در یک فایل JSON ذخیره می‌کند."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\nگزارش با موفقیت در فایل '{filename}' ذخیره شد.")

# ---------- بخش اجرای اصلی اسکریپت ----------
if __name__ == "__main__":
    # *** اطلاعات رجیستری خود را اینجا قرار دهید ***
    REGISTRY_URL = "https://rr.alefba2.ir"  # آدرس رجیستری شما
    USERNAME = ""         # نام کاربری (اگر لازم است)
    PASSWORD = ""         # رمز عبور (اگر لازم است)

    # در صورتی که رجیستری عمومی است، USERNAME و PASSWORD را خالی بگذارید
    # USERNAME = None
    # PASSWORD = None

    print(f"اتصال به رجیستری: {REGISTRY_URL}")
    images_data = get_registry_images(REGISTRY_URL, USERNAME, PASSWORD)

    if images_data:
        # نمایش خلاصه در کنسول
        print("\n" + "="*50)
        print("خلاصه گزارش:")
        total_images = len(images_data)
        total_tags = sum(len(tags) for tags in images_data.values())
        print(f"تعداد کل مخازن (ایمیج‌ها): {total_images}")
        print(f"تعداد کل تگ‌های ورژن: {total_tags}")

        for repo, tags in images_data.items():
            if tags:
                print(f"\n  {repo}:")
                # نمایش حداکثر 5 تگ اول برای نمونه
                tags_to_show = tags[:5]
                for tag in tags_to_show:
                    print(f"    - {tag}")
                if len(tags) > 5:
                    print(f"    ... و {len(tags) - 5} تگ دیگر")
            else:
                print(f"\n  {repo}: (بدون تگ)")

        # ذخیره در فایل
        save_to_file(images_data, "docker_registry_inventory.json")
    else:
        print("هیچ داده‌ای دریافت نشد یا خطایی رخ داده است.")



