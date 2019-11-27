import os

from jinja2 import Environment, FileSystemLoader

from helpers import format_percentage, remove_negative_from_zero_number, remove_zero_fractional
from src.tinkoff_invest import get_yesterday_market_result

root = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(root, 'template')
env = Environment(loader=FileSystemLoader(template_dir))
env.filters['remove_negative_from_zero_number'] = remove_negative_from_zero_number
env.filters['remove_zero_fractional'] = remove_zero_fractional
env.filters['format_percentage'] = format_percentage
template = env.get_template('index.html')

file_name = os.path.join(root, 'index.html')
with open(file_name, 'w') as html_file:
    html_file.write(template.render(get_yesterday_market_result('RUB')))
