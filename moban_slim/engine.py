from typing import Dict

from jinja2 import Environment, FileSystemLoader, Template
from moban.externals import file_system
from slimish_jinja import SlimishExtension

from jinja2_fsloader import FSLoader


class EngineSlim(object):
    def __init__(self, template_fs, options: Dict = None):
        self.template_fs = template_fs
        self.jj2_env = Environment(
            loader=FSLoader(template_fs), extensions=[SlimishExtension],
        )
        self.jj2_env.slim_debug = True

    def get_template(self, template_file: str):
        template_file = file_system.to_unicode(template_file)
        template = self.jj2_env.get_template(template_file)
        return template

    def get_template_from_string(self, string: str):
        string = file_system.to_unicode(string)
        return Template(string)

    def apply_template(self, template, data: Dict, _):
        rendered_content = template.render(**data)
        return rendered_content
