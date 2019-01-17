# Redirects

Generate redirects to pages from their old locations.

The page's model should have a `redirects` field of type `strings` listing
one or more paths, either absolute or relative to the page's URL, to which
redirect pages should be generated.

The included template `lektor_redirects.html` is used to generate the
redirects page.  In the future this could be overridden I suppose.
