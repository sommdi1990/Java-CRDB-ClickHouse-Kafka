import sys
import os
import tarfile
import tempfile
import subprocess
import yaml
import re

TARGET_REGISTRY = "rr.alefba2.ir"

def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode, result.stdout, result.stderr

def helm_template(chart_file):
    base_cmd = ["helm", "template", chart_file]

    # بار اول بدون override
    result = subprocess.run(
        base_cmd,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return result.stdout

    print("⚠ Helm template failed. Retrying with fallback values...")

    fallback_sets = [
        ["--set", "certmanager-issuer.email=dummy@example.com"],
        ["--set", "global.hosts.domain=example.com"],
        ["--set", "postgresql.install=false"],
        ["--set", "redis.install=false"],

        # Loki fixes
        ["--set", "deploymentMode=SingleBinary"],
        ["--set", "singleBinary.replicas=1"],
        ["--set", "backend.replicas=0"],
        ["--set", "read.replicas=0"],
        ["--set", "write.replicas=0"],
        ["--set", "loki.storage.type=filesystem"],
        ["--set", "loki.useTestSchema=true"],
    ]

    retry_cmd = base_cmd[:]

    for s in fallback_sets:
        retry_cmd.extend(s)

    retry = subprocess.run(
        retry_cmd,
        capture_output=True,
        text=True
    )

    if retry.returncode == 0:
        return retry.stdout

    print("❌ Helm template failed again:")
    print(retry.stderr)
    sys.exit(1)



def extract_images(rendered_yaml):
    images = set()
    docs = rendered_yaml.split("---")
    for doc in docs:
        try:
            parsed = yaml.safe_load(doc)
            if not parsed:
                continue
            containers = []

            spec = parsed.get("spec", {})
            if "template" in spec:
                spec = spec["template"].get("spec", {})

            containers += spec.get("containers", [])
            containers += spec.get("initContainers", [])

            for c in containers:
                if "image" in c:
                    images.add(c["image"])
        except:
            continue
    return sorted(images)

def normalize_image(image):
    if "@" in image:
        return image

    if ":" not in image.split("/")[-1]:
        image = image + ":latest"

    return image

def generate_commands(images, output_file):
    pulls = []
    tags = []
    pushes = []

    for image in images:
        image = normalize_image(image)
        pulls.append(f"docker pull {image}")

        # split registry if exists
        parts = image.split("/")
        if "." in parts[0] or ":" in parts[0]:
            repo_path = "/".join(parts[1:])
        else:
            repo_path = image

        target_image = f"{TARGET_REGISTRY}/{repo_path}"

        tags.append(f"docker tag {image} {target_image}")
        pushes.append(f"docker push {target_image}")

    with open(output_file, "w") as f:
        f.write("# ==== PULL IMAGES ====\n")
        for p in pulls:
            f.write(p + "\n")

        f.write("\n# ==== TAG IMAGES ====\n")
        for t in tags:
            f.write(t + "\n")

        f.write("\n# ==== PUSH TO INTERNAL REGISTRY ====\n")
        for p in pushes:
            f.write(p + "\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_images_helm.py <chart.tgz>")
        sys.exit(1)

    tgz_path = sys.argv[1]
    if not os.path.isfile(tgz_path):
        print("❌ File not found")
        sys.exit(1)

    print("⏳ Running helm template...")
    rendered = helm_template(tgz_path)

    print("🔎 Extracting images...")
    images = extract_images(rendered)

    if not images:
        print("⚠️ No images found.")
        sys.exit(0)

    base_name = os.path.splitext(os.path.basename(tgz_path))[0]
    output_file = base_name + ".txt"

    generate_commands(images, output_file)

    print(f"✅ Done. Output written to {output_file}")
    print(f"📦 Total images: {len(images)}")

if __name__ == "__main__":
    main()
