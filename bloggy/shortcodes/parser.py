import re

from django.template import Template, Context


def import_parser(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def parse(value):
    ex = re.compile(r'\[(.*?)\]')
    groups = ex.findall(value)
    parsed = value

    for item in groups:
        if ' ' in item:
            name, space, args = item.partition(' ')
            args = __parse_args__(args)
        # If shortcode does not use spaces as a separator, it might use equals
        # signs.
        elif '=' in item:
            name, space, args = item.partition('=')
            args = __parse_args__(args)
        else:
            name = item
            args = {}

        item = re.escape(item)
        id = args.get('v')
        try:
            html = '<div class="article-single-videoWrapper"><iframe width="560" height="315" src="https://www.youtube.com/embed/{{ id }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>'
            template = Template(html)
            context = Context({
                'id': id
            })

            result = template.render(context)
            parsed = re.sub(r'\[' + item + r'\]', result, parsed)
        except ImportError:
            print("Console error while loading module")

    return parsed


def __parse_args__(value):
    ex = re.compile(r'[ ]*(\w+)=([^" ]+|"[^"]*")[ ]*(?: |$)')
    groups = ex.findall(value)
    kwargs = {}

    for group in groups:
        if group.__len__() == 2:
            item_key = group[0]
            item_value = group[1]

            if item_value.startswith('"'):
                if item_value.endswith('"'):
                    item_value = item_value[1:]
                    item_value = item_value[:item_value.__len__() - 1]

            kwargs[item_key] = item_value

    return kwargs
