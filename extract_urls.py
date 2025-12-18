import re
from urllib import request, error
from pathlib import Path


LINKTRE_PREFIX = "https://www.linktre.cc/siteDetails/"


def fetch_real_url(linktre_url: str) -> str | None:
    """Fetch a linktre.cc detail page and extract the real target URL."""
    try:
        with request.urlopen(linktre_url, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] 请求失败: {linktre_url} -> {e}")
        return None

    # 尝试匹配 window.open('...') / window.open("...")
    patterns = [
        r"onclick\s*=\s*\"[^\"]*window\.open\('([^']+)'\)\"",
        r"onclick\s*=\s*\"[^\"]*window\.open\\\(&quot;([^&]+)&quot;\\\)\"",
        r"window\.open\('([^']+)'\)",
        r"window\.open\(\"([^\"]+)\"\)",
    ]

    for pat in patterns:
        m = re.search(pat, html)
        if m:
            real = m.group(1)
            # 一些页面可能给的是相对路径或带空格，简单清洗一下
            real = real.strip()
            if real:
                return real

    print(f"[WARN] 未在页面中找到 window.open: {linktre_url}")
    return None


def build_url_map(text: str) -> dict[str, str]:
    """从文件内容中找出所有 linktre.cc 详情页，构造映射表。"""
    urls = sorted(set(re.findall(r"https://www\\.linktre\\.cc/siteDetails/\\d+", text)))
    print(f"发现 {len(urls)} 个 linktre.cc URL")

    mapping: dict[str, str] = {}
    for i, u in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 解析 {u} ...")
        real = fetch_real_url(u)
        if real:
            mapping[u] = real
            print(f"  -> {real}")
        else:
            print("  -> 未解析到真实地址，跳过")

    print(f"\n成功解析 {len(mapping)} 个 URL")
    return mapping


def apply_mapping(text: str, mapping: dict[str, str]) -> str:
    """用真实 URL 替换文本中的 linktre.cc URL。"""
    for old, new in mapping.items():
        text = text.replace(old, new)
    return text


def main() -> None:
    root = Path(__file__).resolve().parent
    src = root / "links.yml"
    dst = root / "links_resolved.yml"

    if not src.exists():
        raise SystemExit(f"未找到文件: {src}")

    original = src.read_text(encoding="utf-8")

    mapping = build_url_map(original)
    resolved = apply_mapping(original, mapping)

    dst.write_text(resolved, encoding="utf-8")

    print(f"\n已生成替换后的文件: {dst}")
    print("请确认无误后，再手动用它覆盖原来的 links.yml。")


if __name__ == "__main__":
    main()


