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


def render_opf(first_level_post_list, title):
    render_file('opf.xml', {'first_level_post_list': first_level_post_list}, '{}.opf'.format(title), output_dir)


def parse_headers(toc_file_name):
    headers_info = []

    with open(toc_file_name) as f:
        headers = f.readlines()
        order = 1
        if not headers:
            return None, None
        title_line = 0
        while (not headers[title_line].strip()) or title_line == len(headers):
            title_line += 1

        if title_line == len(headers):
            return None, None

        title = headers[title_line].strip()

        for h in headers[title_line+1:]:
            if h.startswith('# '):
                order += 1
                headers_info.append({
                    'title': h[2:].strip(),
                    'play_order': order,
                    'next_level_post_list': []
                })

            if h.startswith('## '):
                if len(headers) == 0:
                    continue
                order += 1
                headers_info[-1]['next_level_post_list'].append({
                    'title': h[2:].strip(),
                    'play_order': order,
                })

    return title, headers_info


if __name__ == '__main__':
    title, first_level_post_list = parse_headers('./output/toc.md')

    if not title:
        raise ValueError('invalid toc md file')
    print(first_level_post_list)
    render_toc_ncx(first_level_post_list)
    print('test render_toc_ncx pass')

    render_toc_html(first_level_post_list)
    print('test render_toc_html pass')

    render_opf(first_level_post_list, title)
    print('test render_opf pass')
    f = os.path.join(output_dir, title + '.opf')
    print(f)
    os.system("%s %s" % ('/Users/jiaxian/Downloads/KindleGen_Mac_i386_v2_9/kindlegen', f))

