# ameeer.in

Minimal personal website for `https://ameeer.in`.

## Edit

Add posts as Markdown files in `content/posts/`:

```md
---
title: My post title
date: 2026-07-04
series: notes
description: Optional search/result description.
---

Write the post here.
```

Run a local build:

```sh
python3 build.py
python3 -m http.server 8000 -d site
```

Open `http://localhost:8000`.

## Publish

The GitHub Actions workflow builds and deploys `site/` to GitHub Pages on every push to `main`.

The GitHub profile link is configured in `build.py`.
