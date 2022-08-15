# -*- coding: utf-8 -*-

import os
import sys
import datetime

now = datetime.datetime.now()
author = "Christopher DeVito"
year = now.year
version = "0.1.0"
package_name = os.environ["FocalOffsetNode"]

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, project_root)

# -- General configuration ---------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx", "sphinx.ext.viewcode"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "{}".format(package_name)
copyright = "{0}, {1}".format(year, author)

# The full version, including alpha/beta/rc tags.
release = version

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "resources/README.md"]

# Suppress warnings
suppress_warnings = ["ref.python"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a
# theme further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory. They are copied after the builtin
# static files, so a file named "default.css" will overwrite the builtin
# "default.css".
html_static_path = ["_static"]

# Output file base name for HTML help builder.
htmlhelp_basename = "{}doc".format(package_name)
