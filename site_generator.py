import json
import os
from pathlib import Path
import sys

import jinja2
import markdown

DEFAULT_ARTICLES_FOLDER = 'articles'
TEMPLATE_HTML = os.path.join('templates', 'template.html')
CONFIG_FILE = 'config.json'



def get_articles_folder_path():
    input_folder = input("Enter a folder's name/path"
                         'or press "Enter" to use default "articles": ')
    return input_folder if input_folder else DEFAULT_ARTICLES_FOLDER


def get_all_filepaths(articles_folder):
    all_filepaths = []
    for path, subdirs, files in os.walk(articles_folder):
        for name in files:
            if name.lower().endswith('.md'):
                relative_path = os.path.relpath(os.path.join(path, name),
                                              articles_folder)
                absolute_filepath = os.path.join(path, name)
                all_filepaths.append((absolute_filepath,relative_path,))
    return all_filepaths


def get_html_filepath(relative_path ,articles_folder_path):
    articles_folder_path_object = Path(articles_folder_path)
    html_articles_path = articles_folder_path_object.with_name(
        'html_' + articles_folder_path_object.name)
    return html_articles_path / Path(relative_path).with_suffix('.html')  


def get_file_content(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, encoding="utf-8") as opened_file:
        if not filepath.endswith('.json'):
            return opened_file.read()
        else:
            return json.load(opened_file)

def save_html(html, filepath):
    filepath.parents[0].mkdir(exist_ok=True, parents=True)
    with filepath.open("w", encoding="utf-8") as html_file:
        html_file.write(html)


def site_generator():
    config = get_file_content(CONFIG_FILE)
    articles_folder_path = get_articles_folder_path()
    absolute_and_relative_filepaths = get_all_filepaths(
        articles_folder_path)
    for filepath in absolute_and_relative_filepaths:
        markdown_text = get_file_content(filepath[0])
        html_content_from_markdown = markdown.markdown(markdown_text,
                                                       output_format='html5')
        rendered_html = jinja2.Template(html_content_from_markdown).render(
            content=html_content_from_markdown)
        save_html(rendered_html, get_html_filepath(filepath[1],
                                                   articles_folder_path))


if __name__ == '__main__':
    site_generator()
