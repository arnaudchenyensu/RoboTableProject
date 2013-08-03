.. Robot Table documentation master file, created by
   sphinx-quickstart on Wed Jun 26 08:23:31 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Robotable's documentation!
=====================================

In 2002, Lincoln University, with the collaboration of Tufts University, started to develop a Robotable environment to enhance learning about robotics and engineering problem solving.

A Robotable is a tabletop that acts as a rear-projection screen. A picture is projected on it using a mirror (45 degrees inclined) and a projector. The system is completed by an optical tracking system used to detect interaction on the tabletop.

In 2012, Leshi Chen, a master student at Lincoln University, worked to improve the Robotable environment. His goal was to facilitate the use of Robotables by providing a set of toolkits (in C#) for setting-up and creating easily new games.

My project was to port Leshi's toolkits to a more portable computer: a Raspberry Pi. With a Raspberry Pi, setting-up Robotables environment will be easier thanks to its low price and small size. In fact, rather than using a standard computer (with a monitor, keyboard...) we will be able to use a computer with the size of a credit card.

The easiest way to port the toolkits was to rewrite them in another programming language: Python.

This documentation explains how to use the software on a Raspberry Pi.

User Guide
----------

This part of the documentation explains how the software works
and how to run the game example on your own robot table.

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/quickstart

Developer Guide
---------------

This part of the documentation explains how to write a new game
using the existing scripts.

.. toctree::
   :maxdepth: 2

   developer/create_new_game

API Documentation
-----------------

This part of the documentation details every function, class or method
used for the Robot Table Project.

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

