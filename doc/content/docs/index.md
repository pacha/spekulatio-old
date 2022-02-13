---
_alias: docs
---

Documentation
=============

This page will walk you through creating static websites using Spekulatio. All
the main topics you need to know are present here; however, the links at the
right can provide deeper insights into special topics.

Check the [Download]({{ get_url('download') }}) section for information about how to
install Spekulatio in case you don't have it installed in your system yet.

The basics
----------

The essence of Spekulatio is very simple: you provide one or more **input
directories** and the tool creates one **output directory** containing your
newly generated site. The files in the output directory are created by applying
actions to the ones in the input directories.

In this example, you can see how `content` is converted into `build`:

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
* The file starting with underscore (`_`) has been skipped and not
  included in the final site.

Notice that the files in the output directory (`build`) have the same relative
path than their counterparts it the input directory (`content`) but with their
extension changed depending on the applied transformation.

And that is the essence of Spekulatio: it just transforms input files into
output ones. However, to allow you to create complex sites it provides some
additional tools:

* You can pass multiple **input directories** and assign different set of
  **actions** or transformations to each one. That means that one file format
  can be processed differently depending on which directory you place it into.

* You can define the HTML used to convert content files using Jinja
  **templates**, which provide you with ways to define reusable headers,
  footers, sidebars and give you also programming constructs such as `if` or
  `for` statements.

* You can define your own **values** at any point of your site and use them
  in your templates either to show them or to change how your site is rendered.

Also, doing all that is pretty straightforward as you'll see in the next
sections, but, first, let's take a look to Spekulatio's commands.

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
```
:::md
Hello World!
============

This is my first Spekulatio site!
```

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
changes as you do modifications and rebuild your site. That's why it can be
a good idea to launch it in a different terminal from the one you're using to
run the `build` command.

In our case, after opening a web browser at that URL, the result is:

![Hello World example site](/static/img/docs/hello-world.png){.mid .shadow}

Ok, not the most impressive website ever... yet. Let's see how we can build up
from here.

!!! note "Debugging your site"

    If you get an error when building your site and the error message that you
    get is not completely clear, you can add the `-v` (verbose) or `-vv` (very
    verbose) parameters to the build command:

        spekulatio build -vv

    This will display all the operation logs and you'll be able to
    see what Spekulatio was trying to do when the error happened.

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

Here, the Markdown files of both input directories are converted. For example,
in the directory `just-a-folder`, the contents of both sources are merged
together.

However, the file `static/styles.scss` is present in both `foo` and `bar`. That
means that both input directories will produce the same `static/styles.css`
file. When that happens, the file in the second directory is the one that is
used. That's an important fact when it comes to provide multiple input
directories: they are ordered and the later ones override the first ones when
there's a conflict.

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

One of the main advantages of being able to pass multiple input directories is
that **different input directories can be assigned different set of actions per
filetype**.

### Default Input Directories

To pass a list of input directories, you can use the [spekulatio.yaml]({{
get_url('spekulatio.yaml') }}) configuration file. That allows you to provide any
number of input directories and name them in any way you want.

However, most of the time, the easiest way to pass content to Spekulatio is
just using the **default input directories**:

* `templates/`
* `data/`
* `content/`

When `spekulatio build` is executed, these directories are searched in the
current directory and the ones that are present are used as input. **This only
works if no [spekulatio.yaml]({{ get_url('spekulatio.yaml') }}) file is present**,
otherwise the list of input directories to be used is the one defined inside
that file.

Each one of the three default input directories has a set of actions assigned to
it. You can place your source files in one or another depending on what you want
to do:

#### content

> * **Markdown**, **reStructuredText**, **JSON**, **YAML** and **HTML**
>   are converted into **HTML** pages of the final site (using Jinja templates).
> * **SASS**/**SCSS** files are converted to **CSS**.
> * Files starting with an underscore `_` are skipped.
> * Any other file is copied unmodified to the final site.

#### data

> All files here are copied verbatim to the final site (unless they start with an
> underscore, then they are skipped).

#### templates

> Same as `content` but **HTML** files are treated as templates and don't produce,
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

Where the three pages from `content` have been converted into final HTML pages
(potentially using the `layout.html` template), the `foo.json` file has been
copied unmodified and the `layout.html` didn't produce any output as it was just
available to be used as template.

!!! note "Priority of default input directories"

    For files that generate the same path in the output
    directory, the ones in `content` have precedence over the ones in `data`,
    and the ones in `data` have precedence over the ones in `templates`:

        content > data > templates

    For example, if you have:

        my-project/
        ├── content/
        │   └── static/
        │       └── styles.scss
        └── templates/
            └── static/
                └── styles.scss

    The final `build/static/style.css` file will be generated using `styles.scss`
    from `content`.

Templates
---------

Using the `templates` default directory, you can customize the HTML generated in
your site. Any HTML page in it will be created as the combination of a **content
file** (a Markdown, reStructuredText, JSON, YAML or HTML file) in `content` and
one **template** in `templates`.

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

The content of `index.md` could be something like:
```
---
_template: some-directory/my-template.html
author: me
---

Hello World
===========

This is my first Spekulatio site!
```

And this is the content of `my-template.html`:

{% raw %}
```
:::jinja
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

### The `_template` value

You can see that we added a **front-matter** to the top of the Markdown file
(the three-dashes delimited YAML snippet). This is one of the ways in which
variables (also known as **values**) can be defined. We'll cover how **values**
work in the next section, but for now just keep in mind that there are two
kinds: the ones that start with an underscore (`_`), which are *special values*
and are known by the tool and the ones without leading underscore, which are *user
values* and that you're free to define yourself. `_template` is an special value
and tells Spekulatio which template file you want to use to render this file.
`author` is an *user value* and it is just added as an example, it could be
literally anything (it makes sense that the value is then used in the template
in some way though).

You can check the complete list of special values [here]({{ get_url('special-values') }}).

### Jinja syntax

You can also see that the template uses double curly brackets
{% raw %}(`{{ … }}`){% endraw %} to access variables.
This is part of the Jinja templating syntax.
[Jinja](https://palletsprojects.com/p/jinja/) is a very popular templating tool
that allows you to interpolate variables, conditionally add or remove HTML text
using `if` statements or loop through lists using the `for` construct. Apart
from those, it has many more features such as filters and macros, and a very
elegant system of template inheritance that allows you to define reusable parts
of the page such as headers, footers or sidebars.

This is a quick example of how using values of different kinds looks like in a
template.

*Values*:
```
:::yaml
my_variable: 1
my_list:
  - foo
  - bar
my_dict:
  foo: 1
  bar: 2
```

*Template*:
{% raw %}
```
:::jinja
<!DOCTYPE html>
<html>
    <body>
      {# This is a comment. It won't appear in the rendered output #}

      {# Use of a scalar variable #}
      <p>The value of <code>my_variable</code> is {{ my_variable }}.</p>
      {% if my_variable < 100 %}
      <p>Which is a small number.</p>
      {% endif %}

      {# Use a for-loop to iterate through a list #}
      <ul>
      {% for element in my_list %}
        <li>{{ element }}</li>
      {% endfor %}
      </ul>

      {# Access of dictionary elements #}
      <p>The value of <code>my_dict['foo']</code> is {{ my_dict['foo'] }}.</p>
      <p>You can also use the dot notation {{ my_dict.foo }}.</p>

    </body>
</html>
```
{% endraw %}






Values
------


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
up to the user to define. In this case, we have defined `author` but we could
have chosen `foobar` or `spam_and_eggs`, from the point of view of the tool,
you're free to use any variable that you need.

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

### Variables

In our example above, we used variables inside our template as follows:
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

Styles
------

Virtual nodes
-------------

spekulatio.yaml
---------------


Using YAML and JSON files as content
------------------------------------

In the same way that you can generate HTML pages in the final site from
Markdown, reStructuredText or raw HTML, you can also use both YAML and JSON
files. This can be useful when you want to generate site pages out of structured
information. For example, you could save records of books, games, movies or
products as JSON files and then generate a page per record.

Actually, from Spekulatio's point of view, there's no much difference between
passing YAML or JSON or any other content format. For instance, the following
Markdown file:

    ---
    author: Sam
    date: Oct 1st, 2021
    ---

    A Title
    =======

    Some content.

is roughly translated within the tool as the following dictionary:

    {
      "author": "Sam",
      "date": "Oct 1st, 2021",
      "_content": "<h1 id="a-title">A Title</h1><p>Some content.</p>"
    }

The front-matter is added as key-value pairs and then an additional entry is
added for the Markdown content already converted to HTML.

As you can see, that is 

The key fact about Spekulatio is that each page of the site is internally
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


