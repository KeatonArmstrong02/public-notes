import os
import re
from datetime import datetime

folder = os.path.dirname(__file__)

def get_file_dates(path):
    stat = os.stat(path)
    created = datetime.fromtimestamp(stat.st_ctime)
    modified = datetime.fromtimestamp(stat.st_mtime)
    return created, modified

def has_date_in_frontmatter(content):
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            return re.search(r'^date:', frontmatter, re.MULTILINE) is not None
    return False

def add_frontmatter(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_date_in_frontmatter(content):
        return  # Already has a date

    created, modified = get_file_dates(path)
    created_str = created.strftime('%Y-%m-%d %H:%M')
    modified_str = modified.strftime('%Y-%m-%d %H:%M')

    # If file already has frontmatter, add dates to it
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            new_frontmatter = f"date: {created_str}\nlast_modified: {modified_str}\n" + frontmatter
            new_content = f"---\n{new_frontmatter.strip()}\n---{body}"
        else:
            return
    else:
        # No frontmatter, create it
        new_content = f"---\ndate: {created_str}\nlast_modified: {modified_str}\ndraft: false\n---\n{content}"

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

for filename in os.listdir(folder):
    if filename.endswith('.md'):
        add_frontmatter(os.path.join(folder, filename)) 