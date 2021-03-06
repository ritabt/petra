# Petra [![Build Status](https://travis-ci.org/StanfordLegion/petra.svg?branch=master)](https://travis-ci.org/StanfordLegion/petra)

A compiler for Petra programs that emits LLVM.

# Setup

## Dependencies

  - Python >= 3.7
  - [llvmlite](https://github.com/numba/llvmlite)

## Quickstart

```
source setup.sh
pip install -e .
./run_tests.sh
```

## Installation

### With Conda

 1. Create a Conda environment with `source setup.sh`.
 2. Locally install Petra for development with `pip install -e .`.
 3. *Optional:* Install development tools (e.g. mypy) with
    `pip install -r requirements-dev.txt`.

### With Virtual Env

 1. Create a virtual environment with `python3 -m venv venv`.
 2. Enter the virtual environment with `source venv/bin/activate`.
 3. Locally install Petra for development with `pip install -e .`.
 4. *Optional:* Install development tools (e.g. mypy) with
    `pip install -r requirements-dev.txt`.

## Use

 1. Write a Petra program. `import petra` to use the Petra library.
 2. Typecheck your program with `mypy <program name>.py`.
 3. If your program is a test, add it to the tests/ directory and write test
    cases in a format similar to other tests in the directory.
 4. Run all tests with `./run_tests.sh`.

## Troubleshooting

Sometimes you may want to compile the emitted LLVM manually.

 1. Generate llvm bytecode by writing a Python file that uses the Petra library
    and calling `petra.Program.to_llvm()`.
 2. `llc --mtriple=<target-architecture> <llvm-file>` (for target architecture,
    on Linux 64-bit try `x86_64-unknown-linux-gnu`, and on macOS try
    `x86_64-apple-darwin18.7.0`)
 3. Assemble and link to create an executable.

# Background

Petra code is also Python code - every piece of syntax is actually a call to a
Python function in the Petra library. Assuming that the code abides by the type
hints written for each function (which can be verified with mypy), when each
piece of syntax is constructed, it checks that its arguments are legitimate.
When each function is constructed, it typechecks its statements. This means that
if Python can execute your Petra code, then it is valid Petra code!

If your program typechecks, you can programmatically compile your program to
LLVM bytecode or JIT it to call it from other Python code. See the `to_llvm()`
and `compile()` methods of `Petra.program`.

# Petra Programming Language Reference

Petra takes some inspiration from the C programming language and implements a
subset of it, so much of the syntax discussed may be familiar.

## Types

Petra currently supports 4 types, all of which are primitive.

  * `petra.Int8_t`: A 8-bit integer type.

  * `petra.Int32_t`: A 32-bit integer type.

  * `petra.Float_t`: A single-precision float type. No operations have
    been implemented on floats yet - it was introduced for extern
    compatibility.

  * `petra.Bool_t`: A boolean type.

### Function types

Two metatypes are defined for the inputs and outputs of a function.

  * `petra.Ftypein`: This is equivalent to Tuple[Type, ...], which
    means a possibly-empty tuple of types.

  * `petra.Ftypeout`: This is equivalent to Union[Tuple[()], Type],
    which means either the empty tuple (void, which is otherwise not a
    valid type) or a single type.

## Programs

  * `petra.Program(name: str)`

    Creates a program with the given name.

  * `petra.Program.add_func_decl(name: str, t_in: Ftypein, t_out: Ftypeout)`

    Declares an extern function (for typechecking reasons) that can be
    called from Petra code.

  * `petra.Program.add_func(name: str, args: Tuple[Declare, ...], t_out: Ftypeout, block: Block)`

    Adds a function with the given name, declaration, and content to
    the program, then returns the program (for easy chaining).

  * `petra.Program.to_llvm()`

     Returns an unoptimized LLVM representation of the program as a string.

  * `petra.Program.save_object(filename: str)`

     Saves an unoptimized object file of the program suitable for
     passing to the platform linker.

  * `petra.Program.compile()`

    Returns a MCJIT execution engine with the program loaded. See
    tests for an example of how to use this.

## Blocks

  * `petra.Block(statements: List[Union[Expr, Statement]])`

     Creates a block of statements. Used in other control flow
     constructs and in function bodies.

## Statements

  * `petra.If(pred: Expr, then_block: Block, else_block: Block)`

    Creates an if-else statement predicated on the given
    expression. The then and else clause can be empty.

  * `petra.Call(name: str, args: List[Expr])`

    Creates a function call statement to a function that was either
    declared extern or previously added to the program.

  * `petra.DefineVar(symbol: Symbol, value: Expr)`

    Defines a new variable. Variables with the same symbol cannot be
    redeclared within a scope (defined by a function or an if/else
    clause).

  * `petra.Assign(var: Var, value: Expr)`

    Creates an assignment statement assigning the expression to either
    to an existing variable.

  * `petra.Return(e: Union[Tuple[()], Expr])`

    Creates a return statement that returns either nothing or an
    expression.

## Symbols

  * `petra.Symbol(type_: Type, name: str)`

    Creates a symbol, which can be used in variable declarations,
    assignments or when adding parameters to a function. The name must
    pass the regex `r"^[a-z][a-zA-z0-9_]*$"`. Note that the name is
    only used for display to humans and that every symbol is unique
    regardless of name. Two (or more) symbols with the same name can
    be defined in the same scope, but a given symbol may be defined in
    a scope only once.

## Expressions

### Variables

  * `petra.Var(symbol: Symbol)`

    Creates a variable reference to an argument or previously declared variable.

### Constants

  * `petra.Int8(value: int)`

     Creates an `Int8_t` constant.

  * `petra.Int32(value: int)`

    Creates an `Int32_t` constant.

  * `petra.Float(value: float)`

    Creates a `Float_t` constant.

  * `petra.Bool(value: bool)`

    Creates a `Bool_t` constant.

### Arithmetic

  * `petra.Add(left: Expr, right: Expr)`

    Creates a addition of two arithmetic expressions.

  * `petra.Sub(left: Expr, right: Expr)`

    Creates a subtraction of two arithmetic expressions.

  * `petra.Mul(left: Expr, right: Expr)`

    Creates a multiplication of two arithmetic expressions.

  * `petra.Div(left: Expr, right: Expr)`

    Creates a division of two arithmetic expressions.

  * `petra.Mod(left: Expr, right: Expr)`

    Creates a division remainder of two arithmetic expressions.

### Comparison

  * `petra.Lt(left: Expr, right: Expr)`

    Creates a less-than comparison between two arithmetic expressions.

  * `petra.Lte(left: Expr, right: Expr)`

    Creates a less-than-or-equal comparison between two arithmetic expressions.

  * `petra.Gt(left: Expr, right: Expr)`

    Creates a greater-than comparison between two arithmetic expressions.

  * `petra.Gte(left: Expr, right: Expr)`

    Creates a greater-than-or-equal comparison between two arithmetic expressions.

### Equality

  * `petra.Eq(left: Expr, right: Expr)`

    Creates an equality check between two expressions.

  * `petra.Neq(left: Expr, right: Expr)`

    Creates an unequality check between two expressions.

### Logical

  * `petra.And(left: Expr, right: Expr)`

    Creates a short-circuiting boolean and of two boolean expressions.

  * `petra.Or(left: Expr, right: Expr)`

    Creates a short-circuiting boolean or of two boolean expressions.

  * `petra.Not(e: Expr)`

    Creates a boolean not of a boolean expression.

## Errors

  * `petra.ValidateError`

    An exception thrown if Petra code does not confirm to certain
    structural checks such as a variable name conforming to a regex.

  * `petra.TypeCheckError`

    An exception thrown if Petra code fails to typecheck.

# Design and Implementation

The static checks and compilation of Petra are completed in stages.

Static errors are checked upon construction of all Petra syntax and will throw a
StaticException if any are found.

Typechecking occurs each time a function is added to the program. A TypeContext
is constructed using the set of extern functions declared, the set of previously added functions, and an empty variable type context. All statements in the program are sequentially type-checked.

Code generation also occurs each time a function is added to the program.
llvmlite is liberally used to simplify construction of basic blocks, and a
codegen context is passed along to help resolve internal references to variables
and functions.

Petra includes a testing framework built upon Python's unittest. By taking
advantage of the LLVM MCJIT execution engine and Python's ctypes, it's possible
to run Petra functions from Python which eases testing. Static and type
exceptions can also be caught and verified to be thrown for invalid programs.

# Limitations

Petra is incomplete, and programming features are still missing. Here's a
partial list:

  - types:
      - more basic types (signed and unsigned int8/16/32/64, float32/64)
      - aggregate types (arrays and structs)
      - strings
  - control flow:
      - loops
      - elseif
  - pointers, reference/dereference, l-values
  - floating point arithmetic
  - casting between types

In addition, parts of Petra infrastructure could be improved:

  - Some error messages could be reworded or tested due to lack of usage.
  - Petra's testing framework, while decently robust, is missing a lot
    of tests.  An unfortunate side-effect is that there may be latent
    bugs in the compiler as well.
  - Run optimizations on the generated code.
  - Generate debug symbols in the generated code.

# Acknowledgements

Petra was initially designed and built by [Andrew
Benson](https://github.com/anbenson) in Fall 2019 with the helpful guidance of
Elliott Slaughter. Professor Alex Aiken served as advisor.
