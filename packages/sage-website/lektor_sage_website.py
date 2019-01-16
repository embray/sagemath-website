# -*- coding: utf-8 -*-
import copy
import os
from glob import glob

import jinja2
import markdown
import yaml

from lektor.pluginsystem import Plugin


@jinja2.contextfilter
def filter_prefix(ctx, link):
    """
    Prepend level-times "../" to the given string.

    Used to go up in the directory hierarchy.  Yes, one could also do absolute
    paths, but then it is harder to debug locally!
    """

    level = ctx.get('level', 0)
    if level == 0:
        return link
    path = ['..'] * level
    path.append(link)
    return '/'.join(path)


_MARKDOWN = markdown.Markdown()

@jinja2.evalcontextfilter
def filter_markdown(eval_ctx, text):
    if eval_ctx.autoescape:
        return _MARKDOWN.convert(jinja2.escape(text))

    return _MARKDOWN.convert(text)


class SageWebsitePlugin(Plugin):
    name = 'sage-website'
    description = u'Legacy configuration for Sage website'

    _confs = {'config': {}}

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

        # Insert a few additional Jinja filters that are used by the old
        # templates
        self.env.jinja_env.filters.update({
            'prefix': filter_prefix,
            'markdown': filter_markdown
        })
