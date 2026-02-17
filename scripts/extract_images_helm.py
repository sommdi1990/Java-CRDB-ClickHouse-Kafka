import os
import sys
import subprocess
import re

PRIVATE_REGISTRY = "rr.alefba2.ir"


def run_helm_template(chart_file):
    try:
        result = subprocess.run(
            ["helm", "template", chart_file],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("❌ Helm template failed:")
        print(e.stderr)
        sys.exit(1)


def extract_images_from_manifest(manifest):
    images = set()

    # هر خطی که image: داشته باشه
    pattern = re.compile(r'image:\s*"?([^"\s]+)"?')

    matches = pattern.findall(manifest)

    for img in matches:
        img = img.strip()

        # حذف ایمیج بدون tag
        if ":" not in img or img.endswith(":"):
            continue

        images.add(img)

    return images


def generate_script(chart_file, images):
    base_name = os.path.splitext(os.path.basename(chart_file))[0]
    output_file = f"{base_name}.txt"

    with open(output_file, "w", encoding="utf-8") as f:

        f.write("# ===============================\n")
        f.write("# Stage 1: Pull from source registry\n")
        f.write("# ===============================\n\n")

        for img in sorted(images):
            f.write(f"docker pull {img}\n")

        f.write("\n\n# ===============================\n")
        f.write("# Stage 2: Tag for private registry\n")
        f.write("# ===============================\n\n")

        for img in sorted(images):
            f.write(f"docker tag {img} {PRIVATE_REGISTRY}/{img}\n")

        f.write("\n\n# ===============================\n")
        f.write("# Stage 3: Push to private registry\n")
        f.write("# ===============================\n\n")

        for img in sorted(images):
            f.write(f"docker push {PRIVATE_REGISTRY}/{img}\n")

    print(f"\n✅ {len(images)} images extracted from rendered manifest.")
    print(f"📄 Script created: {output_file}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("  python extract_images.py <chart-file.tgz>")
        sys.exit(1)

    chart_file = sys.argv[1]

    if not os.path.exists(chart_file):
        print("❌ File not found.")
        sys.exit(1)

    print("⏳ Running helm template...")
    manifest = run_helm_template(chart_file)

    print("🔎 Extracting images from rendered manifest...")
    images = extract_images_from_manifest(manifest)

    if not images:
        print("⚠ No valid images found.")
        sys.exit(0)

    generate_script(chart_file, images)
