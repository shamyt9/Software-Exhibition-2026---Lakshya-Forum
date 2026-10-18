#!/usr/bin/env python3
"""
Sophisticated template fixer that properly consolidates broken HTML and Jinja2
"""

import re

def fix_template_comprehensive(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strategy: Line-by-line consolidation of broken structures
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for line that ends with unclosed tag
        if line.rstrip().endswith(('"{', '"{', '>"{', '>"{')) or (
            line.rstrip() and not line.rstrip().endswith('>') and 
            (line.count('<') > line.count('>')) and not line.strip().startswith('#')
        ):
            # Likely a broken HTML tag, consolidate with next lines
            consolidated = line.rstrip()
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line:
                    i += 1
                    continue
                
                consolidated += ' ' + next_line
                
                # Check if tag is now complete
                if consolidated.count('<') <= consolidated.count('>'):
                    break
                
                i += 1
            
            result.append(consolidated)
        elif line.strip() == '>':
            # Lone closing bracket - attach to previous line
            if result:
                result[-1] = result[-1].rstrip() + '>'
            i += 1
        else:
            result.append(line)
            i += 1
    
    # Join and fix any remaining issues
    fixed_content = '\n'.join(result)
    
    # Remove extra spaces before >
    fixed_content = re.sub(r'\s+>', '>', fixed_content)
    
    # Consolidate multi-line Jinja2 if blocks
    fixed_content = re.sub(r'{%\s+if\s+([^}]+)\n\s+%}', r'{% if \1 %}', fixed_content)
    fixed_content = re.sub(r'{%\s+elif\s+([^}]+)\n\s+%}', r'{% elif \1 %}', fixed_content)
    fixed_content = re.sub(r'{%\s+else\s+%}\n', r'{% else %}', fixed_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ Template comprehensive fix applied!")

fix_template_comprehensive('templates/complaints/view.html')
