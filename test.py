import mistune

# Initialize the Markdown renderer
markdown_renderer = mistune.create_markdown()

# Dynamic content
content = "# Generated Markdown Document\n\nThis is a paragraph.\n\n"
content += "- Item 1\n- Item 2\n\n"
content += "Here is some `inline code`."

# Render Markdown to HTML
html = markdown_renderer(content)
print(html)