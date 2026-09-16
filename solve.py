import re
from pathlib import Path
from urllib.parse import unquote, quote

DRY_RUN = False
ROOT = Path("PortSwigger")

HASH_RE = re.compile(r"\s+[a-f0-9]{20,}$", re.IGNORECASE)


def clean_name(name):
    p = Path(name)
    stem = unquote(p.stem)
    suffix = p.suffix.lower()

    stem = HASH_RE.sub("", stem)
    stem = stem.replace("\u00a0", " ")
    stem = re.sub(r"\s+", " ", stem).strip()
    stem = stem.replace("–", "-").replace("—", "-")

    if not stem:
        stem = "untitled"

    return stem + suffix


def unique_target(base_path, planned):
    target = base_path
    i = 1

    while target.exists() or str(target).lower() in planned:
        target = base_path.with_name(f"{base_path.stem} ({i}){base_path.suffix}")
        i += 1

    planned.add(str(target).lower())
    return target


def rename_items(root):
    items = sorted(root.rglob("*"), key=lambda x: len(x.parts), reverse=True)
    planned = set()

    for old in items:
        new_name = clean_name(old.name)

        if new_name == old.name:
            continue

        new_path = unique_target(old.with_name(new_name), planned)

        print(f"RENAME: {old} -> {new_path}")

        if not DRY_RUN:
            old.rename(new_path)


def clean_md_content(content):
    def fix_link(match):
        text = match.group(1)
        link = match.group(2).strip()

        if link.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        if match.start() > 0 and content[match.start() - 1] == "!":
            return match.group(0)

        decoded = unquote(link)

        if "#" in decoded:
            path_part, anchor = decoded.split("#", 1)
            anchor = "#" + anchor
        else:
            path_part = decoded
            anchor = ""

        parts = path_part.split("/")
        cleaned_parts = []

        for part in parts:
            if part:
                cleaned_parts.append(clean_name(part))

        new_link = "/".join(cleaned_parts) + anchor
        new_link = quote(new_link, safe="/.#-_()")

        return f"[{text}]({new_link})"

    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", fix_link, content)
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip() + "\n"


def clean_md_files(root):
    for md in root.rglob("*.md"):
        print(f"CLEAN MD: {md}")

        if not DRY_RUN:
            try:
                content = md.read_text(encoding="utf-8", errors="ignore")
                md.write_text(clean_md_content(content), encoding="utf-8")
            except Exception as e:
                print(f"ERROR: {md} -> {e}")


def rename_root_md_to_readme():
    if Path("README.md").exists():
        print("README.md already exists, skip.")
        return

    candidates = list(Path(".").glob("*.md"))

    if not candidates:
        print("No root .md file found.")
        return

    chosen = None
    root_name = ROOT.name.lower()

    for md in candidates:
        if clean_name(md.name).lower() == f"{root_name}.md":
            chosen = md
            break

    if chosen is None:
        chosen = candidates[0]

    print(f"RENAME README: {chosen} -> README.md")

    if not DRY_RUN:
        chosen.rename("README.md")


def remove_empty_dirs(root):
    dirs = sorted(
        [p for p in root.rglob("*") if p.is_dir()],
        key=lambda x: len(x.parts),
        reverse=True
    )

    for d in dirs:
        try:
            if not any(d.iterdir()):
                print(f"REMOVE EMPTY DIR: {d}")

                if not DRY_RUN:
                    d.rmdir()
        except Exception as e:
            print(f"ERROR REMOVE: {d} -> {e}")


def check_hash(root):
    print("\n=== Check remaining hash ===")

    found = False

    for item in root.rglob("*"):
        if HASH_RE.search(item.stem):
            print(f"STILL HAS HASH: {item}")
            found = True

    if not found:
        print("OK: No Notion hash found.")


def main():
    if not ROOT.exists():
        print(f"Không tìm thấy thư mục: {ROOT}")
        print("Nếu thư mục gốc không phải PortSwigger, sửa biến ROOT.")
        return

    print("=== Notion Export Cleaner ===")
    print(f"ROOT = {ROOT}")
    print(f"DRY_RUN = {DRY_RUN}")

    print("\n=== Step 1: Rename files/folders ===")
    rename_items(ROOT)

    print("\n=== Step 2: Clean markdown files ===")
    clean_md_files(ROOT)

    print("\n=== Step 3: Rename root md to README.md ===")
    rename_root_md_to_readme()

    print("\n=== Step 4: Remove empty dirs ===")
    remove_empty_dirs(ROOT)

    check_hash(ROOT)

    print("\nDONE")

    if DRY_RUN:
        print("Đang chạy thử. Nếu log ổn, đổi DRY_RUN = False rồi chạy lại.")
    else:
        print("Đã đổi tên thật.")


if __name__ == "__main__":
    main()
