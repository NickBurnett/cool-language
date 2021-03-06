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
The lexer has been tested on Python v3.7.3, and provides 4 unit-tests in the `tests.py` source. To execute the unit-tests, run `python -m unittest tests.py` after installing the necessary package (`pip3 install unit`). ***Note***: This functionality is now deprecated, as the unittests are deleted (no use for grading).

To lex a single program, first write the program in the `programs/` directory, and name the program `<name>.txt`. To lex the program, run `python driver.py <name>`. The driver program will automatically fetch the correct program file from the `programs/` directory.

## **Part 2**
### *Language Changes*
The main changes to the language are the removal of the swap operator '<->' and removal of the prefix/postfix increment and decrement operators. In addition to those changes, I have added a shift keyword that will shift the first ID argument a number of times given by an expression.

### *Running the Parser*
The parser has been tested on Python v3.7.3, and provides no unit tests. The parser and lexer sources have been moved to the `interpreter` directory. To execute the parser, run the driver file in the root directory, `driver.py` with the program argument in the programs folder. An example might be program b, executing the command `python driver.py b` which would then output whether the program is in the language or not. In addition, you may choose to run the parser against a program that is not in the language specified. Program d is an example of this. Execute the command `python driver.py d` and observe that the parsing fails because the second print statement doesn't end in a semi-colon.

## **Part 3**
### *Program Changes*
Note that all programs should now be fully functioning, and should pass the lexing, parsing, and interpretation phases.

### *Language Changes*
The main changes to the language are the addition of the println keyword and the changing of the order of precedence. The order of precedence is as follows (highest to lowest):
- neg
- not
- ">", ">=", "<", "<=", "==", "!="
- and, or
- "*", "/", "%"
- "+", "-"

### *Parser Changes*
The parser now implements static semantics using the store system. Whenever a new scope is entered, a new store is pushed onto the stack to handle any variable definitions. A variable will modify variables in the outer scopes if it is already defined. If not, then the variable will be defined in the inner scope. Once a scope is exited, the store will be popped off of the stack, restoring the parent scope as the inner scope. The parser inmplements the static semantic checking at parse-time, and the interpreter implements scoping in if and while statements.

### *Running the Interpreter*
The interpreter has been tested on Python v3.7.3 and provides no unit tests. The interpreter is located in the `interpreter` directory. The exeute the interpreter, run the driver file in the root directory, `driver.py` with the program argument in the programs folder. An example might be program b, executing the command `python driver.py b` which would then execute the specified program.