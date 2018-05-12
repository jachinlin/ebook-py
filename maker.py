# coding=utf8

import os
from jinja2 import Environment, PackageLoader

templates_env = Environment(loader=PackageLoader('maker'))
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')


def render_file(template_name, context, output_name, output_dir):
    template = templates_env.get_template(template_name)
    with open(os.path.join(output_dir, output_name), "w") as f:
        f.write(template.render(**context))


def render_toc_ncx(first_level_post_list):
    render_file('toc.xml', {'first_level_post_list': first_level_post_list}, 'toc.ncx', output_dir)


def render_toc_html(first_level_post_list):
    render_file('toc.html', {'first_level_post_list': first_level_post_list}, 'toc.html', output_dir)


if __name__ == '__main__':
    first_level_post_list = [
        {
            'title': 'a',
            'id': 12,
            'play_order': 2,
            'next_level_post_list': [
                {'title': 'a.1', 'id': 12, 'play_order': 3, },
                {'title': 'a.2', 'id': 12, 'play_order': 4, }
            ]
        },
        {
            'title': 'b',
            'id': 12,
            'play_order': 5,
            'next_level_post_list': [
                {'title': 'b.1', 'id': 12, 'play_order': 6, },
                {'title': 'b.1', 'id': 12, 'play_order': 7, }
            ]
        },
    ]

    render_toc_ncx(first_level_post_list)
    print('test render_toc_ncx pass')

    render_toc_html(first_level_post_list)
    print('test render_toc_html pass')


