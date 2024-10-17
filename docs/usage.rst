.. _usage:
===========
Game's rule and usage
===========

Quick start
===========

Here's how to play the Minesweeper:
make sure you are in the roor directory "./MEM679-minesweeper/". 
The entry point is main.py in the root directory. First, activate the virtual environment

.. code-block:: bash

   conda activate minesweeper


Once you are in the corresponding virtual environment, type

.. code-block:: bash

   python main.py

to enter the GUI of the game

Cross-platform operations
===========

We set left-click to open a box and right-click to flag a box as usual. To accommodate both MacOS and Windows operation systems, 
"Chording" functionality is added, which means when the number of flags around a revealed cell matches its adjacent mine count, 
players can reveal multiple cells efficiently by Shift+left-click. The traditional way to trigger the "chording" is by clicking both the left and right mouse buttons simultaneously, 
which ends up impossible for MacOS users.

Highlights
===========

Absolute Imports:
Using absolute imports ensures that modules are imported based on their full package path (src.module), eliminating ambiguity.
It avoids issues related to the module's __name__ and __package__ attributes.

Separate Entry Point:
By having main.py outside the src package, we avoid running a module inside the package directly.
This prevents conflicts with the module namespace and ensures that imports work correctly.

Module Initialization:
When you import src.gui in main.py, Python initializes the src package properly.
All modules within src can use absolute imports without issues.



For more details of module explaination and usage, see the API documentation.
