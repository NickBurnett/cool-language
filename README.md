# **OPL Project**
## **Part 1**
### *State Transition Diagram*
The state transition diagram is provided with the repository download as a PDF.
### *Language Changes*
The main changes to the language are the addition of three operators:
- Prefix/Postfix increment operator
- Prefix/Postfix decrement operator
- Swap operator

The lexer takes these lexemes (++, --, <->) into account when reading the input.
### *Running the Lexer*
The lexer has been tested on Python v3.7.3, and provides 4 unit-tests in the `tests.py` source. To execute the unit-tests, run `python -m unittest tests.py` after installing the necessary package (`pip3 install unit`).

To lex a single program, first write the program in the `programs/` directory, and name the program `<name>.txt`. To lex the program, run `python driver.py <name>`. The driver program will automatically fetch the correct program file from the `programs/` directory.