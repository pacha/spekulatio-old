---
_alias: presets
article_classes: reference-page
---

Presets
=======

Each input directory in Spekulatio is assigned a set of **actions**. These
actions determine how each filetype in that directory will be processed. In
Spekulatio, you can create a set of actions from scratch, use an action
**preset** (which is a predefined set of actions) or use a combination of both
(select a preset and override the actions for certain filetypes).

This is the list of available action presets. Check the section
[spekulatio.yaml]({{ get_url('spekulatio.yaml') }}) to see how to assign a preset or
a combination of a preset and some overriding actions to an input directory.

» `base`
--------

Basic preset that you can use as base to define your own set of actions. It
contains the essential actions for Spekulatio to work. All the following presets
include this one implicitly.

| Filetype              | Action      |
| --------------------- | ----------- |
| Pattern `_*`          | ignore      |
| Pattern `*.meta.yaml` | md_to_html  |
| Directories           | create_dir  |

*Default action*: `ignore`

» `site_content`
----------------

This preset is useful for input directories that generate HTML pages from other
formats (Markdown, reStructuredText, …) and that don't contain HTML templates.
It is the preset used for the `content` default input directory.

| Filetype    | Action          |
| ----------- | --------------- |
| html        | html_to_html    |
| md          | md_to_html      |
| rst         | rst_to_html     |
| json        | json_to_html    |
| yaml        | yaml_to_html    |
| sass        | sass_to_css     |

*Default action*: `copy`

» `site_templates`
------------------

This preset is useful for input directories that contain HTML templates static
assets such as SASS/SCSS/CSS, JS or images. It is very similar to `site_content`
but HTML files are not considered content themselves but treated as templates.
This is the preset used for the `templates` default input directory.

| Filetype    | Action            |
| ----------- | ----------------- |
| html        | use_as_template   |
| md          | md_to_html        |
| rst         | rst_to_html       |
| json        | json_to_html      |
| yaml        | yaml_to_html      |
| sass        | sass_to_css       |


*Default action*: `copy`

» `site_data`
------------------

This preset is useful for input directories where the files have to be copied
over to the final site without modification. It is the preset used for the
`data` default input directory.

*Default action*: `copy`

