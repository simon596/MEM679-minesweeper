# MEM679-minesweeper

## Cross-platform operations
We set left-click to open a box and right-click to flag a box as usual. To accommodate both MacOS and Windows operation systems, <b/>"Chording" functionality</b> is added, which means <u/>when the number of flags around a revealed cell matches its adjacent mine count</u>, players can reveal multiple cells efficiently by <b/>Shift+left-click</b>. The traditional way to trigger the "chording" is by clicking both the left and right mouse buttons simultaneously, which ends up impossible for MacOS users.

## highlights of programming
Absolute Imports:
Using absolute imports ensures that modules are imported based on their full package path (src.module), eliminating ambiguity.
It avoids issues related to the module's __name__ and __package__ attributes.

Separate Entry Point:
By having main.py outside the src package, we avoid running a module inside the package directly.
This prevents conflicts with the module namespace and ensures that imports work correctly.

Module Initialization:
When you import src.gui in main.py, Python initializes the src package properly.
All modules within src can use absolute imports without issues.