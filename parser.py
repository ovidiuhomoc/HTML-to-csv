import os

from bs4 import BeautifulSoup


def parse(table_html: str):
    soup = BeautifulSoup(table_html, 'html.parser')


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), 'rsrc', 'table.html'), 'r') as f:
        html_parent_component = f.read()
    parse(html_parent_component)
