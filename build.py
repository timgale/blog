#!/usr/bin/env python3
"""
Simple blog post builder
Converts Markdown posts to HTML and updates index.html
"""

import os
import re
from datetime import datetime
from pathlib import Path

# Try to import markdown library, fallback to simple converter
try:
    import markdown
    USE_MARKDOWN_LIB = True
except ImportError:
    USE_MARKDOWN_LIB = False
    print("Note: 'markdown' library not found. Using basic converter.")
    print("For better formatting, install: pip3 install markdown\n")


def simple_markdown_to_html(text):
    """Basic Markdown to HTML converter for common patterns"""
    # Convert headers
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    
    # Convert bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # Convert links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    
    # Convert code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    
    # Convert paragraphs (double newline = new paragraph)
    paragraphs = text.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            # Handle lists
            if re.match(r'^\d+\.', p) or p.startswith('- '):
                lines = p.split('\n')
                list_type = 'ol' if re.match(r'^\d+\.', lines[0]) else 'ul'
                items = []
                for line in lines:
                    item = re.sub(r'^[\d\-]+\.\s*|- ', '', line)
                    items.append(f'<li>{item}</li>')
                html_paragraphs.append(f'<{list_type}>{"".join(items)}</{list_type}>')
            else:
                html_paragraphs.append(f'<p>{p}</p>')
        elif p:
            html_paragraphs.append(p)
    
    return '\n'.join(html_paragraphs)


def parse_frontmatter(content):
    """Extract YAML frontmatter from Markdown file"""
    frontmatter = {}
    body = content
    
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            # Parse frontmatter
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            body = parts[2]
    
    return frontmatter, body


def convert_markdown(text):
    """Convert Markdown to HTML using available method"""
    if USE_MARKDOWN_LIB:
        return markdown.markdown(text)
    else:
        return simple_markdown_to_html(text)


def read_posts():
    """Read all Markdown posts from posts/ directory"""
    posts = []
    posts_dir = Path('posts')
    
    if not posts_dir.exists():
        print("No posts/ directory found")
        return posts
    
    for md_file in sorted(posts_dir.glob('*.md'), reverse=True):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, body = parse_frontmatter(content)
        
        post = {
            'title': frontmatter.get('title', 'Untitled'),
            'date': frontmatter.get('date', datetime.now().strftime('%Y-%m-%d')),
            'excerpt': frontmatter.get('excerpt', ''),
            'content': convert_markdown(body),
            'filename': md_file.stem
        }
        posts.append(post)
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts


def generate_blog_html(posts):
    """Generate HTML for blog posts section"""
    html = []
    
    for post in posts:
        # Format date nicely
        try:
            date_obj = datetime.strptime(post['date'], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
            iso_date = post['date']
        except:
            formatted_date = post['date']
            iso_date = post['date']
        
        post_html = f'''
                <article class="blog-post">
                    <h3>{post['title']}</h3>
                    <time datetime="{iso_date}">{formatted_date}</time>
                    <div class="post-content">
                        {post['content']}
                    </div>
                </article>
'''
        html.append(post_html)
    
    return '\n'.join(html)


def update_index_html(posts_html):
    """Update index.html with generated blog posts"""
    index_file = Path('index.html')
    
    if not index_file.exists():
        print("Error: index.html not found")
        return False
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the blog section and replace posts
    # Look for the pattern between <h2>Recent Posts</h2> or <h2>Recent Blog Posts</h2> and </div> (closing container)
    pattern = r'(<h2>Recent (?:Blog )?Posts</h2>\s*)(.*?)(\s*</div>\s*</section>)'
    
    replacement = r'\1' + '\n' + posts_html + r'\3'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def main():
    print("Building blog posts...\n")
    
    # Read all posts
    posts = read_posts()
    print(f"Found {len(posts)} post(s)")
    
    if not posts:
        print("No posts to process")
        return
    
    for post in posts:
        print(f"  - {post['title']} ({post['date']})")
    
    # Generate HTML
    posts_html = generate_blog_html(posts)
    
    # Update index.html
    if update_index_html(posts_html):
        print("\n✓ Successfully updated index.html")
        print("Your blog is ready to view!")
    else:
        print("\n✗ Failed to update index.html")


if __name__ == '__main__':
    main()
