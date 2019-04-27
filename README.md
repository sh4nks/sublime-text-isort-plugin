Sublime text isort plugin
====

Small plugin that adds a command to sublime which replaces the contents with
the output of the isort library. This plugin is just a wrapper around the
isort library, thus if you want to know how isort works, visit the libraries
GitHub page [here][isort].

## Install

### Package Control

Available via [package control][package-control].  Just bring up the package
control menu in sublime (default `ctrl-shift-p`), and enter
`Package Control: Install Package`, search for `isort`.

### Manual

Clone this repository into the ``Packages`` folder of Sublime Text:

```
$ cd ~/.config/sublime-text-3/Packages
$ git clone https://github.com/thijsdezoete/sublime-text-isort-plugin
```

[isort]: https://github.com/timothycrosley/isort
[package-control]: https://github.com/wbond/package_control_channel

Using isort
===========

Bring up the command palette (default: `ctrl-shift-p`) and search for
`ImportSort`, next hit enter and you will see that your imports have been
sorted.


Configuring isort
=================

If you find the default isort settings do not work well for your project, isort provides several ways to adjust
the behavior.

To configure isort for a single user create a \~/.isort.cfg file:

    [settings]
    line_length=120
    force_to_top=file1.py,file2.py
    skip=file3.py,file4.py
    known_standard_libary=std,std2
    known_third_party=randomthirdparty
    known_first_party=mylib1,mylib2
    indent='    '
    multi_line_output=3
    length_sort=1

You can then override any of these settings by using command line arguments, or by passing in override values to the
SortImports class.

Example
=======

Before isort:

    from my_lib import Object

    print("Hey")

    import os

    from my_lib import Object3

    from my_lib import Object2

    import sys

    from third_party import lib15, lib1, lib2, lib3, lib4, lib5, lib6, lib7, lib8, lib9, lib10, lib11, lib12, lib13, lib14

    import sys

    from __future__ import absolute_import

    from third_party import lib3

    print("yo")

After isort:

    from __future__ import absolute_import

    import os
    import sys

    from third_party import (lib1, lib2, lib3, lib4, lib5, lib6, lib7, lib8,
                             lib9, lib10, lib11, lib12, lib13, lib14, lib15)

    from my_lib import Object, Object2, Object3

    print("Hey")
    print("yo")
