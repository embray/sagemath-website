# -*- coding: utf-8 -*-
import copy
import os
from glob import glob

import jinja2
import markdown
import yaml

from lektor.pluginsystem import Plugin


_MARKDOWN = markdown.Markdown()


@jinja2.evalcontextfilter
def filter_markdown(eval_ctx, text):
    if eval_ctx.autoescape:
        return _MARKDOWN.convert(jinja2.escape(text))

    return _MARKDOWN.convert(text)


class SageWebsitePlugin(Plugin):
    name = 'sage-website'
    description = u'Legacy configuration for Sage website'

    _confs = {
        'config': {},
        'packages': {}
    }

    def on_setup_env(self, **extra):
        """Load configs and set up the build environment."""

        conf_dir = os.path.join(self.env.root_path, 'conf')
        for path in glob(os.path.join(conf_dir, '*.yaml')):
            config_name = os.path.splitext(os.path.basename(path))[0]
            with open(path) as fobj:
                data = yaml.load(fobj)

            self._confs[config_name] = data

        # Insert additional Jinja2 globals from config.yaml
        # This is possibly dangerous and in the future should go away.
        self.env.jinja_env.globals.update(self._confs['config'])
        self.env.jinja_env.globals['packages'] = self._confs['packages']
        self.env.jinja_env.globals['spkgs'] = sorted(
                self._confs['packages'].get('spkg', {}).values(),
                key=lambda x: x['name'].lower())

        # Insert a few additional Jinja filters that are used by the old
        # templates
        self.env.jinja_env.filters.update({
            'markdown': filter_markdown
        })

        def existing_template(template, env=self.env.jinja_env):
            try:
                env.loader.get_source(env, template)
            except jinja2.TemplateNotFound:
                return False

            return True

        self.env.jinja_env.tests['existing_template'] = existing_template
