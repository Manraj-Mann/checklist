import os
from bs4 import BeautifulSoup

# Create a directory named "list" in the current working directory if it doesn't exist
output_directory = "list"
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# List all HTML files in the parent directory (../)
parent_directory = "../"
html_files = [file for file in os.listdir(parent_directory) if file.endswith(".html")]

# Iterate through each HTML file
for html_file_name in html_files:
    # Read HTML content from the HTML file
    with open(os.path.join(parent_directory, html_file_name), 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize Markdown content
    markdown_content = ''

    # Find the major heading and description
    header = soup.find('header')
    major_heading = header.find('h1', class_='title').text.strip()
    description = header.find_all('p', class_='text_small')[-1].text.strip()

    # Add the major heading to the Markdown content
    markdown_content += f"# {major_heading}\n\n"
    markdown_content += f"{description}\n\n"

    # Find all the sections with class "checklist"
    sections = soup.find_all('section', class_='checklist')

    # Initialize section counter
    section_counter = 1

    # Iterate through each section
    for section in sections:
        # Get the section title
        section_title = section.find('h2', class_='checklist__title').text.strip()

        # Add an extra newline before each major section (except the first one)
        if section_counter > 1:
            markdown_content += '\n'

        # Underline the section title with '=' characters
        section_title_markdown = f"**{section_title}**\n{'=' * len(section_title)}\n"

        # Find all checklist items within the section
        checklist_items = section.find_all('li', class_='checklist-item')

        # Initialize a Markdown list for this section
        markdown_content += section_title_markdown

        # Initialize item counter for numbering
        item_counter = 1

        # Iterate through each checklist item
        for item in checklist_items:
            # Get the checklist item title (bold)
            item_title = item.find('span', class_='checklist-item__title').text.strip()

            # Get the checklist item description with links
            item_description = item.find('div', class_='info').text.strip()

            # Find all links within the description and replace them with Markdown links
            for link in item.find_all('a'):
                item_description = item_description.replace(
                    link.text,
                    f"[{link.text}]({link['href']})"
                )

            # Combine the title and description (with links) into a single Markdown item
            item_markdown = f"{item_counter}. **{item_title}**<br>  {item_description}\n"

            # Increment the item counter
            item_counter += 1

            # Append the item to the section's Markdown content
            markdown_content += item_markdown

        # Increment the section counter
        section_counter += 1

    # Write the Markdown content to a file in the "list" directory with the same name as the HTML file
    markdown_file_name = os.path.splitext(html_file_name)[0] + ".md"
    with open(os.path.join(output_directory, markdown_file_name), 'w', encoding='utf-8') as markdown_file:
        markdown_file.write(markdown_content)

    print(f"Conversion from {html_file_name} to Markdown is complete. Saved to 'list/{markdown_file_name}'.")

print("All conversions are complete.")