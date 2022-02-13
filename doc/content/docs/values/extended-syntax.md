---
_alias: advanced-syntax
---

Extended Syntax
===============

Every time you define a value in Spekulatio, by default, it is inherited by all
children pages and directories and it replaces any value could have been defined
with the same name previously. The **extended syntax** for values allows you to
define both the scope of a variable (whether or how much it should be inherited)
and what to do if a variable with the same name existed before.

While the regular syntax for a variable is:

    <name>: <value>

The extended syntax has the form:

    __<name>:
      operation: replace|append|merge|delete
      scope: local|level|branch
      value: <value>

As you can see, the extended syntax is prefixed with two underscores and allows
you to pass a dictionary that defines the variable behavior in detail. Note that
the two underscores are only necessary during the definition, **in templates,
the variable is used without them** (ie. just as `<name>`).

These are the possible options to use:

* `operation` lets you define what to do with the variable if it existed
  previously.

    - `replace` is the default option, it means that the new value will replace
      any existing one with the same name.
    - `append` applies only to lists and adds the list provided in `value` to
      the existing one.
    - `merge` is similar to `append` but it applies to dictionaries, it will
      merge the dictionary provided in `value` to the already existing one.
    - `delete` removes the value altogether (you can't provide a `value` in this case).

* `scope` controls how the value will be inherited by descendant pages. It only
  makes sense inside `_values.yaml` files since values defined in a
  front-matter are not inherited by any other page.

    - `local`: the value won't be inherited by any children of the directory.
    - `level`: makes the value to be set in the directory and all the direct
      descendants (one level).
    - `branch`: is the default one and makes the value to be recursively set in
      every descendant of the current directory.

* `value` is the actual value to use by the selected `operation`.

!!! note "Extended syntax and special values"

    Note that the extended syntax can't be used with [special values]({{
    get_url('special-values') }}) since they have fixed values for both their
    operations and scopes.

Some examples
-------------

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

