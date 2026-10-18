#!/usr/bin/env python3
"""Comprehensively fix all template formatting issues"""

with open('templates/complaints/view.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove all unnecessary line breaks within HTML/Jinja2 tags
import re

# Fix 1: Consolidate closing > that appear on their own line
content = re.sub(r'\s*\n\s*>', '>', content)

# Fix 2: Remove extra spaces before > in HTML tags
content = re.sub(r'\s+>', '>', content)

# Fix 3: Consolidate multi-line Jinja2 expressions
# This regex finds opening {% or {{ and consolidates until closing %} or }}
def consolidate_jinja2(content):
    """Consolidate multi-line Jinja2 expressions"""
    lines = content.split('\n')
    output = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Count opening and closing tags on this line
        open_tags = line.count('{%') + line.count('{{')
        close_tags = line.count('%}') + line.count('}}')
        
        if open_tags > close_tags:
            # Incomplete tag, consolidate
            consolidated = line
            i += 1
            while i < len(lines):
                next_line = lines[i]
                # Collapse whitespace and add to consolidated line
                consolidated += ' ' + next_line.strip()
                
                open_tags += next_line.count('{%') + next_line.count('{{')
                close_tags += next_line.count('%}') + next_line.count('}}')
                
                if open_tags <= close_tags:
                    break
                i += 1
            output.append(consolidated)
        else:
            output.append(line)
        
        i += 1
    
    return '\n'.join(output)

content = consolidate_jinja2(content)

with open('templates/complaints/view.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Template completely fixed!")
