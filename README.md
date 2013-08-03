Robotable Project
================

In 2002, Lincoln University, with the collaboration of Tufts University, started to develop a Robotable environment to enhance learning about robotics and engineering problem solving. 

A Robotable is a tabletop that acts as a rear-projection screen. A picture is projected on it using a mirror (45 degrees inclined) and a projector. The system is completed by an optical tracking system used to detect interaction on the tabletop.

In 2012, Leshi Chen, a master student at Lincoln University, worked to improve the Robotable environment. His goal was to facilitate the use of Robotables by providing a set of toolkits (in C#) for setting-up and creating easily new games.

My project was to port Leshi's toolkits to a more portable computer: a Raspberry Pi. With a Raspberry Pi, setting-up Robotables environment will be easier thanks to its low price and small size. In fact, rather than using a standard computer (with a monitor, keyboard...) we will be able to use a computer with the size of a credit card.

The easiest way to port the toolkits was to rewrite them in another programming language: Python. Toolkits' architecture design and the algorithm remain almost the same. The main differences are that my software does not provide the same level of details and the Network toolkit use a different architecture.

At the end, the software in Python provides almost the same result as the initial software. Nonetheless, improvements still need to be made, specially concerning the Network and Game Management toolkit.
