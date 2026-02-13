import argparse
import sys
import os
import json
from collections import OrderedDict

try:
    import yaml
except ImportError:
    print("Error: PyYAML is not installed. Please run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

NEW_REGISTRY = "rr.alefba2.ir"

def extract_images_from_k8s_object(obj, images_dict):
    """استخراج تمام فیلدهای image از دیکشنری و ذخیره به‌عنوان کلید در دیکشنری"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'image' and isinstance(value, str):
                images_dict[value.strip()] = None   # ذخیره به‌عنوان کلید
            else:
                extract_images_from_k8s_object(value, images_dict)
    elif isinstance(obj, list):
        for item in obj:
            extract_images_from_k8s_object(item, images_dict)

def load_documents(file_path):
    """بارگذاری فایل YAML/JSON و برگرداندن لیست داکیومنت‌ها"""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if ext in ['.json']:
            data = json.loads(content)
            return [data] if isinstance(data, dict) else data
        else:
            return list(yaml.safe_load_all(content))

def strip_registry(image):
    """حذف رجیستری صریح از ابتدای ایمیج"""
    if '/' not in image:
        return image
    first, rest = image.split('/', 1)
    if any(c in first for c in ['.', ':']) or first == 'localhost':
        return rest
    return image

def build_target_image(source):
    """ساخت ایمیج جدید با رجیستری مقصد"""
    stripped = strip_registry(source)
    return f"{NEW_REGISTRY}/{stripped}"

def main():
    parser = argparse.ArgumentParser(description='استخراج دستورات docker pull/tag/push از manifest کوبرنتیز')
    parser.add_argument('input_file', help='مسیر فایل YAML/JSON ورودی')
    parser.add_argument('-o', '--output', help='مسیر فایل خروجی (اختیاری)')
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"خطا: فایل {args.input_file} یافت نشد.", file=sys.stderr)
        sys.exit(1)

    if args.output is None:
        base = os.path.splitext(args.input_file)[0]
        args.output = base + '.txt'

    try:
        docs = load_documents(args.input_file)
    except Exception as e:
        print(f"خطا در خواندن فایل: {e}", file=sys.stderr)
        sys.exit(1)

    images = OrderedDict()
    for doc in docs:
        if isinstance(doc, dict):
            extract_images_from_k8s_object(doc, images)

    if not images:
        print("هیچ ایمیجی یافت نشد.", file=sys.stderr)
        sys.exit(0)

    # ساخت نگاشت منبع -> مقصد
    source_to_target = {img: build_target_image(img) for img in images.keys()}

    # بخش اول: دستورات pull
    pull_commands = [f"docker pull {img}" for img in source_to_target.keys()]

    # بخش دوم: دستورات tag
    tag_commands = [f"docker tag {src} {tgt}" for src, tgt in source_to_target.items()]

    # بخش سوم: دستورات push
    push_commands = [f"docker push {tgt}" for tgt in source_to_target.values()]

    # ترکیب با خطوط خالی
    output_lines = "\n".join(pull_commands) + "\n\n" + \
                   "\n".join(tag_commands) + "\n\n" + \
                   "\n".join(push_commands) + "\n"

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_lines)

    print(f"فایل خروجی با {len(images)} ایمیج منحصربه‌فرد در '{args.output}' ذخیره شد.")

if __name__ == '__main__':
    main()