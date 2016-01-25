#!/usr/bin/python
"""Generates `articles/` from written entries in `entries/`."""
import os
import re
import string


# Create target directory if it doesn't already exist.
TARGET_DIR = 'articles/'
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

# Render base templates for articles and homepage.
article_template_str = open("templates/article.template").read()
home_article_str = open("templates/home.template").read()
article_template = string.Template(article_template_str)
home_template = string.Template(home_article_str)

# Generate target directory of published entries.
titles = []
target_dir = 'entries'
entries = os.listdir(target_dir)
for entry in entries:
    with open('entries/' + entry) as f:
        scrubbed_text = re.sub('\n\n+\s+', '\n\n<p>', f.read())
        title = entry.replace('-', ' ').title()
        context = {
            'title': title,
            'content': scrubbed_text,
        }
        generated = article_template.substitute(context)
        with open('articles/' + entry, 'w') as t:
            t.write(generated)
        titles.append((entry, title))
        print "'{}' added.".format(title)

# Put together ToC for homepage.
formatter = "<li><a href='articles/{entry}'>{title}</a>"
contents = [formatter.format(entry=entry, title=title)
            for entry, title in titles]

with open('index.html', 'w') as home:
    entries_list = '\n'.join(contents)
    html = home_template.substitute({'entries': entries_list})
    home.write(html)
