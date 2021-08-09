import os.path

import markdown
from jinja2 import Environment, FileSystemLoader

# Define markdown files and HTML template directories
MD_FILES_PATH = "../../markdown"
HTML_FILES_PATH = "../../posts/"

# Get markdown files in markdown directory
md_directories = []
md_file_paths = []
for filename in os.listdir(MD_FILES_PATH):
    if os.path.isdir(os.path.join(MD_FILES_PATH, filename)):
        md_directories.append(MD_FILES_PATH + "/" + filename)
    elif filename.endswith(".md"):
        md_file_paths.append(MD_FILES_PATH + "/" + filename)

# Get markdown files in markdown subdirectories
for directory in md_directories:
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            md_file_paths.append(directory + "/" + filename)

print("markdown files:", md_file_paths)
print("markdown directories:", md_directories)

# Load Jinja2 Templates
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
markdown_template = env.get_template('post_template.html')
index_post_template = env.get_template('index_post_template.html')
index_template = env.get_template('index_template.html')

# Generate all posts
portfolio_html = ""
for filepath in md_file_paths:
    if not filepath.endswith(".md"):
        continue
    filename = filepath.split("/")[-1]
    html_filepath = HTML_FILES_PATH + filename.replace(".md", ".html")

    with open(filepath, 'r') as f:
        text = f.read()
        md_html = markdown.markdown(text)

    with open(html_filepath, 'w') as f:
        f.write(markdown_template.render(title=filename.replace(".md", "").replace("_", " "), markdown=md_html))

    # Generate portfolio HTML based on posts
    try:
        with open(filepath.replace(".md", ".description"), 'r') as f:
            description = f.read()
    except FileNotFoundError:
        description = ""
    portfolio_html += "\n" + index_post_template.render(href=html_filepath.replace("../", ""),
                                                        post_title=filename.replace(".md", ""),
                                                        post_description=description)

# Generate main website
with open('../../index.html', 'w') as f:
    f.write(index_template.render(portfolio=portfolio_html))
