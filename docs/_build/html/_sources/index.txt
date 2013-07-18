.. Robot Table documentation master file, created by
   sphinx-quickstart on Wed Jun 26 08:23:31 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Robot Table's documentation!
=======================================

The initial robot table project was realized by Leshi Chen, at Lincoln University. He implemented a set of toolkits in C# (Network, Robot Tracking, Game Management and Communication) to support distributed multiplayer RoboTable game development.

An other project (realized by Arnaud Chen-yen-su) was to port the toolkits on a Raspberry Pi. The easiest way proved to be to rewrite the toolkits in python.

This documentation is all about Arnaud's project and how to use the software on a Raspberry Pi.

User Guide
----------

This part of the documentation explain how the software works
and how to run the game example on your own robot table.

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/quickstart

Developer Guide
---------------

This part of the documentation explain how to write a new game
using the existing scripts.

.. toctree::
   :maxdepth: 2

   developer/intro
   developer/install
   developer/quickstart

API Documentation
-----------------

This part of the documentation detailed every function, class or method
used for the Robot Table Project.

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

