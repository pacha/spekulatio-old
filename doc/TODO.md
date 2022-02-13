
* Fix tests
* Update templates of the spekulatio theme so they use node.title, node.content and node.toc
* Make `spekulatio serve` read configuration file
* Make `spekulatio serve` use Flask and have pretty URLs
* Add syntax highlighting to code snippets (pygments)
* Finish documentation
* Write README.md
* Fix sidebar so the `directories_as_titles` value is not needed in the built-in theme

Text:
```
For example, imagine that we assign different actions to Markdown files to the
directories `foo` and `bar` of the following project:

    my-project/
    ├── foo/
    │   └── page.md
    └── bar/
        └── page.md

Let's say that in `foo`, we convert Markdown files to HTML but in `bar`, we just
copy them to the output directory without transformation. In that case, the
resulting output directory would be:

    build/
    ├── page.html
    └── page.md

with `page.html` coming from `foo` and `page.md` coming from `bar`.

Assigning different set of actions to different directories is the mechanism
that allows you to use Markdown, reStructuredText, HTML, YAML or JSON files as
input to templates to generate HTML pages or to copy them to the final site
without modification, for example.
```

