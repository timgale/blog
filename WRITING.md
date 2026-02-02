# Writing Blog Posts

## Quick Start

1. Create a new Markdown file in the `posts/` folder
2. Add frontmatter (title, date, excerpt)
3. Write your post in Markdown
4. Run `python3 build.py` to convert and update the site
5. View at http://localhost:8000

## Post Format

Each post should have frontmatter at the top:

```markdown
---
title: Your Post Title
date: 2026-02-01
excerpt: A short summary of your post that appears in the listing
---

# Your Post Title

Your content here...
```

## Markdown Syntax

```markdown
# Heading 1
## Heading 2
### Heading 3

**bold text**
*italic text*

[link text](https://example.com)

- Bullet list
- Another item

1. Numbered list
2. Another item

`inline code`
```

## Workflow

### Create a new post
```bash
cd ~/Sites/blog
touch posts/my-new-post.md
# Edit the file with your content
```

### Build and view
```bash
python3 build.py  # Converts posts to HTML
blog              # Start the server
```

### Deploy
```bash
git add .
git commit -m "Add new post"
git push
```

## Tips

- Keep filenames lowercase with dashes (e.g., `my-post.md`)
- Posts are sorted by date (newest first)
- The excerpt shows in the post listing
- For better Markdown formatting, install: `pip3 install markdown`
