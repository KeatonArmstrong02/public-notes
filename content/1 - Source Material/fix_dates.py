import os
import re

folder = os.path.dirname(__file__)
date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})$', re.MULTILINE)

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find date in body (anywhere)
    match = date_pattern.search(content)
    if not match:
        return  # No date found, skip
    date_str = f"{match.group(1)} {match.group(2)}"
    # Remove the date line from the body
    content_wo_date = date_pattern.sub('', content, count=1).lstrip('\n')

    # Check for YAML frontmatter
    if content_wo_date.startswith('---'):
        parts = content_wo_date.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            # Update or add date in frontmatter
            if re.search(r'^date:', frontmatter, re.MULTILINE):
                frontmatter = re.sub(r'^(date:).*$', f'date: {date_str}', frontmatter, flags=re.MULTILINE)
            else:
                frontmatter = f"date: {date_str}\n" + frontmatter
            new_content = f"---\n{frontmatter.strip()}\n---{body}"
        else:
            # Malformed YAML, skip
            return
    else:
        # No YAML frontmatter, create it
        new_content = f"---\ndate: {date_str}\ndraft: false\n---\n{content_wo_date}"

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

for filename in os.listdir(folder):
    if filename.endswith('.md'):
        process_file(os.path.join(folder, filename)) 