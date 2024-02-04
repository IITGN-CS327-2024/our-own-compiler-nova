# Nova Language Documentation

## Strings
### Bool Type: Nova Lang General Syntax

In Nova language, each statement must end with a semicolon(;), it can be a declaration of a variable, conditional statements, loops, print, and so on. Moreover, throughout the documentation, if something like `<xyz>` is encountered, then it is a placeholder where xyz specifies what it should be.

### Types

Nova lang would support three types, namely numbers, booleans, and string. The numbers are defined as `int`, booleans as `bool`, and strings as `string`. Further, the number could be extended to float to store floating point numbers such as 1.04, but as of now, we have not included float data type.

```nova
Integer   | Bool    | String
--------- | ------- | ------
int       | bool    | string

There are only two boolean types: true and false.

Variable Declaration
Variables in Nova can be declared using the var keyword followed by the declaration of the type (int, string, bool) and its name. One thing to note: it is also necessary to initialize the variable, and once a variable is declared, it cannot be redeclared in any of the scopes(same or child). By default, all the variables in Nova are mutable, but only the same type of values can be assigned if needed; otherwise, it will throw an error.

var <type> <variable_name> = <value>;
