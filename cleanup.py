"""
Look for unused stuff in the dissertation project.
"""

# Parse all .tex files in all subdirectories of the current directory, and combine them into a single file.
import os

latex_text = ''
for root, dirs, files in os.walk('.'):
    for filename in files:
        if not filename.endswith('.tex'):
            continue
        filepath = os.path.join(root, filename)
        with open(filepath, 'r') as f:
            latex_text += f.read()

print(f'Read {len(latex_text)} characters of LaTeX text.')
print(f'Rough word count: {len(latex_text.split())}')

# Look for all citations (\cite{...}) in the text.
import re

citations = re.findall(r'\\cite\{[^\}]+\}', latex_text)

# Split multiple citations into individual citations.
citations = [citation[6:-1] for citation in citations]
citations = [citation.split(',') for citation in citations]
citations = [citation.strip() for citation_list in citations for citation in citation_list]
citations = set(citations)
print(f'Found {len(citations)} unique citations: {citations}')

# Parse the bibliography.bib file and remove all citations that are not used.
with open('bibliography.bib', 'r') as f:
    bib_text = f.read()

bib_entries = re.findall(r'@[^\{]+\{[^\,]+\,', bib_text)
bib_entries = [entry[1:-1] for entry in bib_entries]
bib_entries = [entry.split(',') for entry in bib_entries]
bib_entries = [entry[0].strip() for entry in bib_entries]
bib_entries = [entry.split('{')[1] for entry in bib_entries]
bib_entries = set(bib_entries)
print(f'Found {len(bib_entries)} unique bibliography entries: {bib_entries}')

unused_citations = citations - bib_entries
print(f'Found {len(unused_citations)} unused citations: {unused_citations}')

# Look for images that are not used.
for root, dirs, files in os.walk('.'):
    for filename in files:
        image_formats = ['.png', '.jpg', '.pdf', '.jpeg', '.svg']
        for image_format in image_formats:
            if filename.endswith(image_format):
                break
        else:
            continue
        
        if filename not in latex_text:
            print(f'Found unused image: {filename}')

        # Check if the image is bigger than 1MB. In this case it should be optimized.
        filepath = os.path.join(root, filename)
        if os.path.getsize(filepath) > 1000 * 1000:
            print(f'Image {filename} is bigger than 1MB ({os.path.getsize(filepath) / 1_000_000} MB).')
        