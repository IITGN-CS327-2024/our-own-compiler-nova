## Token Classification

- Keywords
> "var" | "int" | "bool" | "string" | "println" | "array" | "tuple" | "if" | "else" |
 "loop" | "true" | "false" | "fn" | "return" | "void" | "break" | "continue" | 
 "and" | "or" | "not" | "try" | "catch" | "throw" | "length" | "head" | "tail" | "cons"

This is the list of all the keywords

- Numbers
> 0 | [1-9][0-9]*

Either 0 or any number that starts with a non-zero value.

- Identifiers
> [a-zA-Z][a-zA-Z0-9]*

Identifiers starts with an alphabet and can't be same as a keyword.

- Operators
> "+" | "-" | "*" | "/" | "=" | "<" | ">" | "<=" | ">=" | "==" | "!=" | "|" | "|" | "." 

Arithmetic, logical, string, and array operators

- Logical operators
> "and" | "or" | "not"

- Whitespace
> " " | "\t"

- Left_Parenthesis
> "("

- Left_Braces
> "{"

- Left_Bracket
> "["

- Right_Parenthesis
> ")"

- Right_Braces
> "}"

- Right_Bracket
> "]"

- Symbols
> "::"

Use to differentiate from the return datatype of a function and slicing operator

- Seperators
> "," | ":"

These are used to seperate entities, e.g., numbers in a array or range in slicing operation.

- endOfStm
> ";"

Each of the statement must end with a ";"


Note: Braces represents the blocking statements start and end. bracket are used in indexing and slicing operations. Parenthesis is used in enclosing function parameters, difining values in array methods.