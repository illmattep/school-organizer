from flask import Markup, request, render_template, Flask

class Utils:
    def get_pagination_links(self, current_page, total_pages):
        links = []
        for page in range(1, total_pages + 1):
            if page != current_page:
                links.append('<a href="?page={}">{}</a>'.format(page, page))
            else:
                links.append('<span class="current-page">{}</span>'.format(page))
        return Markup(' '.join(links))