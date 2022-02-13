---
_alias: adding-styles
---

Adding Styles
=============

You can provide the styles for your site using either regular CSS files or
SASS/SCSS ones. To add the styles, you only have to add them to your templates.
For instance, if your file tree looks like:

    /
    └── static/
        ├── one.css
        └── two.scss

Then, you can refer to those files like in this example:

    <!DOCTYPE html>
    <html lang="en">
        <head>
            <link rel="stylesheet" href="/static/one.css">
            <link rel="stylesheet" href="/static/two.css">
        </head>
        ⋮
    </html>

Note that:

* Style files can be anywhere in the file tree.
* You can refer to them using absolute paths like in this example or relative
  ones.
* In the case of SASS/SCSS files, they get automatically converted to CSS files
  during the building process and you should link the output file in your template
  (in this case, `two.css` is used in the template and not `two.scss`).

Different Styles Per Page/Section
---------------------------------

If different parts of your site should display different styles, you have
several options:

* Using multiple templates.
* Using conditional flags inside a single template.
* Passing a list of style files to load as a variable.

### Different styles using multiple templates

You can, of course, have multiple templates defined with different sets of
style files in each one. Then from each page or section of your site you can
load the appropriate template. This option is the best approach if the templates
also change the markup in the body of the page. If you need to reuse common
parts across templates, you can make use of [template inheritance]({{
get_url('jinja-101') }}#template-inheritance-and-includes) do to so.

### Different styles using conditional flags

However, sometimes the template should be the same across pages or sections but
the set of style files to load should be different. In those cases, it can be
just easier to set the styles conditionally:
{% raw -%}
```
:::html
<!DOCTYPE html>
<html lang="en">
    <head>
        <link rel="stylesheet" href="/static/base.css">

        {% if special_styles %}
        <link rel="stylesheet" href="/static/special-styles.css">
        {% else %}
        <link rel="stylesheet" href="/static/non-special-styles.css">
        {% endif %}
    </head>
    ⋮
</html>
```
{% endraw -%}

And then, you can have `special_styles: false` at `_values.yaml` file in the
root of your site and `special_styles: true` in the directories or pages that
require different styles.

### Different styles using a list of style files

In the case of a more complicated site where the set of style files changes a
lot between sections, you can define a list of CSS files to use an override it
wherever necessary. For example, in the root `_values.yaml` file, you can have:

    css_files:
      - /styles/css/reset.css
      - /styles/css/base.css
      - /styles/css/cusomization.css

And load them your template with:

{% raw -%}
```
{% for css_file in css_files %}
<link rel="stylesheet" href="{{ css_file }}">
{% endfor %}
```
{% endraw -%}

With this setup, you can override the list at any point in the site by
redefining the `css_files` variable:

    css_files:
      - /styles/css/some-different-file.css
      - /styles/css/even-another-different-file.css

Or by adding files to the default one by using the double underscore syntax to
alter variables:

    __css_files:
      operation: append
      value:
        - /static/css/added-styles.css

SASS/SCSS Imports
-----------------

You can also make use of the
[@import](https://sass-lang.com/documentation/at-rules/import) rule inside your
SASS/SCSS files. This allows you to load common variables, mixins or functions
that you can reuse across style files.

Import filenames in SASS/SCSS start with an underscore, which is very convenient
as Scaffolding will ignore them during the build process and not try to convert
them as standalone style files. However, they will still be picked up during the
generation of the final CSS files for the site.

For example, if you have these files:

    /
    └── static/
        ├── _colors.scss
        └── styles.scss

You can define variables in `_colors.scss`:

    $primary-color: #CE2D2D;
    $secondary-color: #387077;

And then reuse them in `styles.scss`:

    @import 'colors';

    a
    {
        color: $primary-color;

        &:hover
        {
          color: $secondary-color;
        }
    }

Note that when you import a file, you let out the starting underscore out. Also,
here, both files are in the same directory, but they don't have to be. They may
not even be inside the same Spekulatio [Input Directory]({{
get_url('docs') }}#input-directories). You only have to specify the path of the
imported file relative to the final location of the importing file.

#### Importing Spekulatio variables

In Spekulatio, you can import the value of a variable from a SASS/SCSS file too.
Taking the previous example, if you have:

    @import 'colors'

in your styles file, you don't necessarily have to create a `_colors.scss` file,
but can define the content in a Spekulatio variable inside a `_values.yaml`
file:

    colors: |
      $primary-color: #CE2D2D;
      $secondary-color: #387077;

The only requirement for this variable to be accessible from the SASS/SCSS file
is that it is defined in one of its ancestor directories.

!!! Note

    If both a variable and a file are defined with the same name, `@import`
    will give precedence to the variable.

