
Documentation
=============

This page will walk you through creating static websites using Spekulatio. All
the main topics you need to know are present here; however, you can also use the
links at the right as reference for more advanced topics.

If you don't have Spekulatio installed in your system yet, you can also check
out the [Download](/download.html) section for information on how to install it.

The basics
----------

The essence of Spekulatio is very simple: you provide one or more **input
directories** and the tool generates one **output directory** containing your
site by applying actions to each one of the source files.

In this example, you can see how a site is generated inside the `build` directory
by converting each one of the files in `content`:

{# Example content directory being converted #}
<div class="three-part-example">
  <img src="/static/img/docs/one-dir-input.png" alt="Spekulatio input directory example">
  <img src="/static/img/arrows/right.png" class="arrow arrow-right" alt="arrow right">
  <img src="/static/img/arrows/down.png" class="arrow arrow-down" alt="arrow down">
  <img src="/static/img/docs/one-dir-output.png" alt="Spekulatio output directory example">
</div>

Here, the following actions have been applied:

* Markdown files have been converted to HTML pages.
* The SCSS file has been converted to CSS.
* The PNG image has been copied over without transformation.
* The file starting with underscore (`_`) has been skipped and was not
  included in the final site.

Notice that the files in the output directory (`build`) have the same relative
path than their counterparts it the input directory (`content`) but with their
extension changed in some cases.

In the following sections we'll see how you can define your custom HTML for the
generated pages using templates, how you can add metadata to control how
Spekulatio behaves and how to customize which actions are applied to which
filetypes.

But let's start with how to run Spekulatio first.

The commands
------------

The tool has only two commands that you can run from any terminal.

One to build your site:

    spekulatio build

And another one to launch a development server:

    spekulatio serve

You typically run these commands at the root of your Spekulatio project.

To illustrate it, let's create a `hello-world` project with the following
content inside:

    hello-world/
    └── content/
        └── index.md

The file `index.md` can contain any Markdown formatted text. For example, let's
use:

    Hello World!
    ============

    This is my first Spekulatio site!

If you run `spekulatio build` inside `hello-world`, a new directory
`build` will appear with the contents of your first Spekulatio site:

    hello-world/
    ├── build/
    │   └── index.html
    └── content/
        └── index.md

Now, if you want to see how it looks like, you can run `spekulatio serve` —also from
inside `hello-world`— and a development HTTP server will be launched. By default
the port `8000` is used, but you can change that with the `--port` parameter (eg.
`spekulatio serve --port 5000`). Once launched, you should be able to see your
new site by pointing any browser to:

    http://localhost:8000/

You'll need to keep the development server running to be able to see your
changes as you do modifications and rebuild your site, and that's why it can be
a good idea to launch it in a different terminal from the one you're using to
run the `build` subcommand.

In our case, after opening a web browser at that URL, the result is:

![Hello World example site](/static/img/docs/hello-world.png){.mid .shadow}

Ok, not the most impressive website ever. Let's see how we can build up from
here.

!!! note "Debugging your site"
    If you get an error when building your site and the error message that you
    get is not completely clear, you can add the `-vv` (very verbose) parameter
    to the build command:

        spekulatio build -vv

    That will display all the operation logs of the tool and you'll be able to
    see what Spekulatio was trying to do when the error happened, which will
    potentially help you to locate the problem.

Input Directories
-----------------

In the examples above, we have passed one single input directory to the tool but
you can actually provide multiple ones. When you do so, the resulting output
directory is generated as if all the input directories had been merged together.
For example:

{# Example: two input directories being merged #}
<div class="three-part-example">
  <img src="/static/img/docs/two-dirs-input.png" alt="Spekulatio two input directories example">
  <img src="/static/img/arrows/right.png" class="arrow arrow-right" alt="arrow right">
  <img src="/static/img/arrows/down.png" class="arrow arrow-down" alt="arrow down">
  <img src="/static/img/docs/two-dirs-output.png" alt="Spekulatio two input directories example">
</div>

Here, the Markdown files of both input directories are converted. For the
directory `just-a-folder`, the contents of both sources are merged together. In
general, each file of each input directory is processed as if its input
directory was the only one.

However, the file `static/styles.scss` is present in both `foo` and `bar`. That
means that both input directories will produce the same `static/styles.css`
file. When that happens, the file in the second directory is the one that
is used. We'll see later how to specify a list of directories in a specific order
using a `spekulatio.yaml` file. But, for now, we can confidently say that `bar`
was listed after `foo` in this example.

!!! note "Overriding files using multiple input directories"

    Note that the important thing for a file to override another from a
    different input directory is not that they both have the exact same path and
    filename but that both generate the same filename in the output directory.
    For example, in Spekulatio both Markdown and reStructuredText files can
    generated HTML pages. That means that if we have `foo` and `bar` as input
    directories:

        my-project/
        ├── foo/
        │   └── page.md
        └── bar/
            └── page.rst

    then they both will generate the same `build/page.html` file. So depending
    on which directory is listed later, one will take prececence over the other.

The advantage of being able to pass multiple input directories comes from the
fact that **different input directories can be assigned different set of actions
per filetype**.

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
without modification.


### Default Input Directories

To define the list of input directories that you want to use, you have two
options:

* Use the list of **default input directories**.
* Provide a `spekulatio.yaml` file with a custom list.

The syntax of the `spekulatio.yaml` file and how it works is explained in a
later section. However, for many use cases it is enough to just use the default
input directories. To do so, you only have to create one or more of the
following directories at the same level where you run `spekulatio build`:

* `templates/`
* `data/`
* `content/`

When the `build` command is executed, these directories are checked and the ones
that are present are used as input. This only works if no `spekulation.yaml`
file is present, otherwise the list of input directories to be used is the one
defined in it.

Each one of the three default input directories has a set of actions assigned to
it. You can place your source files in one or another depending on what you want
to do:

#### content

> * Markdown, reStructuredText, JSON, YAML and HTML are converted into HTML
>   pages of the final site (using HTML templates).
> * SASS/SCSS files are converted to CSS.
> * Files starting with an underscore `_` are skipped.
> * Any other file is copied unmodified to the final site.

#### data

> All files are copied verbatim to the final site (unless they start with an
> underscore).

#### templates

> Same as `content` but HTML files are treated as templates and don't produce,
> by themselves, any pages in the site.

For example, if you have a project that looks like:

    my-project/
    ├── content/
    │   ├── page1.html
    │   ├── page2.md
    │   └── page3.json
    ├── data/
    │   └── foo.json
    └── templates/
        └── layout.html

The output directory will look like:

    build/
    ├── foo.json
    ├── page1.html
    ├── page2.html
    └── page3.html

Where the three pages from `content/` have been converted into final HTML pages
(potentially using the `layout.html` template), the `foo.json` file has been
copied unmodified and the `layout.html` didn't produce any output as it was just
available to be used as template.

### Priority of Default Input Directories

The priority of the default input directories is as follows:

    content > data > templates

That means that, for files generate the same path in the output directory,
the ones in `content` have precedence over the ones in `data`,
and the ones in `data` have precedence over the ones in `templates`.

For example, if you have:

    my-project/
    ├── content/
    │   └── static/
    │       └── styles.scss
    └── templates/
        └── static/
            └── styles.scss

The final `build/static/style.css` file will be generated using `styles.scss`
from `content`. Or, in other words, the styles that you provide in your content
will override the ones provided in your templates if their paths are the same.

Templates
---------

Using the `templates` default directory (or any input directory defined in
[spekulatio.yaml](#spekulatioyaml) with the `use_as_templates` action assigned),
you can customize the HTML of your site. Any HTML page in it will be created as
the combination of a **content file** (a Markdown, reStructuredText, JSON, YAML
or HTML file in the `content` directory) and one **template** in `templates`.

Consider this basic example:

    hello-world/
    ├── build/
    │   └── index.html
    ├── content/
    │   └── index.md
    └── templates/
        └── some-directory/
            └── my-template.html

The `index.html` page in `build` is rendered by passing the processed contents
of `index.md` to the template `some-directory/my-template.html`.

Where the content of `index.md` is:
```
---
_template: some-directory/my-template.html
author: me
---

Hello World!
============

This is my first Spekulatio site!
```

And this is the content of `my-template.html`:

{% raw %}
```html
<!DOCTYPE html>
<html>
    <body>
        <article>
          <div class="author">{{ author }}</div>
          <div class="content">
            {{ _node.content }}
          </div>
        </article>
    </body>
</html>
```
{% endraw %}

You can see that we added a **front-matter** to the top of the Markdown file
(the three-dashes delimited YAML snippet) and we added some **Jinja** syntax
(double curly brackets) together to a new variable (`_node`) to the HTML
template.

Let's take a look at those new elements.

!!! note "Control Your HTML"

    As you can see, stating to write your own HTML in Spekulatio is a question
    of adding a file to the correct directory. There's no restriction or
    predefined structure that you need to take into account when writing the
    HTML itself either. You can also write your templates in a way that they can
    be reused across projects (as _themes_) or have them specificaly written for
    your current project.

### Front-matter

The front-matter is a very common way in static site generators of adding
metadata to your content. It is always at the top of the file and it consists of
a YAML snippet surrounded by lines of three dashes:
```
---
_template: some-directory/my-template.html
author: me
---
```
In Spekulatio, you can add any valid YAML content to it —including nested
elements— as long as the root element is a dictionary (as opposed to a list).

In our example, there are two variables defined: `_template` and `author`. All
values that start with an underscore are **special values**. There are only a
limited number of them, like `_title`, `_sort` or `_template`, and they have a
specific meaning in Spekulatio. To see a complete list of them, you can check
the reference page [Special Values](/docs/reference/special-values.html). All
other values —the ones without a leading underscore— are **user values** and are
up to the user to define. In this case, we set `author` but we could have chosen
`foobar` or `spam_and_eggs`, from the point of view of the tool, it doesn't
matter.

The `_template` value tells Spekulatio which template you want to use. Its
value has to be relative to the input directory where the templates are stored.
Which templates are defined and how they are used is up to you. One very common
use case is to define different templates for different page layouts. For
example, you can have two templates: one for an one column layout and another
one for two columns. In the following project, you could have the home page
(`index.md`) be rendered using the one-column layout and the articles (`foo.md`
and `bar.md`), using the two-columns one:

    hello-world/
    ├── content/
    │   ├── articles/
    │   │   ├── foo.md
    │   │   └── bar.md
    │   └── index.md
    └── templates/
        ├── one-column.html
        └── two-columns.html

If you have multiple input directories with templates, the file that you specify
will be searched through them starting by the last directory listed. That means
that if two input directories contain a template with the same relative path,
the second one will have precedence over the first.

### Jinja Syntax

Spekulatio uses the [Jinja library](https://jinja.palletsprojects.com/) to power
its templates. It is very flexible and mature and offers a great deal of
features. The most basic one is interpolating a variable:

{% raw %}
```html
<div class="author">{{ author }}</div>
```
{% endraw %}

That will be rendered, in our example, as:
```html
<div class="author">me</div>
```

However, Jinja offers much more including conditional statements, loops over
values, definition of reusable blocks and so on. You can find the documentation
of the possibilities it offers at:

[https://jinja.palletsprojects.com/en/3.0.x/templates/](https://jinja.palletsprojects.com/en/3.0.x/templates/)

The documentation is very complete and easy to follow, but let's cover here some
basic elements.

#### Delimiters

To use Jinja constructs, use the following delimiters:

{% raw %}
* `{{ … }}` for expressions (eg. like interpolating the value of a variable)
* `{% … %}` for statements (eg. `if` or `for` loops)
* `{# … #}` for comments. These, unlike HTML comments, won't appear in the final
  rendered pages.
{% endraw %}

#### Variable interpolation

Consider a set of variables of different kinds:
```
a_scalar: foo
a_list:
  - one
  - two
a_dictionary:
  one:
    two: true
```
You can show their values with the double curly brace notation we saw before
{% raw %}`{{ … }}`{% endraw %}:
{% raw %}
```html
<span>This is a scalar: {{ a_scalar }}</span>
<span>This is an element in a list {{ a_list[2] }}</span>
<span>This is an element in a dictionary {{ a_dictionary.one.two }}</span>
```
{% endraw %}
Also, you can apply _filters_ to the values using pipes:
{% raw %}
```html
<span>This is a scalar: {{ a_scalar|upper }}</span>
```
{% endraw %}
The list of all available built-in filters is available
[here](https://jinja.palletsprojects.com/en/3.0.x/templates/#list-of-builtin-filters).

#### If Statements

You can conditionally render parts of your HTML with `if` statements:
{% raw %}
```
{% if <expresion> %} … {% endif %}
```
{% endraw %}

For example, if you have values defined as:
```
category: foo
show_banner: true
```
Then you can use them as follows:
{% raw %}
```html
<!DOCTYPE html>
<html>
    <head>
        {% if category == 'foo' %}
        <link rel="stylesheet" href="static/css/special-styles.css">
        {% endif %}
    </head>
    <body>
        {% if show_banner %}
        <div class="banner">
            …
        </div>
        {% endif %}
    </body>
</html>
```
{% endraw %}

#### For Loops

If you define lists, you can iterate through them using:
{% raw %}
```
{% for <variable> in <iterable> %} … {% endfor %}
```
{% endraw %}
For example, giving this list:
```
authors:
  - Mary
  - John
  - Sam
```
Then you can iterate over it like this:
{% raw %}
```html
<!DOCTYPE html>
<html>
    <body>
        <ul class="authors">
            {% for author in authors %}
            <li>{{ author }}</li>
            {% endfor %}
        </ul>
    </body>
</html>
```
{% endraw %}

#### Template Inheritance and Includes

In almost every site, there are parts of the layout that are reused across
different pages. Headers, sidebars or footers are the most common usual suspects
in this regard. If your site uses one single template for every page then
reusing those components is very straightforward. You add them to the template
and every page will show them. However, if you have a more complex site, you may
want to have different layouts that still share some components. For instance,
you may want to have some pages displaying an one-column layout and others a
two-column one, while still keeping the same header and footer.

To solve that problem you can use **template inheritance** in Jinja, which
allows you to specify that one template has to be based in another one but
replacing only parts of it.

To illustrate it, imagine that we have the following `templates` folder:

    templates/
    ├── base.html
    ├── one-column.html
    └── two-columns.html

Then `base.html` can contain all the common elements to every page:

    <!DOCTYPE html>
    <html>
        <head>
            <link rel="stylesheet" href="static/css/styles.css">
            <title>My Site</title>
        </head>
        <body>
            <header> … </header>

            {% block content %}
            {% endblock %}

            <footer> … </footer>
        </body>
    </html>


### Using templates

### Overriding templates

### The \_node object

### Themes

!!! note "Themes"

    Another important advantage that multiple input directories bring is that
    "themes" in Spekulatio are just regular input directories. If you want to
    define a theme, you just need to provide an input directory (typically
    containing HTML templates and other files such as CSS styles, JS scripts and
    images) and reuse it across projects. The only thing that you may want to
    take into account is to pass the "theme" directory with less priority so the
    content directories can override some aspects if necessary. (For example,
    you can create a symbolic link `templates` that points to the actual theme
    directory in multiple projects).

Values
------

In Spekulatio, you can also define metadata in some content files
using a **front-matter** or define metadata in directories using a special
`_values.yaml` file in them.

In Spekulatio these *metadata* items are named **values** and can be used as
pieces of information to be shown in your final HTML pages or to control how
Spekulatio behaves.

Front-matter
------------

A **front-matter** is a YAML snippet delimited by two three-dashes lines that
can be added to the top of any Markdown, reStructuredText or non-template HTML
file. It can be used, for example, to define metadata related to your document:

    ---
    author: Sam
    date: Oct 3rd, 2021
    category: Some Category
    ---

    A Title
    =======

    Some content.

Any value defined in the front-matter becomes automatically available to the
template engine when the page is being rendered. In the example above, that
means that you could access `author`, `date` and `category` in a HTML template
like this (of course, which HTML tags and styles to use are up to you):

    <ul>
      <li>{{ author }}</li>
      <li>{{ date }}</li>
      <li>Archived under: {{ category }}</li>
    </ul>

As you'll see below in the [Special and User Values](#special-and-user-values)
section, you have all the freedom to create the values that you need for your
site. There's no predefined set that you *have* to use or that you're *limited*
to. As far as Spekulatio is concerned, you can just define `foo: bar` and it
will be perfectly ok. There are, however, some values that have a special
meaning for the tool. They all start with an underscore (`_`) and change how
Spekulatio behaves. For example, `_template` defines which template file to use
to render the current file:

    ---
    _template: my-templates/two-columns-layout.html
    ---

    A Title
    =======

    Some content.

An important aspect of the front-matter is that the top level must be a
mapping/dictionary (as opposed to a list or a scalar), but other than that the
values of the dictionary can be of any kind. For example, you can define nested
dictionaries or lists:

    ---
    my_data:
      authors:
        - Sam
        - Jim
    ---

    A Title
    =======

    Some content.

And then access them in the templates like:

    {% raw -%}
    <ul>
    {% for author in my_data.authors %}
      <li>{{ author }}</li>
    {% endfor %}
    </ul>
    {% endraw -%}

!!! Note
    A front-matter is a very common way of defining metadata among static site
    generators and many tools have built-in support for it, such as text editors
    showing the correct syntax highlighting in Markdown files that have one
    present.

### Everything is a dictionary

One key fact about Spekulatio is that each page of the site is internally
represented as a dictionary of information. Take the following Markdown file for
example:

    ---
    author: Sam
    date: Oct 1st, 2021
    ---

    A Title
    =======

    Some content.

When Spekulatio processes this file, its information is stored in the form of a
dictionary that contains keys for:

* The items in the front-matter.
* A `_content` entry with the Markdown text already converted to HTML.

In JSON syntax, that dictionary would look like:

    {
      "author": "Sam",
      "date": "Oct 1st, 2021",
      "_content": "<h1 id="a-title">A Title</h1><p>Some content.</p>"
    }

That means that you can think of the non-front-matter part of the content of
Markdown, reStructuredText or non-template HTML files as a convenient way of
defining the special `_content` value.

For example, if you only provide a front-matter and no body of text:

    ---
    foo: bar
    ---

Then the internal representation of the page will look like:

    {
      "foo": "bar",
      "_content": ""
    }

In practice, in addition to `_content`, Spekulatio may include additional fields
in the dictionary depending of the filetype that is being processed. For
example, for Markdown, the following fields are added:

* `_title`: Main title of the page (ie. the H1 header).
* `_src_text`: The raw Markdown text
* `_content`: The Markdown text converted to HTML
* `_toc`: An structure with the table of contents of the Markdown text

Check the [Actions Reference page](/docs/reference/actions.html) to get more
information of what values are automatically added to the dictionary depending
on the filetype being processed (eg. `md_to_html`, `rst_to_html`,
`html_to_html`).

!!! note "Special values can be overwritten"

    The front-matter of a file has precedence over the special values that
    Spekulatio automatically adds. For example, it is perfectly fine to define
    `_title` inside the front-matter and override the default value, which is
    extracted from the first Markdown header.

### JSON and YAML content files

Markdown, reStructuredText and non-template HTML files are treated as
dictionaries in which the body of text is used as the source to compute the
`_content` entry. And in the same way, **JSON and YAML files can also generate
HTML pages in the final site, only that in these two cases what you pass to the
tool is the raw dictionary itself**.

For example, consider an example `foo.md` file:

    ---
    author: Sam
    _template: my-template.html
    ---

    A Title
    =======

    Some content.

Inside Spekulatio, it will generate the following dictionary (in JSON syntax):

    {
      "author": "Sam",
      "_template": "my-template.html",
      "_title": "A Title",
      "_content": "<h1 id='a-title'>A Title</h1><p>Some content.</p>"
      "_src_text": "A Title\n=======\n\nSome content.\n",
      "_toc": [{"level": 1, "id": "a-title", "name": "A Title", "children": []}],
    }

Now, if you add that JSON content as a `bar.json` to your input directory, the
content of the two files that will be generated from the Markdown and JSON ones
(`foo.html` and `bar.html`) will be exactly the same. That means that all the
content formats of Spekulatio:

* Markdown
* reStructuredText
* non-template HTML
* JSON
* YAML

are just different ways of passing the exact same information to the tool.

Of course, writing HTML inside quotes of a JSON string is probably not a fun
experience and you may want to use Markdown or reStructuredText for texts
instead —and raw HTML for more complex content. However, both JSON and YAML can
be a very good fit to hold structured data. For example, let's say that you have
a database full of metadata about TV series. Potentially, you can export the
information to JSON files and have them automatically rendered as different
pages in your site.

Like for the other formats, to generate pages out of JSON and YAML files, you
need to add them to an input directory that has the correct actions associated
to it (ie. `json_to_html` associated to JSON and `yaml_to_html` associated to
YAML). The `content` default input directory and the `site_content` preset
convert JSON and YAML to pages automatically.

!!! Note "Special values in JSON and YAML files"

    The example above may led to think that if you provide content using JSON or
    YAML files, you *need* to provide special fields such as `_title` or
    `_content`. That is absolutely not the case. Spekulatio generates these
    special values automatically when a Markdown file is processed, for
    instance. But it is up to you to use them or not in your templates. In the
    same way, you just have to add values to the JSON and YAML files that you'll
    be using in your HTML templates. For example:

        {
          "foo": "bar"
        }

    is a perfectly valid JSON file to generate an HTML page in Spekulatio. The
    HTML template will receive the `foo` value and it is up to you how to
    display it in the page.

    That said, sometimes it can be useful to add special values to JSON or YAML
    files. For instance, if all your templates expect a `_title` variable to be
    defined independently of the filetype of the source file, you can add it
    like any other user value.


The \_values.yaml file
----------------------

Using the front-matter, you can set a particular value, let's say `author`, to
any given page. Now, imagine that you want to assign the same author to one
hundred articles that are stored under a particular directory of your site.
Setting the value in each single page sounds like both laborious and difficult
to maintain in the long run, and that's why Spekulatio allows you to define
values at the directory level.

If you add a `_values.yaml` file to a directory, all the values defined inside
are automatically assigned to that directory and all its descendants. For
example, imagine that you have this input directory:

    content/
      index.md
      dir1/
        _values.yaml
        article-1.md
        article-2.md
        extra/
          article-3.md

And the content of `_values.yaml` is:

    author: me

then, the value `author: me` will be available in all articles (`article-1`,
`article-2` and `article-3`) as if it were defined in their front-matter. This
only applies recursively to *descendants* of `dir1/` and `index.md` —one level
above— wouldn't be affected, for instance.

!!! note

    The fact that `_values.yaml` starts with an underscore is not a coincidence.
    It prevents Spekulatio from mistakenly taking the file as a regular YAML one
    and trying to generate a HTML page out of it. Since underscore files are
    automatically skipped by the tool, `_values.yaml` is skipped too.

### Value priority

Now imagine that you have a directory containing one hundred articles by the
same author, Mary, except for two of them that are written by Sam. If you set
the `author` value in a `_values.yaml` file at the root of the directory, all
articles will be assigned to the same author. And setting the `author` value in
each article doesn't sound very appealing either. In that case, what you can do
is to set `author: Mary` in `_values.yaml` and `author: Sam` in the front-matter
of the only two articles that differ.

In other words, front-matter values have priority over the ones inherited from
the `_values.yaml` files. Or even more generally, **each node of the site tree
can override values any parent node**.

That means that if you have a input dictionary as this:

    content/
      _values.yaml
      dir1/
        _values.yaml
        dir2/
          _values.yaml
          file.md

the priority from highest to lowest when it comes to defining values is:

* the front-matter of `content/dir1/dir2/file.md`
* `content/dir1/dir2/_values.yaml`
* `content/dir1/_values.yaml`
* `content/_values.yaml`

That is, a descendant can always override any value set by any ancestor.

### It's dictionaries all the way down

The fact that values are recursively inherited is the key to understanding how
Spekulatio works. We have seen that, internally, Spekulatio treats content files
as data dictionaries. Well, this is true for every directory too. Basically, if you have
an input directory tree like:

    contents/
      index.md
      _values.yaml
      dir1/
        bar.md
        _values.yaml
        dir2/
          foo.md
          _values.yaml
      static/
        styles.scss
        _values.yaml

The resulting site is internally computed as a tree of dictionaries where each
node contains the data defined in itself (by means of the front-matter in the
case of pages and the `_values.yaml` file in the case of directories) and the
data that it inherits recursively from its ancestors:

[TODO: tree of dictionaries]

This tree of dictionaries is essential to how the final site is created: first,
input directories get merged to define the tree structure of the final site,
then a tree of dictionaries using this structure is created —with values being
inherited from parent to descendants— and, finally, the pages of the site are
created by passing the values of this directories to the corresponding
templates.


User Values
-----------

Spekulatio doesn't define any specific content-related values such as `author`,
`date`, or `tag`. You can define them if you need, of course, but those values
don't have any special meaning inside the tool. They are **user values** and you
can use them for two things:

* **Display them in the pages of your site**. For example, if you define the author
  of an article as `author: Sam`. Then you can just display it in your templates
  with something similar to:

        <div id="author">{{ author }}</div>

  However, if you have a site in which defining multiple authors per article
  makes more sense, you can just do it by defining a user value that fits your
  needs, like for instance: `authors: ['Mary', 'Sam']`. And then you can display
  it as:

        <ul id="authors">
        {% for author in authors %}
          <li>{{ author }}</li>
        {% endfor %}
        </ul>

* **Change how your site is rendered**. Since you can access user values in your
  templates, you can use them as variables and then render your site's pages
  depending on their values. For example, you can define a variable
  `show_footer` that can have values `true` or `false` and then your template
  can contain something like:

        {% if show_footer %}
        <footer>
          …
        </footer>
        {% endif %}

  Another example: you can define a variable that contains the list of CSS files
  that should be loaded in each page. The variable can be initialized with the
  default list of files but can also be overridden in particular pages or entire
  sections. For instance, in the root `_values.yaml` file, you can have:

        css_files:
          - /styles/css/reset.css
          - /styles/css/base.css
          - /styles/css/cusomization.css

  And then in your template:

        <head>

        …

          {% for css_file in css_files %}
          <link rel="stylesheet" href="{{ css_file }}">
          {% endfor %}

        …

        </link>

Thanks to the fact that you can define any values that you want, that they can
have any arbitrary structure (nested lists, dictionaries or scalars),
that they are inherited and overridden from pages and
sections and that you can control the site rendering with them, user values
offer a great way to parametrize your project.

Special Values
--------------

While _user values_ can be freely defined and used, Spekulatio also defines a
limited set of _special values_. Those always start with a single underscore
(`_`) and are used to change the behavior of the tool.

The most important one is `_template` which is used to specify which template
has to be used when rendering content files (such as Markdown, reStructuredText,
non-template HTML, JSON or YAML ones) to HTML. There are other values like
`_alias` that can be set to refer to a page without having to use its path or
URL or `_md_options`, `_rst_options`, `_sass_options`, which allow you to
configure how the conversion of different filetypes takes place.

A more in-depth description of special values is provided in the
[Templates](/docs/templates.html) and [Nodes](/docs/nodes.html) sections, but you
can also check the list of all available ones in the [Special
Values](/docs/reference/special-values.html)
reference section.

!!! Note

    Note that a leading underscore means two different things when it is applied
    to either the name of a value or to a filename. A filename that starts with an
    underscore is skipped and doesn't generate an associated file in the final
    site. In the name of a value, an underscore means that the value has a
    special meaning within Spekulatio.

Value Extended Syntax
---------------------

Imagine that you define a value like this in the `_values.yaml` at the root of
your input directory:

    css_files:
      - /static/css/reset.css
      - /static/css/styles.css

If you add the following lines to the `<head>` section of your base template:

    {% for css_file in css_files %}
    <link rel="stylesheet" href="{{ css_file }}">
    {% endfor %}

all pages of your site will use the same set of CSS files. That's very
convenient since you can just change that value if you want to add an additional
CSS file and the whole site will be automatically updated.

Now, imagine that you have a page where you would like to add one extra CSS file
without affecting the others. Maybe you need to add some custom styles
that only apply there for some reason. If you add this to its front-matter:

    ---
    css_files:
      - /static/css/reset.css
      - /static/css/styles.css
      - /static/css/custom.css
    ---

you'll get the desired effect. All other pages will use the value set at the root
of the site and this page will use the overwritten value since front-matter
values have preference over inherited ones. However, there's a problem, if now
you update the `css_files` values at the root of the site to include an
additional file:

    css_files:
      - /static/css/reset.css
      - /static/css/styles.css
      - /static/css/one-more.css

the overwritten value in the page will not reflect the change.

To solve this kind of problem, Spekulatio offers the _extended syntax_ for
values. If you prefix the name of your value by *two* underscores, you can
provide a dictionary that allows you to control how the value is set. For
instance, in the case of the example above we could do:

    ---
    __css_files:
      operation: append
      value:
        - /static/css/custom.css
    ---

which would add the new CSS file to the already existing value of `css_files`,
effectively resulting in setting the variable to:

    css_files:
      - /static/css/reset.css
      - /static/css/styles.css
      - /static/css/custom.css

Once you prefix the name of your variable with two underscores, instead of
passing the actual value you want it to hold, you can provide a dictionary
of the form:

    __name:
      operation: replace|append|merge|delete
      scope: local|level|branch
      value: <value to use>

where:

* `operation` let's you define what to do with the value. `replace` is the
  default option, it means that the new value will replace any existing one with
  the same name. `append` applies only to lists and adds the list provided in
  `value` to the existing one. `merge` is similar to `append` but it applies to
  dictionaries, it will merge the dictionary provided in `value` to the already
  existing one. And, finally, `delete` removes the value altogether (you don't
  provide a value in this case).

* `scope` controls how the value will be inherited by descendant pages. It only
  makes sense to use it in `_values.yaml` files since values defined in a
  front-matter are not inherited by any other page. For instance, if you set the
  scope to `local` the value won't be inherited by any children of the
  directory. `level` makes the value to be set in the directory and all the
  direct children. `branch` is the default and makes the value to be recursively
  set in every descendant of the current directory.

* `value` is the actual value to use by the selected `operation`.

For example, when you declare a value like:

    foobar:
      one: 1
      two: 2

then, in a descendant page or directory you can do:

    __foobar:
      operation: merge
      value:
        three: 3

which will result in the value set to:

    foobar:
      one: 1
      two: 2
      three: 3

Even if the value has not been set before, you can use the extended syntax. For
example, if you want to set a special header only for the direct children of a
directory, you can set a value like this in its `_values.yaml` file:

    __special_header:
      scope: level
      value: true

then in the template you can check the value of `special_header` and change the
HTML to use accordingly.

Finally, it is necessary to note that the normal syntax for setting values like:

    foo: bar

is just a short form for:

    __foo:
      operation: replace
      scope: branch
      value: bar

Styles
------

Virtual nodes
-------------

spekulatio.yaml
---------------

