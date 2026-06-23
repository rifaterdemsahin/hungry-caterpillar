import re
import json

def parse_vtt(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Remove all the internal timestamp tags like <00:00:02.600><c>
    content = re.sub(r'<[^>]+>', '', content)
    
    blocks = content.split('\n\n')
    entries = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 2 and '-->' in lines[0]:
            time_range = lines[0].split(' align:')[0].strip()
            text_lines = []
            for line in lines[1:]:
                # Ignore lines that are just spaces or single chars, unless it's text
                if line.strip():
                    text_lines.append(line.strip())
            
            text = ' '.join(text_lines).strip()
            if text:
                entries.append({'time': time_range, 'text': text})
    
    # deduplicate adjacent identical text
    dedup = []
    for entry in entries:
        if not dedup or dedup[-1]['text'] != entry['text']:
            dedup.append(entry)
        else:
            # Update end time
            start = dedup[-1]['time'].split(' --> ')[0]
            end = entry['time'].split(' --> ')[1] if ' --> ' in entry['time'] else entry['time']
            dedup[-1]['time'] = f"{start} --> {end}"

    # further cleanup overlapping phrases
    final = []
    for e in dedup:
        # if the new text starts with the old text, we might want to replace or ignore, but it's okay for now
        # simple cleaning
        if e['text'] != '[Music]':
             final.append(e)
        else:
             final.append(e)
             
    with open('transcript.json', 'w') as f:
        json.dump(final, f, indent=2)

if __name__ == '__main__':
    parse_vtt('The Very Hungry Caterpillar - Official Animated Film ｜ Made For Kids ｜ Eric Carle Book [75NQK-Sm1YY].en.vtt')
