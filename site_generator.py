import json
import os
from pathlib import Path

import jinja2
import markdown


ARTICLES_FOLDER = 'articles'
TEMPLATES_FOLDER = 'templates'
ARTICLE_TEMPLATE = 'article.html'
INDEX_FILE = 'index.html'
OUTPUT_FOLDER = 'pages'
CONFIG_FILE = 'config.json'


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


def get_html_filepath(article_path, parent_folder=''):
    return (Path(parent_folder) / article_path).with_suffix('.html')  


def init_jinja_environment():
    jinja_environment = jinja2.Environment()
    jinja_environment.loader = jinja2.FileSystemLoader(TEMPLATES_FOLDER)
    return jinja_environment


def render_article_html(template, markdown_text, article_title):
    html_from_markdown = markdown.markdown(markdown_text,
                                           output_format='html5',
                                           extensions=['codehilite',
                                                       'fenced_code'])
    return template.render(title=article_title,
                           index_href=os.path.join('..', INDEX_FILE),
                           content=html_from_markdown)


def render_index_html(template, config):
    return template.render(config=config)


def site_generator():
    config = get_file_content(CONFIG_FILE)
    jinja_environment = init_jinja_environment()
    template = jinja_environment.get_template(ARTICLE_TEMPLATE)
    for article in config['articles']:
        markdown_text = get_file_content(os.path.join(ARTICLES_FOLDER,
                                                      article['source']))
        rendered_html = render_article_html(template, markdown_text,
                                            article['title'])
        html_article_path = get_html_filepath(article['source']
        save_html(rendered_html, html_article_path, OUTPUT_FOLDER))
        article['source'] = html_article_path
    template = jinja_environment.get_template(INDEX_FILE)
    rendered_index_html = render_index_html(template, config)
    save_html(rendered_index_html, get_html_filepath(INDEX_FILE,
                                                     OUTPUT_FOLDER))
    

if __name__ == '__main__':
    site_generator()
    print('Done!')