---
_alias: spekulatio.yaml
article_classes: reference-page
---

spekulatio.yaml
===============

The `spekulatio.yaml` file allows you to configure the location of the output
directory and the list of input directories to be used. You can also specify
custom sets of actions to be applied to them and even define new filetypes.

You only have to provide a `spekulatio.yaml` file when the structure and actions
associated to the [default directories](/docs/#default-input-directories)
searched by Spekulatio are not enough for your project.

!!! Note "Using `spekulatio.yaml` to load a theme"

    A typical case in which it may be necessary to use a `spekulatio.yaml` file is
    when you want to use an external theme. A theme is just an input directory
    that contains templates, styles and JavaScript files that you
    can reuse across projects. Unless you place the files of the theme in the
    default `templates` directory, you'll need to specify its path in the
    `spekulatio.yaml` file. An example of this is the built-in, basic [theme]({{
    get_url('theme') }}) provided by Spekulatio.

This example shows every possibility of this configuration file:

    output_dir: /tmp/some/folder/
    filetypes:
      - name: temp_dir
        regex: ^temp/.*$
      - name: temp_files
        regex: ^temp-.*$
        scope: filename
      - name: txt
        extensions: ['.txt']
    input_dirs:
      - path: foo/
        preset: site_content
      - path: bar/
        preset: site_templates
      - path: baz/
        preset: base
        actions:
          - filetype: txt
            action: render
          - filetype: temp_dir
            action: ignore
          - filetype: temp_files
            action: ignore
          - filetype: yaml
            action: render
        default_action: copy

This is a description of each option:

» `output_dir`
--------------

> *Mandatory*

Directory where the final site will be generated. It can be any path in the
filesystem. Make sure you use an empty directory for the output directory as any
file inside it can potentially be overwritten with the contents of the site.
Also, since Spekulatio doesn't delete the previous contents of the output directory
automatically, any files already there will be present in the generated site
itself.

» `filetypes`
-------------

> *Optional*

Allows to create set of files to which later assign `actions`. You can create
them by passing either a list of file extensions or a regular expression.

When you pass a list of extensions:

    filetypes:
      - name: txt
        extensions: ['.txt', '.text']

any file that matches one of them will be included in that filetype.

When you pass a regular expression, you can match the pattern either against
the path of the file (relative to the root of the input directory) or just its
filename. For example:

    filetypes:
      - name: temp_dir
        regex: ^temp/.*$

will match any files in a `baz/temp/` directory if `baz` is the input directory.

When you want to match only using the filename, you need to add the `scope`
entry:

    filetypes:
      - name: temp_files
        regex: ^temp-.*$
        scope: filename

This will match any file whose filename starts with `temp-` independently of its
location inside the input directory.

Once your filetypes are defined, you can use them later in the `actions`
section to assign specific actions to them inside an input directory.

There are a number of common filetypes already predefined in Spekulatio so you
don't have to define them every time. You can check the complete list at
[Filetypes]({{ get_url('filetypes') }}). Note that it is possible to redefine any
already existing filetype in Spekulatio if you need to do so.

!!! note "Important: filetype definition order matters!"

    The order in which filetypes are defined matters for files that match more
    than one of them. Place the filetypes that you want to take predecence
    first, as they are checked by Spekulatio in the same order as you provide
    them.

    For example, the file `temp/foo.txt` will be considered of filetype `temp`
    with this configuration:

        filetypes:
          - name: temp_dir
            regex: ^temp/.*$
          - name: txt
            extensions: ['.txt']

    But of filetype `txt` with this one:

        filetypes:
          - name: txt
            extensions: ['.txt']
          - name: temp_dir
            regex: ^temp/.*$

» `input_dirs`
--------------

> *Mandatory*

This is the list of the input directories where your source files live. For each
input directory, you need to specify a `path` and a set of actions to be applied
to the files inside it. The path can be located anywhere in the filesystem,
which means that the directories of a Spekulatio project don't have to
necessarily exist under a common directory (although that's the most convenient
setup when the project is under version control so all the files are inside the
same repository).

To pass a set of actions there are two possibilities, either you pass an action
`preset` or a custom list of `actions`. To pass a preset, you only have to
provide its name:

    input_dirs:
      - path: foo/
        preset: site_content

The available presets correspond to the different set of actions that are
applied in the [default directories](/docs/#default-input-directories). To see a
complete description of each preset, take a look at [Presets]({{
get_url('presets') }}).

To pass a custom list of actions, provide a list of matches between filetypes
and actions:

    input_dirs:
      - path: baz/
        preset: base
        actions:
          - filetype: txt
            action: render
          - filetype: temp_dir
            action: ignore
          - filetype: temp_files
            action: ignore
          - filetype: yaml
            action: render
        default_action: copy

The filetype name is either one of the built-in [Filetypes]({{ get_url('filetypes')
}}) or one defined by you in the `spekulatio.yaml` file itself. The action name
should be one of the available [Actions]({{ get_url('actions') }}) in Spekulatio.

The `default_action` is the action that will be applied to each file that
doesn't match any filetype. By default, this will be to ignore the file, but you
can set this to a different action (like `copy` as in this example).

In the example above, you can see how, in addition, to the list of actions a
preset is also provided. While this is not required, it is highly recommended
that you pass at least the `base` one. That will include the actions that are
needed to replicate the directory structure of the input directories and skip
files that start with underscore. You can also pass any of the other available
presets and add more actions using the `actions` list or overwrite the ones in
the preset.

