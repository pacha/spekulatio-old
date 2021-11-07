
Theme Styles
============

The Spekulatio theme allows you to customize which stylesheets are loaded by
means of the `_css_files` list. You can overwrite or modify its value from any
node of your site. Its default value is:

    _css_files:
      - /static/css/normalize.css
      - /static/css/spekulatio.css

The first entry, `normalize.css`, resets all the default styles so they look the
same across browsers. The second one, `spekulatio.css`, contains the styles of
the Spekulatio theme itself.

If you want to keep most style definitions but want to modify some, instead of
completely redefining the variable, you can use the double underscore notation
to add new entries to the list while leaving the ones already defined in place:

    __css_files:
      operation: append
      value:
        - /static/css/my-styles.css

After this, the value of `_css_file` will be:

    _css_files:
      - /static/css/normalize.css
      - /static/css/spekulatio.css
      - /static/css/my-styles.css

and whatever you add to `my-styles.css` will take preference over the
definitions in the other files.

You can change the `_css_files` variable in the front matter of a content
file if you want the change to only affect that file in particular, or in the
`_values.yaml` file of any directory if you want the change to affect all the
pages under it. For example, if you add the snippet above to the `_values.yaml`
file at the root of your content, the `my-styles.css` file will be loaded in
every page of the site.

Since the value of `_css_files` is a list, you can add more than one entry.
Entries can be either external stylesheets (ie. an external link) or files
inside your project. For example, to load a font from Google Fonts —_Lato_ in
this example—, you can do something like:

    __css_files:
      operation: append
      value:
        - https://fonts.googleapis.com/css?family=Lato:400,400i,700
        - /static/css/my-styles.css

where the `my-styles.css` file would contain something along the lines of:

    html
    {
        font: 16px/1.4 'Lato', Helvetica, Arial, sans-serif;
    }

For style files inside your project, you can freely decide on their name and
location. Just remember that the filenames to provide in this list are those of
the generated files. For instance, if you add `my-styles` to your project as a
SASS/SCSS file (eg. `my-styles.scss`), you will still list it as `my-styles.css`
in the `_css_files` variable.

Color variables
---------------

Adding extra CSS files to your project allows you to add or override any
pre-existing styles. However, changing the overall scheme color that way would
require to override each HTML element style that uses one of the colors of the
theme. Fortunately, Spekulatio defines the colors of the theme by just adding a
file to your project:

    /static/css/_colors.scss

If you provide a file at the same location in your content directory (or
any other input directory provided after the theme), your definition will
override the default one.

For example, if you add a `/static/css/_colors.scss` file with the following
contents, your site with adapt a _dark_ style:

    // page background
    $background-color: #333333;

    // surface boxes such as <code> blocks or <footer>
    $surface-color: lighten($background-color, 12%);

    // normal text
    $text-color: #FEFEFE;

    // alternative text color (eg. main menu items)
    $text-color-companion-shade: #FFFFFF;

    // primary accent color (eg. links)
    $primary-color: #EE6457;

    // companion shade for the primary accent color (eg. main menu item hover)
    $primary-color-companion-shade: #14A7B9;

    // secondary accent color (eg. inline code text)
    $secondary-color: #FFFFFF;

    // companion shade for the secondary accent color (eg. background of inline code)
    $secondary-color-companion-shade: #595959;

Independently of whether you override this file or not, you can use the color
definitions in any SASS/SCSS file by importing them:

    @import 'colors';

Since Spekulatio can import SASS/SCSS definitions from values, you can
alternatively override the colors in a front matter or in a `_values.yaml` file
(note the YAML pipe notation as the value that you pass is a multiline string
literal):

    colors: |
      $background-color: #333333;
      $surface-color: lighten($background-color, 12%);
      $text-color: #FEFEFE;
      $text-color-companion-shade: #FFFFFF;
      $primary-color: #EE6457;
      $primary-color-companion-shade: #14A7B9;
      $secondary-color: #FFFFFF;
      $secondary-color-companion-shade: #595959;

The advantage of this second method is that you can define colors per directory
instead of for the entire site. So, if you need different color schemes in
different parts of your site, this is an easy way to achieve it.

!!! note

    You can override the theme colors using either a file or in a values file,
    but in both cases you need to redefine _all_ colors. In both cases, your
    text completely replaces the original definition of the colors and the build
    will fail complaining about missing colors if some of them is not defined.
