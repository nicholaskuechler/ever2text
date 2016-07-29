ever2text
=========

Convert Evernote exports to plain text files.

The goal is to export Evernote notes to raw text files for use with any
text editor, such as `Atom <https://atom.io/>`_ or
`Sublime Text <https://www.sublimetext.com/>`_.

GitHub for ever2text: `https://github.com/nicholaskuechler/ever2text <https://github.com/nicholaskuechler/ever2text>`_

If you are looking to export Evernote notes for use with SimpleNote, have a
look at `ever2simple <https://github.com/claytron/ever2simple>`_.

Installation
------------

Install using ``pip`` (preferably in a virtualenv):

::

    $ pip install -U ever2text

Development Installation
------------------------

Clone this repository with ``git``:

::

    $ git clone https://github.com/nicholaskuechler/ever2text.git
    $ cd ever2text
    $ python setup.py install

Usage
-----

First you will need to export your notes from inside of the Evernote
application. For each notebook, right click the notebook name and select the
"Export Notes" option. Make sure to select the ``enex`` format.

IMPORTANT: You need to export each notebook individually. I could not find an
option to export all notebooks in to a single Evernote export file. Make sure
to give each exported notebook a unique name. I used the notebook name as the
basis for the exported enex dump file.

Once you have created an export file, you can run the script on the file
setting the ``--output`` to a directory:

::

    $ ever2text my_notebook.enex --output output_directory --format text

You can export notes to either plain text or markdown format. The default is
plain text. For markdown formatted notes, use ``--format markdown``.

::

    $ ever2text my_notebook.enex --output output_directory --format markdown

Notes and Caveats
-----------------

- Each Evernote notebook needs to be exported individually. It does not appear
  you can export all notebooks in to a single export file.

- Notes are created with a number suffix to avoid collisions when multiple
  notes have the same title.

- If a title cannot be sanitized, the note will have a default title of
  ``title_fail-NUMBER.txt``

- Converting notes to text will not preserve tags in the notes.

- This does not handle any attachments.

Credits
-------

Based on ever2simple by Clayton Parker: https://github.com/claytron/ever2simple
