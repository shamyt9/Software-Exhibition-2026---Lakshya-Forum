#!/usr/bin/env python3
import re

# Read the file
with open('templates/complaints/view.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all multiline url_for calls with single-line versions
# Pattern: <a\s+href="{{ url_for(...) }}" with stuff in between becomes <a href="{{ url_for(...) }}" 

# First, let's find and replace the entire broken actions section
pattern = r'(<div style="padding: 20px">.*?<div style="display: flex; gap: 12px; flex-wrap: wrap">).*?(</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*{% endblock %})'

replacement = r'''\1
                        <a href="{{ url_for('ai.classify', cmp_id=complaint.complaint_id) }}" class="btn-secondary" style="padding: 10px 20px; border: 2px solid #38bdf8; border-radius: 10px; color: #38bdf8; text-decoration: none; font-weight: 600; transition: all 0.2s;">🔄 Re-run AI</a>
                        <a href="{{ url_for('fir.fir_view', cmp_id=complaint.complaint_id) }}" class="btn-primary" style="padding: 10px 20px; background: #3b82f6; color: white; border-radius: 10px; text-decoration: none; font-weight: 600;">📄 Generate FIR</a>
                        {% if current_user.role in ['admin', 'supervisor', 'sp', 'cci', 'io'] and prediction and ('fraud' in prediction.category.lower() or 'financial' in prediction.category.lower()) %}
                        <a href="{{ url_for('freeze.generate_freeze', cmp_id=complaint.complaint_id) }}" class="btn-primary" style="padding: 10px 20px; background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); color: white; border-radius: 10px; text-decoration: none; font-weight: 600; transition: all 0.3s;" title="Generate transaction freeze request for RBI/Bank">❄️ Request Freeze</a>
                        {% endif %}
                        {% if current_user.role in ['admin', 'supervisor'] %}
                        <a href="{{ url_for('assignment.assign', cmp_id=complaint.complaint_id) }}" style="padding: 10px 20px; border: 2px solid #f59e0b; border-radius: 10px; color: #f59e0b; text-decoration: none; font-weight: 600;">👮 Assign Officer</a>
                        {% endif %}
                        {% if current_user.role == 'admin' %}
                        <a href="{{ url_for('complaint.edit_complaint', cmp_id=complaint.complaint_id) }}" style="padding: 10px 20px; border: 2px solid #a78bfa; border-radius: 10px; color: #a78bfa; text-decoration: none; font-weight: 600;">✏️ Edit Complaint</a>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

\2'''

try:
    content_new = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # If the regex replacement worked
    if content_new != content:
        with open('templates/complaints/view.html', 'w', encoding='utf-8') as f:
            f.write(content_new)
        print("✅ Template file fixed successfully!")
    else:
        print("⚠️ Regex pattern didn't match. Trying alternative approach...")
        # Alternative: find the section and replace line by line
        lines = content.split('\n')
        in_actions_section = False
        new_lines = []
        skip_lines = 0
        
        for i, line in enumerate(lines):
            if skip_lines > 0:
                skip_lines -= 1
                continue
                
            if '⚡ ACTIONS' in line:
                in_actions_section = True
                # Add the header
                new_lines.append(line)
                # Skip to find the opening div
                j = i + 1
                while j < len(lines) and '<div style="padding: 20px">' not in lines[j]:
                    new_lines.append(lines[j])
                    j += 1
                
                # Add the fixed actions section
                new_lines.append('                <div style="padding: 20px">')
                new_lines.append('                    <div style="display: flex; gap: 12px; flex-wrap: wrap">')
                new_lines.append('                        <a href="{{ url_for(\'ai.classify\', cmp_id=complaint.complaint_id) }}" class="btn-secondary" style="padding: 10px 20px; border: 2px solid #38bdf8; border-radius: 10px; color: #38bdf8; text-decoration: none; font-weight: 600; transition: all 0.2s;">🔄 Re-run AI</a>')
                new_lines.append('                        <a href="{{ url_for(\'fir.fir_view\', cmp_id=complaint.complaint_id) }}" class="btn-primary" style="padding: 10px 20px; background: #3b82f6; color: white; border-radius: 10px; text-decoration: none; font-weight: 600;">📄 Generate FIR</a>')
                new_lines.append('                        {% if current_user.role in [\'admin\', \'supervisor\', \'sp\', \'cci\', \'io\'] and prediction and (\'fraud\' in prediction.category.lower() or \'financial\' in prediction.category.lower()) %}')
                new_lines.append('                        <a href="{{ url_for(\'freeze.generate_freeze\', cmp_id=complaint.complaint_id) }}" class="btn-primary" style="padding: 10px 20px; background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); color: white; border-radius: 10px; text-decoration: none; font-weight: 600; transition: all 0.3s;" title="Generate transaction freeze request for RBI/Bank">❄️ Request Freeze</a>')
                new_lines.append('                        {% endif %}')
                new_lines.append('                        {% if current_user.role in [\'admin\', \'supervisor\'] %}')
                new_lines.append('                        <a href="{{ url_for(\'assignment.assign\', cmp_id=complaint.complaint_id) }}" style="padding: 10px 20px; border: 2px solid #f59e0b; border-radius: 10px; color: #f59e0b; text-decoration: none; font-weight: 600;">👮 Assign Officer</a>')
                new_lines.append('                        {% endif %}')
                new_lines.append('                        {% if current_user.role == \'admin\' %}')
                new_lines.append('                        <a href="{{ url_for(\'complaint.edit_complaint\', cmp_id=complaint.complaint_id) }}" style="padding: 10px 20px; border: 2px solid #a78bfa; border-radius: 10px; color: #a78bfa; text-decoration: none; font-weight: 600;">✏️ Edit Complaint</a>')
                new_lines.append('                        {% endif %}')
                new_lines.append('                    </div>')
                new_lines.append('                </div>')
                
                # Skip old lines until we find </div></div></div></div></div></div>
                j = j + 1
                depth = 0
                while j < len(lines):
                    if '</div>' in lines[j]:
                        depth += 1
                        if depth >= 6:  # 6 closing divs
                            skip_lines = j - i - 1
                            break
                    j += 1
                in_actions_section = False
            else:
                new_lines.append(line)
        
        with open('templates/complaints/view.html', 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print("✅ Template file fixed with alternative approach!")
        
except Exception as e:
    print(f"❌ Error: {e}")
