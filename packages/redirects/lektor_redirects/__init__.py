# -*- coding: utf-8 -*-
import os
import posixpath

import pkg_resources

from lektor.build_programs import BuildProgram
from lektor.db import Page
from lektor.pluginsystem import Plugin
from lektor.sourceobj import VirtualSourceObject
from lektor.utils import build_url

# I feel like this is not the simplest way to do this but it was the best I
# could find from following the examples of other plugins; the docs were not
# as much help as I'd have liked...

# TODO: Ensure that none of the redirects conflict with an existing artifact's
# URL

class RedirectPage(VirtualSourceObject):
    def __init__(self, parent, path):
        super(RedirectPage, self).__init__(parent)
        self._path = path

    @property
    def path(self):
        if self._path.startswith('/'):
            return self._path

        # Not an absolute path; make it relative to the parent's path
        return posixpath.join(posixpath.dirname(parent.path), self._path)

    @property
    def url_path(self):
        if self._path.startswith('/'):
            return self._path

        return build_url([posixpath.dirname(self.parent.url_path), self._path])


class RedirectPageBuildProgram(BuildProgram):
    template_path = 'lektor_redirects.html'

    def produce_artifacts(self):
        self.declare_artifact(self.source.url_path,
                              sources=[self.source.source_filename])

    def build_artifact(self, artifact):
        artifact.render_template_into(self.template_path, this=self.source)


class RedirectsPlugin(Plugin):
    name = 'Redirects'
    description = u'Generate one or more redirects to a page.'

    def on_setup_env(self, **extra):
        self.env.generator(self.generate_redirects)
        self.env.add_build_program(RedirectPage, RedirectPageBuildProgram)
        self.env.jinja_env.loader.searchpath.append(
                pkg_resources.resource_filename('lektor_redirects',
                                                'templates'))

    @staticmethod
    def generate_redirects(source):
        """Generate redirect virtual sources for a given page."""

        if isinstance(source, Page) and 'redirects' in source:
            for redirect in source['redirects']:
                yield RedirectPage(source, redirect)
