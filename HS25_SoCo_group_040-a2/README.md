# How to use
To use the different files, run the following commands in your terminal:

extensions.lgl

```bash
python.exe interpreter.py extensions.lgl
```
----
data_structures.lgl

```bash
python.exe interpreter.py data_structures.lgl
```
----
functional.lgl

```bash
python.exe interpreter.py functional.lgl
```
----
tracing.lgl

```bash
python.exe interpreter.py --trace tracing.lgl
```
# Design decisions
The only noteworthy design decision we made concerns the implementation of the map, reduce, and filter functions.
We decided that users should first store the function they want to apply in a variable.
When calling map, reduce, or filter, the user can then simply pass the variable name instead of writing the entire
function inline as a parameter.While this approach introduces an additional variable and one extra line of code for 
the function definition, it keeps the use of map, reduce, and filter much cleaner and easier to read.

# Prompts used
- Why does my trace output show all 0ms for "..."?
- How to implement stack structure for tracing the function calls (manually) with timer?
- In python how to implement stack without using a default stack implementation
- How to consider system args in python, when args are optional?

