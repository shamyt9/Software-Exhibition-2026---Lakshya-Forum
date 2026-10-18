#!/usr/bin/env python3
"""Fix all Jinja2 multi-line statement issues in template"""

with open('templates/complaints/view.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this line has an opening Jinja2 tag but no closing tag
    if ('{%' in line or '{{' in line) and not (line.count('{%') == line.count('%}') or line.count('{{') == line.count('}}')):
        # Find the closing tag
        consolidated = line.rstrip('\n')
        i += 1
        
        while i < len(lines):
            next_line = lines[i]
            # Add the next line, collapsing whitespace
            consolidated += ' ' + next_line.strip()
            
            # Check if we have found the closing tag now
            if consolidated.count('{%') == consolidated.count('%}') or consolidated.count('{{') == consolidated.count('}}'):
                break
            
            i += 1
        
        output.append(consolidated + '\n')
    else:
        output.append(line)
    
    i += 1

with open('templates/complaints/view.html', 'w', encoding='utf-8') as f:
    f.writelines(output)

print("✅ Template fixed!")
