import re
from urllib import request, error
from pathlib import Path

LINKTRE_PREFIX = "https://www.linktre.cc/siteDetails/"


from typing import Dict, Optional


def fetch_real_url(linktre_url: str) -> Optional[str]:
    """访问 linktre.cc 详情页，解析按钮 onclick 里的 window.open 真实地址。"""
    try:
        with request.urlopen(linktre_url, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] 请求失败: {linktre_url} -> {e}")
        return None

    # 先定位按钮所在的 div: class="col-md-4 siteDetails-btn"
    div_match = re.search(
        r'<div[^>]*class="[^"]*col-md-4\s+siteDetails-btn[^"]*"[^>]*>(.*?)</div>',
        html,
        flags=re.S,
    )
    if not div_match:
        print(f"[WARN] 未找到 siteDetails 按钮区域: {linktre_url}")
        return None

    div_html = div_match.group(1)

    # 在该 div 里寻找 button 的 onclick 上的 window.open(...)
    # 示例：<button ... onclick="window.open('https://xxx.com', '_blank')">
    btn_match = re.search(
        r'onclick\s*=\s*"[^"]*window\.open\(\s*[\'"]([^\'"]+)[\'"]',
        div_html,
    )
    if not btn_match:
        btn_match = re.search(
            r"onclick\s*=\s*'[^']*window\.open\(\s*[\"']([^\"']+)[\"']",
            div_html,
        )

    if btn_match:
        url = btn_match.group(1).strip()
        if url:
            return url

    print(f"[WARN] 未在页面中找到 window.open: {linktre_url}")
    return None


def build_url_map(text: str) -> Dict[str, str]:
    """从文件内容中找出所有 linktre.cc 详情页，构造映射表。"""
    # 注意：这里是正则表达式语法，不要把反斜杠写成字面量
    # 匹配形如: https://www.linktre.cc/siteDetails/442
    urls = sorted(set(re.findall(r"https://www\.linktre\.cc/siteDetails/\d+", text)))
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


def apply_mapping(text: str, mapping: Dict[str, str]) -> str:
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


