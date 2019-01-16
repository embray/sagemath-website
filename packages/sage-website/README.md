# sage-website

Plugin just for the SageMath website, particularly used for backwards
compatibility with the old site structure.

This reads some YAML-formatted configuration data from under the site's
`conf/` directory, and in particular inserts variables from the
`conf/config.yaml` file into the global context for Jinja templates, and
also performs some other tasks that the old website's `render.py` script
was previously responsible for.
