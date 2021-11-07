
Actions
=======

In Spekulatio, each file in an input directory is transformed (unless skipped)
into a file of the output directory using an **Action**. This is the complete
list of actions available in the tool. You can assign an action to a
[filetype]({{ get_node(alias='filetypes').url }}) using the
[spekulatio.yaml](/docs/config.html) configuration file.

`copy`
: Copies the file to the output directory without performing any transformation.
  Valid for any kind of filetype.

`html_to_html`
: Generates a HTML page in the output directory by passing the following values
  to a HTML template:

    * `_content`: the unmodified HTML content of the current file.
    * `_src_text`: same value as `_content`.
    * Any values specified in the front matter of the current file.
    * Any values inherited by this node.

    The template to be used is determined by the current value of `_template`
    —so the value is either defined previously and inherited by this node or
    defined in the front matter of the current file. HTML files to which this
    action is applied to don't typically feature the markup for a complete HTML
    page but just the HTML that should be used as content when inserted into the
    desired template.

`ignore`
: Skips the file and nothing is generated in the output directory.

`json_to_html`
: Generates a HTML page in the output directory by passing the contents of the
  JSON file to a template as values. For this to work is necessary that the JSON
  file contains a dictionary as root element. The JSON dictionary can also
  define any special values like `_title` or `_content`. And, in particular, it
  can specify the value of `_template` to override the current value of this
  variable. For example:

        {
          "_template": "some/template.html",
          "_title": "Page rendered from a JSON file",
          "_content": "<p>You can also pass any content to be inserted</p>",
          "a_variable": "And you can add any additional values",
          "a_list": ["one", "two"]
          …
        }

`md_to_html`
: Generates a HTML page in the output directory by passing the following values
  to a HTML template:

    * `_content`: the Markdown content of the file converted to HTML.
    * `_src_text`: the original Markdown content of the file.
    * `_toc`: the _table of contents_ of the file.
    * Any values specified in the front matter of the file.
    * Any values inherited by this node.

    The table of contents (`_toc`) has the following structure (same as for
    reStructuredText files with the `rst_to_html` action):

        [
          {
            "level": 1,
            "id": "title-1",
            "name": "Title 1",
            "children": [
              {
                "level": 2,
                "id": "title-2",
                "name": "Title 2",
                "children": []
              },
              …
          },
          …
        ]

    The template to be used is determined by the current value of `_template`
    —so the value is either defined previously and inherited by this node or
    defined in the front matter of the current file. You can also access any
    values inside the Markdown content itself using Jinja notation:

        {% raw %}
        ---
        foo: 3
        ---

        Title
        =====

        The value of `foo` is {{ foo }}.
        {% endraw %}

`render`
: Generates a file in the output directory with the same extension as the
  original file by passing the following values to a Jinja template:

    * `_content`: the contents of the file.
    * `_src_text`: same as `_content`.
    * Any values specified in the front matter of the file.
    * Any values inherited by this node.

    The template to be used is determined by the current value of `_template`
    —so the value is either defined previously and inherited by this node or
    defined in the front matter of the current file. You can also access any
    values inside the Markdown content itself using Jinja notation. For example,
    you can render a plain text file using a plain text template and use Jinja
    notation in both the original file and the template itself:

        {% raw %}
        ---
        template: some/template.txt
        foo: 3
        ---

        The value of foo is {{ foo }}.
        {% raw %}

`render_without_frontmatter`
: Exactly the same as `render` but will not check if a front matter is present
  in the original file. This is useful when the contents of the file could make
  the tool think that there's a front matter present when there's none (for
  example, if you want to render raw YAML files). Note that `render` can be used
  with files that don't have a front matter. `render_without_frontmatter` is
  intended to be used with files that don't have one but that might mislead the
  tool into thinking that there's actually one.

`rst_to_html`
: Generates a HTML page in the output directory by passing the following values
  to a HTML template:

    * `_content`: the reStructuredText content of the file converted to HTML.
    * `_src_text`: the original reStructuredText content of the file.
    * `_toc`: the _table of contents_ of the file.
    * Any values specified in the front matter of the file.
    * Any values inherited by this node.

    The table of contents (`_toc`) has the following structure (same as for
    Markdown files with the `md_to_html` action):

        [
          {
            "level": 1,
            "id": "title-1",
            "name": "Title 1",
            "children": [
              {
                "level": 2,
                "id": "title-2",
                "name": "Title 2",
                "children": []
              },
              …
          },
          …
        ]

    The template to be used is determined by the current value of `_template`
    —so the value is either defined previously and inherited by this node or
    defined in the front matter of the current file. You can also access any
    values inside the reStructuredText content itself using Jinja notation:

        {% raw %}
        ---
        foo: 3
        ---

        =====
        Title
        =====

        The value of ``foo`` is {{ foo }}.
        {% endraw %}

`sass_to_css`
: Compiles a `.sass` or `.scss` file into a `.css` one.

`use_as_template`
: When this action is associated to a given filetype inside an input directory,
  the whole directory is marked to be used as a container of templates and all
  the files of the given type are skipped and don't generate anything in the
  output directory. For example, if you associate `.txt` files to
  `use_as_template` in `my-dir/`, then you can 

`virtual_node`
: This action can be applied to YAML files and makes those them to be skipped so
  they don't generate any output. However, they can internally define values and
  will be present in the node tree passed to all templates. This is useful when,
  for example, you want to autogenerate the items of your site menu inside your
  layout by inspecting the node tree and have some of them pointing to external
  resources. In that case, the virtual nodes will represent the external
  resources and can contain metadata that points to them (eg. their URL or an
  icon) without having a file being generated in the site itself. All files with
  a `.meta.yaml` or `.meta.yml` extension are automatically applied this action.

`yaml_to_html`
: Generates a HTML page in the output directory by passing the contents of the
  YAML file to a template as values. For this to work is necessary that the YAML
  file contains a dictionary as root element. The YAML dictionary can also
  define any special values like `_title` or `_content`. And, in particular, it
  can specify the value of `_template` to override the current value of this
  variable. For example:

        _template: some/template.html
        _title: Page rendered from a YAML file
        _content: "<p>You can also pass any content to be inserted</p>"
        a_variable: And you can add any additional values
        a_list:
          - one
          - two
        …

