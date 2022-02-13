---
_alias: adding-links
---

Adding Links
============

There's not much Spekulatio specific about adding links to your sites: you
can define them as you would normally do in Markdown, reStructuredText or HTML
documents, and you can provide absolute/relative URLs which will be resolved as
expected by the browser. However, Spekulatio provides some help in those cases
where you don't want to hardcode URLs in your site:

* For internal links, you can assign aliases to your pages and refer
  to them using them instead of hardcoding their URL.
* For any link, you can define variables that are defined once and used multiple
  times in your source files.

Link Syntax
-----------

You can add links to your document using the standard syntax according to its
formtat:

_Markdown_

    [Text of the link](http://www.example.com)

_reStructuredText_

    `Text of the link <http://www.example.com>`_.

_HTML_

    <a href="http://www.example.com">Text of the link</a>

And, in the case of Markdown and reStructuredText, you can provide the URLs as
references too:

_Markdown_

    [Text of the link][id]
    ⋮
    [id]: http://www.example.com

_reStructuredText_

    This is the `text of the link`__.
    ⋮
    __ http://www.example.com

!!! Note "reStructuredText Links"

    In the case of reStructuredText, check the [official documentation][rst-links] for more
    possibilities.

    [rst-links]: https://docutils.sourceforge.io/docs/user/rst/quickref.html#hyperlink-targets

!!! Note "HTML in Markdown"

    In Markdown, you can add HTML directly to the document, so consider this
    possibility in case you need to customize the final HTML form of the link.

### Adding Custom Classes to Links

_Markdown_

You can add classes or ids to your links with the following syntax:

    [Text of the link](http://www.example.com){.my-class #my-id}

That example would, for example, be converted to:

    <a id="my-id" class="my-class" href="http://www.example.com">Text of the link</a>

_reStructuredText_

In the case of reStructuredText, there's no direct way to add a class name or id
to a link. However, you can use the `raw` directive to insert HTML in the
document:

    You can click |my-link|.

    .. |my-link| raw:: html

        <a id="my-id" class="my-class" href="http://www.example.com">here</a>

Absolute and relative URLs
--------------------------

URLs of your site will be resolved by the browser, which means that you can
expect the normal behavior no matter if you specify them in their absolute or
relative form. For example, consider the following input directory:

    /
    └── dir1/
        └── foo.md
            dir2/
            └── bar.md

If the domain from which the page will be served is `www.example.com`, you can
create a link inside `foo.md` pointing to `bar.md` in the following ways:

_Full URL_

    [a link](https://www.example.com/dir1/dir2/bar.html)

_Absolute URL_

    [a link](/dir1/dir2/bar.html)

_Relative URL_

    [a link](dir2/bar.html)

Notice that in all cases the target URL refers to the final HTML file `bar.html`
created from `bar.md`.

In general, it may be a good idea to use absolute URLs without the domain name
so you can move the content without changes between domains if necessary.
Relative URLs are also very useful. For example, you can have all the links and
static files inside a section of your site specified as relative, which will
allow you to move the section within the site tree without modification.

!!! Note "Serving your site from a given path"

    If your site is served from a specific path instead of the root of the
    domain, you can define a variable at the root of the site:

        url_prefix: "https://my-domain.org/path-to-serve-from"

    and use it to avoid having to hardcode the domain and path in absolute
    links:
    {%- raw %}

        [Text of the link]({{ url_prefix }}/dir1/dir2/bar.html)

    {%- endraw %}

Aliases
-------

Sometimes you may not want to refer to pages using their paths because if those
change in the future all the links in the site that point to them will be
broken. To avoid that you can set an **alias** (an unique string identifier) to the
page you want to link to, and use that to refer to it.

To define the alias, you only have to set the `_alias` value in the front matter
of the page:
```
---
_alias: configuration
---

Configuration
=============

…
```
And then, to create the link, just use the `get_url()` function:
{%- raw %}
```
More details in the [Configuration]({{ get_url('configuration') }}) section.
```
{%- endraw %}

`get_url()` is one of the available [template functions]({{
get_url('template-functions') }}), and can be used inside any content file
(Markdown, reStructuredText or HTML) or template.

!!! Note

    Make sure the alias of a page is unique across the site to ensure that it
    can be referenced without ambiguity.

Avoid Harcoded URLs with Variables
----------------------------------

Aliases only work for internal links, however, you can use **variables** to
avoid hardcoding URLs in your site for any kind of link. For example, you can
define the following one inside the [_values.yaml]({{
get_url('docs')}}#the-values-yaml-file) file at the root of your file tree:

    some_url: http://www.example.com/path/to/page

and refer to it in your links:
{%- raw %}
```
[a link]({{ some_url }})
```
{%- endraw %}


Pretty URLs
-----------

In Spekulatio, all pages are generated with the `.html` extension. However, the
development server (`spekulatio serve`) supports *pretty* or *clean URLs*. That
means that pages will be served even if the `.html` extension is not provided:

    # these two URLs serve the same content
    /foobar/page.html
    /foobar/page

And also it is not necessary to specify `index.html` to load a directory page:

    # also, these two URLs serve the same content
    /foobar/index.html
    /foobar/

Using pretty URLs in your site doesn't require activating any configuration. It
just depends on how you write your internal links. That is, as long as you write
your internal links using pretty URLs you're already using them.

However, when using pretty URLs take into account the following:

  * Make sure that you use either pretty URLs of the full ones, but don't mix
    both styles. Mixing them can make configuring the HTTP server or the hosting
    service much harder, the URLs will look inconsistent and it may affect your
    site's SEO (Search Engine Optimization).

  * Most static site hosting services (such as Netlify, GitHub Pages or
    Surge.sh) support pretty URLs out of the box without any additional
    configuration. If you deploy your site in them, it should directly work no
    matter which kind of URLs you use in your internal links. For some services,
    it may be necessary to activate a configuration option though.

  * If you plan to serve your site directly using NGINX, Apache or any other
    HTTP server, make sure that the pretty URL configuration is in place.

  * Having two URLs that serve the same content to search engines may hurt your
    site's SEO. This is usually not a problem if you use the same links
    consistently through your site, as the search engines will use the ones they
    find to index the content. However, if you have a mix of link styles or want
    to change from one style to another, then it is very important to define
    with type of URLs are the [canonical ones][wiki-canonical] that you want to
    use and optionally add HTTP redirects (301, 302) to them.

[wiki-canonical]: https://en.wikipedia.org/wiki/Canonical_link_element

