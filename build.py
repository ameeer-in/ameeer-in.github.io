#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import html
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
POSTS = CONTENT / "posts"
SITE = ROOT / "site"

SITE_TITLE = "ameer's website"
SITE_TAGLINE = "writing, mostly about technology"
SITE_URL = "https://ameeer.in"
LINKEDIN_URL = "https://www.linkedin.com/in/ameerraja/"
GITHUB_URL = "https://github.com/ameeer-in"


def clean_site() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)


def read_page(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text.strip()

    _, front_matter, body = text.split("---\n", 2)
    data: dict[str, str] = {}

    for line in front_matter.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")

    return data, body.strip()


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def display_date(value: dt.date) -> str:
    return value.strftime("%b '%y")


def slug_from_path(path: Path) -> str:
    name = path.stem
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)


def escape_attr(value: str) -> str:
    return html.escape(value, quote=True)


def inline_markup(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def markdown_to_html(markdown: str) -> str:
    blocks: list[str] = []
    paragraph: list[str] = []
    lines = markdown.splitlines()
    i = 0

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append(f"<p>{inline_markup(' '.join(paragraph))}</p>")
            paragraph.clear()

    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith("```"):
            flush_paragraph()
            language = line.removeprefix("```").strip()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code = html.escape("\n".join(code_lines))
            class_name = f' class="language-{escape_attr(language)}"' if language else ""
            blocks.append(f"<pre><code{class_name}>{code}</code></pre>")
            i += 1
            continue

        if not line.strip():
            flush_paragraph()
            i += 1
            continue

        image = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line.strip())
        if image:
            flush_paragraph()
            alt, src = image.groups()
            blocks.append(f'<p><img src="{escape_attr(src)}" alt="{html.escape(alt)}"></p>')
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            blocks.append(f"<h{level}>{inline_markup(heading.group(2))}</h{level}>")
            i += 1
            continue

        if re.match(r"^\s*[-*]\s+", line):
            flush_paragraph()
            items: list[str] = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i]).strip()
                items.append(f"<li>{inline_markup(item)}</li>")
                i += 1
            blocks.append("<ul>\n" + "\n".join(items) + "\n</ul>")
            continue

        if line.startswith("> "):
            flush_paragraph()
            quotes: list[str] = []
            while i < len(lines) and lines[i].startswith("> "):
                quotes.append(lines[i][2:].strip())
                i += 1
            blocks.append(f"<blockquote><p>{inline_markup(' '.join(quotes))}</p></blockquote>")
            continue

        paragraph.append(line.strip())
        i += 1

    flush_paragraph()
    return "\n".join(blocks)


def render_base(page_title: str, content: str, description: str = "") -> str:
    title = SITE_TITLE if page_title == SITE_TITLE else f"{page_title} | {SITE_TITLE}"
    description = description or SITE_TAGLINE
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape_attr(description)}">
  <title>{html.escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&family=Marcellus&family=Quattrocento+Sans:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
<header>
  <h1><a class="site-title" href="/">{html.escape(SITE_TITLE)}</a></h1>
  <p>{html.escape(SITE_TAGLINE)}</p>
</header>
<main class="page-content" aria-label="Content">
{content}
</main>
</body>
</html>
"""


def write_page(path: Path, html_text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")


def load_posts() -> list[dict[str, object]]:
    posts: list[dict[str, object]] = []

    for path in sorted(POSTS.glob("*.md")):
        data, body = read_page(path)
        date = parse_date(data["date"])
        slug = data.get("slug") or slug_from_path(path)
        title = data["title"]
        description = data.get("description", "")
        series = data.get("series", "")
        post = {
            "title": title,
            "date": date,
            "date_text": display_date(date),
            "slug": slug,
            "url": f"/posts/{slug}/",
            "series": series,
            "description": description,
            "body": markdown_to_html(body),
        }
        posts.append(post)

    posts.sort(key=lambda item: item["date"], reverse=True)
    return posts


def post_list(posts: list[dict[str, object]], include_archive: bool = True) -> str:
    rows = [
        '<li class="post-list-item">',
        '  <span class="post-list-date list-header">date</span>',
        '  <span class="post-list-link list-header">link</span>',
        '  <span class="post-list-series list-header">series</span>',
        "</li>",
    ]

    for post in posts:
        series = f"({html.escape(str(post['series']))})" if post["series"] else ""
        rows.extend(
            [
                '<li class="post-list-item">',
                f'  <span class="post-list-date">{html.escape(str(post["date_text"]))}</span>',
                f'  <a class="post-list-link" href="{escape_attr(str(post["url"]))}">{html.escape(str(post["title"]))}</a>',
                f'  <span class="post-list-series">{series}</span>',
                "</li>",
            ]
        )

    if include_archive:
        rows.extend(
            [
                '<li class="post-list-item archive-row">',
                '  <span class="post-list-date"></span>',
                '  <a class="post-list-link" href="/posts/">archive...</a>',
                '  <span class="post-list-series"></span>',
                "</li>",
            ]
        )

    return '<ul id="post-list">\n' + "\n".join(rows) + "\n</ul>"


def render_index(posts: list[dict[str, object]]) -> None:
    content = "\n".join(
        [
            '<p><a href="/about/">about</a></p>',
            post_list(posts[:5], include_archive=True),
        ]
    )
    write_page(SITE / "index.html", render_base(SITE_TITLE, content))


def render_archive(posts: list[dict[str, object]]) -> None:
    content = "\n".join(
        [
            '<a href="/">&lt;&lt;&lt;</a>',
            "<article>",
            '<p class="post-meta">all posts</p>',
            "<h1>archive</h1>",
            post_list(posts, include_archive=False),
            "</article>",
        ]
    )
    write_page(SITE / "posts" / "index.html", render_base("archive", content, "All posts"))


def render_posts(posts: list[dict[str, object]]) -> None:
    for post in posts:
        published = post["date"]
        assert isinstance(published, dt.date)
        content = "\n".join(
            [
                '<a href="/">&lt;&lt;&lt;</a>',
                "<article>",
                '<p class="post-meta">',
                f'  <time datetime="{published.isoformat()}">{html.escape(str(post["date_text"]))}</time>',
                "</p>",
                f"<h1>{html.escape(str(post['title']))}</h1>",
                str(post["body"]),
                "</article>",
            ]
        )
        path = SITE / "posts" / str(post["slug"]) / "index.html"
        write_page(path, render_base(str(post["title"]), content, str(post["description"])))


def render_about() -> None:
    data, body = read_page(CONTENT / "about.md")
    date = parse_date(data["date"])
    body = body.replace("{{LINKEDIN_URL}}", LINKEDIN_URL)
    body = body.replace("{{GITHUB_URL}}", GITHUB_URL)
    content = "\n".join(
        [
            '<a href="/">&lt;&lt;&lt;</a>',
            "<article>",
            '<p class="post-meta">',
            f'  <time datetime="{date.isoformat()}">{display_date(date)}</time>',
            "</p>",
            "<h1>about</h1>",
            markdown_to_html(body),
            "</article>",
        ]
    )
    write_page(SITE / "about" / "index.html", render_base("about", content, data.get("description", "")))


def copy_assets() -> None:
    shutil.copytree(ROOT / "assets", SITE / "assets", dirs_exist_ok=True)
    shutil.copyfile(ROOT / "CNAME", SITE / "CNAME")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    clean_site()
    posts = load_posts()
    render_index(posts)
    render_archive(posts)
    render_posts(posts)
    render_about()
    copy_assets()
    print(f"Built {SITE}")


if __name__ == "__main__":
    main()
