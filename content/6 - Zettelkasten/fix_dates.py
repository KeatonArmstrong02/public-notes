import os
import re

folder = os.path.dirname(__file__)
date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})$', re.MULTILINE)

for filename in os.listdir(folder):
    if filename.endswith('.md'):
        path = os.path.join(folder, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
            else:
                continue
        else:
            continue

        # Find date in body (at the start, before tags)
        match = date_pattern.search(body)
        if match:
            date_str = f"{match.group(1)}T{match.group(2)}:00"
            # Remove the date line from the body
            body = date_pattern.sub('', body, count=1).lstrip('\n')
            # Update or add date in frontmatter
            if re.search(r'^date:', frontmatter, re.MULTILINE):
                frontmatter = re.sub(r'^(date:).*$', f'date: {date_str}', frontmatter, flags=re.MULTILINE)
            else:
                frontmatter = f"date: {date_str}\n" + frontmatter
            # Reassemble file
            new_content = f"---\n{frontmatter.strip()}\n---{body}"
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content) 