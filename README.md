
Spekulatio
==========

Spekulatio is a very simple and flexible static site generator. It takes a
folder of content files, which can be written using RestructuredText, Markdown,
JSON or YAML, and a folder of HTML templates, and generates a site by combining
them.

For example, if you pass the following file structure:
```
templates/
    a-page-layout.html
    another-page-layout.html
    static/
        script.js
        styles.css

content/
    index.rst
    about/
        image.png
        me.rst
    articles/
        article-1.rst
        article-2.rst
    some-records/
        record-1.yml
        record-2.yml
        record-3.yml
```

The generated site will look like:
```
build/
    index.html
    about/
        image.png
        me.html
    articles/
        article-1.html
        article-2.html
    some-records/
        record-1.html
        record-2.html
        record-3.html
    static/
        script.js
        styles.css
```

During the generation process, each content file (`.rst`, `.md`, `.json`,
`.yaml`) is converted into a dictionary of key/value pairs that is passed to
one of the templates to generate the corresponding HTML file. You can define
which templates to use per project, folder and file.

Any other file in the _content_ folder will be copied over to the _build_
folder without modification. That means that you can add images, style sheet files,
JavaScript files or any other type of static files and include them directly in your
site.

Features
--------

In a nutshell, Spekulatio supports:

* RestructuredText, Markdown, JSON, YAML as formats for the content files.

* [Jinja2](http://jinja.pocoo.org/docs/2.10/templates/) syntax for template files.

* Rebuilding only modified files to speed up site generation.

* Automatic [SCSS](https://sass-lang.com/) compilation into CSS.


Why Spekulatio
--------------

There are plenty of great static site generators out there. Some popular ones
are:

* [Sphinx](https://github.com/sphinx-doc/sphinx)
* [Hugo](https://github.com/gohugoio/hugo)
* [Jekyll](https://github.com/jekyll/jekyll)
* [Pelican](https://github.com/getpelican/pelican)
* [Lektor](https://github.com/lektor/lektor)

... and many, many more.

Some of them have large sets of options with many pages of documentation, and
some of them are specialized in a particular kind of site (blog, CMS, project
documentation site). Also some of them are based in a particular JavaScript
technology such as React or Vue.js.

Spekulatio is just agnostic about, well, everything...

* It requires very little to learn. Spekulatio is very small and based around a
  very simple concept: when you pass a content folder, some files
  (RestructuredText, JSON and YAML) are converted to HTML and the rest of them
  are just copied over. So, basically, all the documentation you need to learn
  how to use the tool is this single page.

* It is not intended for any kind of site in particular. It has no notion of
  _posts_, _authors_ or _categories_. It is up to you to define which
  information you want to have defined in each page and that is passed to the
  template to render the final page. Creating a blog or a documentation site is
  all the same from the point of view of the tool.

* It's up to you to include this or that JavaScript or CSS framework, or none!
  Since you write the HTML, you decide.

Not having a predefined set of metadata comes with a downside. Spekulatio
doesn't have a concept of reusable _themes_ and it is mainly intended for people
that want to create their own, custom HTML for their project and that don't want
to necessarily adapt their HTML to the conventions of the site generator tool.

Installation
------------

Spekulatio requires Python 3.6.

To install it you can use the Python package manager:
```
pip3 install git+https://github.com/pacha/spekulatio.git#egg=spekulatio
```

**Note:** If you are installing the tool at the system level you may need to run
pip with `sudo`.

Creating a site
---------------

This is an example of how to create a minimal site using Spekulatio.

First, create the following project structure:
```
my-project/
    build/
    content/
        index.rst
    templates/
        page.html
```

Use this as the contents of `index.rst`:
```
---
_template: "page.html"
author: "Me"
date: "March 10th, 2019"
---

My title
========

My content.
```
At the top of the file, you can specify the metadata that you want to associate
to this document using what is popularly known as *front-matter*. That is, a
YAML snipped enclosed between three-dashes lines. Keys that start with an
underscore have an special meaning in Spekulatio and are used to configure how
the site will be generated. In this case, `_template` just indicates which
template file to use to generate the HTML associated to this restructured text
file.

For the `page.html` template, you can use:
```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <section id="content">
            {{ node.content }}
        </section>
        <section id="author">
            Page created by {{ node.data.author }} on {{ node.data.date }}.
        </section>
    </body>
</html>
```

This template file is used to generate the file `index.html` out of
`index.rst` and Spekulatio passes a single object to it: ``node``.

A node represents the page you're rendering at that moment in the content tree
and it allows you to access the particular content of the page within the
template:

* `node.content`: is the content of the RestructuredText file converted to HTML.

* `node.data`: is a dictionary with the metadata passed as front-matter (eg.
  you can access a key `foo` with `node.data.foo`). Since metadata is very
  frequently accessed from the template, there's a shortcut `data` passed to the
  template too pointing to the data dictionary (ie. `data.foo` is the same as
  `node.data.foo`).

Actually, nodes represent both directories and pages of your content tree, and
you can navigate through them using the following properties:

* `node.parent`: parent node of the current one being rendered.

* `node.children`: for a directory node, all children nodes

* `node.next`: next node (breadth-first order)

* `node.prev`: previous node (breadth-first order)

* `node.root`: root node of the content tree

Accessing other nodes can be useful to build menus or breadcrumb links.

Now, we're ready to generate our site using the following command:
```
my-project$ spekulatio
```

Since we only have one input file (`index.rst`), only one output HTML file will
be generated:
```
my-project/
    build/
        index.html
```

Now you can open this file directly in your browser or run a small web server
with:
```
my-project$ python3 -m http.server --directory ./build
```

And open your new site at: `http://localhost:8000/`

This example uses a single RestructuredText file as content. In the case of JSON
or YAML files the procedure is even simpler since the whole content of the files
is considered metadata and passed as a dictionary to the templates.

### Project and folder data (Underscore content files)

Sometimes you may want to provide data that is share across multiple pages. For
instance, you may want to use the same template across all the files in a
subdirectory. Editing all the pages one by one to add the same `_template` value
can be cumbersome, and there's a more generic way to do it.

Spekulatio has a particular type of content files just to solve this problem. If
you create a content file by prepending an underscore to its name, two things
will happen:

* That content file will not generate any HTML associated to it.

* The metadata defined in it will be shared by all the content files that are in
  the same directory or in subdirectories of that directory.

For example, consider the structure:
```
my-project/
    content/
        foo.rst
        directory-1/
            _values.json
            bar.rst
            directory-2/
                baz.rst
```

In this case, `_values.json` will not generate the output file
`directory-1/_values.html` and the data defined inside it will be used when
`bar.rst` or `baz.rst` are rendered (but not in the case of `foo.rst` since it
is located outside `directory-1/`.

So, if `_values.json` has:
```
{
    "_template": "special-layout.html",
    "poweredby": "Spekulatio"
}
```
both `bar.rst` and `baz.rst` will be rendered with the `special-layout.html`
template.

The name or the type of underscore files doesn't really matter for the process.
It is only the underscore that triggers them being treated in a special manner.
You can use any of the content types (`.rst`, `.json` or `.yaml`) to define
them, and you can call them `_values.xxx` or use any other name that makes
sense in the context of the project. You can even use several of them in the
same folder too. (If you have several underscore files in the same directory
they will be processed in alphabetical order).

The values provided by a underscore content file have less priority than the
ones that are provided in the files themselves. That means that if `baz.rst`
content is:
```
---
_template: normal-layout.html
---

My title
========

My content.
```
the final data dictionary that will be used to generate the HTML will be:
```JavaScript
{
    "_template": "normal-layout.html",
    "poweredby": "Spekulatio",
}
```

The same applies for two underscore files at different levels. Here:
```
my-project/
    content/
        _foo.json
        directory-1/
            _bar.json
            page.rst
```
The values of `_foo.json` have less precedence than `_bar.json`. And `page.rst`
will inherit the values from `_foo.json`, then from `_bar.json` and finally use
their own in order of increasing priority.

Underscore content files are a very flexible mechanism to configure your
project. For example:

* You can place a underscore file at the root of the project for values that are
  global to the project, like `author` or `copyright`.

* You can use underscore files to set the template to use in different
  directories. For example you can have a folder with blog posts using a
  template and another folder "pages" using a different one.

* And you can always set exceptions by overriding values in the normal content
  files themselves.

### JSON and YAML content files

You can use JSON and YAML as content files, however, only ones that contain a
top level object are allowed (that is, the top level element can't be a list,
since it can't be converted directly into a dictionary).

For example, both this JSON file:
```JavaScript
{
    "_template": "page.html",
    "author": "Me",
    "date": "March 10th, 2019"
}
```
and this YAML file:
```yaml
_template: "page.html"
author: "Me"
date: "March 10th, 2019"
```
will render the same result. The dictionary data generated out of them is passed
untouched to the template, which in this case could reference `{{ data.author }}` or
`{{ data.date }}` freely.


### Template files

Template files are written using the
[Jinja2](http://jinja.pocoo.org/docs/2.10/templates/) syntax.

To create the templates you can use any of the features provided by Jinja2 such
as template inheritance, control structures (for loops or if statements) or
filters.

To know which template to use in each case:

* Spekulatio checks for the key `_template` in the metadata of each input file.

* If the key is present and a template of that name exists in the _templates_
  folder provided by the user, then the HTML is generated using the data of the
  content file. If a template of that name doesn't exist then an error is
  raised.

* If the `_template` key is not present, then the default `layout.html` name is
  used. If a template with that name is present in the _templates_ folder of
  the user, then that template is used. If not, then Spekulatio will use a
  default template that just creates an HTML listing all the data entries of
  the content file.

### Static files

Any file that is not a content file is considered by Spekulatio a _static_ file.

Static files are just copied over to the _build_ directory without
transformation but keeping their relative path with respect to the one in their
original directory.

That means that you can add any image, style sheet or JavaScript file to your
project. Spekulatio doesn't really mind too much about the file types, so be
aware that if you add any unrelated file, anywhere in your project _content_
folder, it will still be copied to the _build_ folder regardless of its type.

For example, the following structure:
```
my-project/
    content/
        static/
            foo.png
```

will generate:
```
my-project/
    build/
        static/
            foo.png
```

One important thing is that static files are copied over both the _templates_
and the _content_ folders. That means that you can have static files that are
directly used in your templates together with them and add static files that are
referenced from your content files together with the content files.

For example:
```
my-project/
    templates/
        my-template.html
        static/
            script.js
            styles.css

    content/
        static/
            foo.png
        directory-1/
            page.rst
            directory-2/
                baz.png
```

will generate:
```
my-project/
    build/
        static/
            script.js
            styles.css
            foo.png
        directory-1/
            page.html
            directory-2/
                baz.png
```

Note that:

* Paths are merged. So if you have a `static/` directory in the _templates_
  folder **and** in the _content_ folder. You'll end up with a single `static/`
  directory in the output.

* Content static files have preference over template static files. That is, if
  you have a static file with the same path in both the _templates_ folder and
  the _content_ one, the content one will overwrite the one from _templates_.
  (This allows you to override some aspects of the templates folder in case you
  want to reuse it for several projects).

* Static files can be placed anywhere in the file tree, having them or not in a
  `static/` folder is just a matter of preference of the site creator.

To reference static files from the template or content files, just use absolute
paths from the site root (note the starting slash `/`):
```html
    <img src="/static/foo.png">
```

Or relative paths from the location of the content file. For instance, in the
`page.rst` file or the previous example, you could reference `baz.png` as (note
the missing slash at the beginning):
```
.. image:: directory-2/baz.jpg
```

#### Adding HTML as static files

One peculiarity of the static file handling in Spekulatio is that in the
_templates_ folder any type other than HTML is considered static, while in the
_content_ folder that is the case for any file other than RestructuredText, JSON
or YAML.

That means that if you place HTML files in your _content_ folder, they will be
copied to the _build_ folder untouched. This is useful when you don't want
to generate some HTML pages of your site out of content files but you want to
provide the final HTML to be used in the site yourself. (You can also do this by
adding the HTML file to the _templates_ folder and adding a dummy content file
without any data other than `_template` pointing to that HTML).

In the same way, if you add JSON or YAML files to the _templates_ folder, they
will be copied as they are to the _build_ folder.

#### SCSS support

Most static files are just copied over the _build_ directory. An exception to
this rule is [Sass](https://sass-lang.com/) files with the SCSS syntax.

Spekulatio offers compiling support for this CSS extension. Therefore, when it
finds a `.scss` file, instead of just copying it, it compiles it and saves the
`.css` result to the _build_ directory.

That means that, if you want to reference a `.scss` file from your templates,
you have to use the `.css` filename directly in the HTML.

For example, the input structure:
```
my-project/
    content/
        static/
            foo.scss
```
will generate:
```
my-project/
    build/
        static/
            foo.css
```

And any template using that style sheet can reference it like:
```html
<link rel="stylesheet" href="/static/foo.css">
```

## Command line reference

Spekulatio provides a single command:
```
Usage: spekulatio [OPTIONS]

  Create static site from content files using a set of HTML templates.

Options:
  --build-dir TEXT     Directory for output files (default: ./build).
  --content-dir TEXT   Directory for content files (default: ./content).
  --template-dir TEXT  Directory for HTML templates (default: ./templates).
  --verbose            Show processing messages.
  --help               Show this message and exit.
```

Basically, you just have to pass where are your content files (`content-dir`),
your template files (`template-dir`) and where you want your site to be
generated (`build-dir`).

However if you set your project structure so that the default names are used:
```
my-project/
    build/
    content/
    templates/
```

Then to generate the site, you only have to run the command without passing any options:
```
my-project$ spekulatio
```

Spekulatio keeps track of timestamps of generated files and only recreates those
pages for which the original content file was modified. However, if you change
your templates, you may want to force the recreation of all output files to be able to
see the changes. You can do so with the option: `--no-cache`.

Once your site is generated you'll have all the output HTML files in the
`build/` directory (or the one you have specified). To check your site, you can
serve it locally with:
```
my-project$ python3 -m http.server --directory ./build
```
Then you should be able to browse your site at: `http://localhost:8000`.

*Note:* You can also just directly open the HTML files in your browser from the
file system. However, be aware that, in this case, any URL that is written as an
absolute path from the root of the site (eg. `/static/my-image.png`) will not
work.

