.. matpLaTeX documentation master file, created by
   sphinx-quickstart on Thu Sep 12 16:52:38 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

matpLaTeX documentation
=======================

**MatpLaTeX** is lets you export your matplotlib figures with all the text in a separate LaTeX file. 

.. note::

   This project is still in development. Different versions may not be compatible.

Basic usage
-----------

Saving a figure:

.. code-block:: python

   import matplotlib.pyplot as plt
   import matplatex

   fig = plt.figure()
   # Add stuff to the figure.

   matplatex.save(fig, 'myprettyfig')

Using the saved figure in LaTeX:

.. code-block:: latex

   % Preamble
   \usepackage{tikz}
   \newlength{\figurewidth}
   \newlength{\matplatextmp}

   % ...

   % Document body
   \setlength{\figurewidth}{.8\linewidth}
   \input{myprettyfig.pdf_tex}

It's that simple! Check the :doc:`usage` section for more options.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   api

