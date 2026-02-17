import tarfile
import yaml
import os
import sys

PRIVATE_REGISTRY = "rr.alefba2.ir"


def is_valid_image(image):
    if not image:
        return False
    image = image.strip()
    if ":" not in image:
        return False
    if image.endswith(":"):
        return False
    return True


def normalize_image(image):
    image = image.strip()

    # اگر registry نداشت implicit docker.io هست
    # ولی نیازی نیست docker.io اضافه کنیم
    return image


def extract_images(data, images):
    if isinstance(data, dict):

        # حالت repository + tag
        if "repository" in data:
            repo = data.get("repository")
            tag = data.get("tag")
            if repo and tag:
                img = f"{repo}:{tag}"
                if is_valid_image(img):
                    images.add(normalize_image(img))

        # حالت image: nginx:1.2.3
        if "image" in data and isinstance(data["image"], str):
            img = data["image"]
            if is_valid_image(img):
                images.add(normalize_image(img))

        for value in data.values():
            extract_images(value, images)

    elif isinstance(data, list):
        for item in data:
            extract_images(item, images)


def extract_from_chart(tgz_path):
    images = set()

    with tarfile.open(tgz_path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.name.endswith("values.yaml"):
                f = tar.extractfile(member)
                if f:
                    content = yaml.safe_load(f.read())
                    if content:
                        extract_images(content, images)

    return images


def generate_script(tgz_path, images):
    base_name = os.path.splitext(os.path.basename(tgz_path))[0]
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

    print(f"\n✅ {len(images)} valid images extracted.")
    print(f"📄 Script created: {output_file}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("  python extract_images.py <chart-file.tgz>")
        sys.exit(1)

    tgz_file = sys.argv[1]

    if not os.path.exists(tgz_file):
        print("❌ File not found.")
        sys.exit(1)

    images = extract_from_chart(tgz_file)

    if not images:
        print("⚠ No valid images found.")
        sys.exit(0)

    generate_script(tgz_file, images)
