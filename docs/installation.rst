.. _installation:
============
Instructions on Installation
============

Clone from Github:
============

To install the current minesweeper game, pick a directory and git clone the source code to your local repository:

.. code-block:: bash

   git clone https://github.com/simon596/MEM679-minesweeper.git

Create a virtual environment:
============

To prevent potential version conflicts of some libraries, it is highly recommended that you create a python virtual environment for running the game. 
Here we shows how to do so by using Anaconda to manage the libraries.

.. code-block:: bash

   conda create -n minesweeper

Make sure that you are working in the root directory, where the requirements.txt exists. The dependent Python libraries can be quickly installed by running

.. code-block:: bash

   pip install -r requirements.txt



Verification
============

To test whether the installation is successful, one quick way would be entering the following in the terminal under the root directory:

.. code-block:: bash

   tox

This will automatically go through all the test codes for the source code files of the building blocks of the minesweeper game.


Dependencies
============

My Project mainly depends on:

- pygame
- pyscaffold

Ensure these core libraries are installed correctly in your environment.

