import os
import re
import sys

keywords = ["true", "false"]

data_type = ["int", "bool", "string"]
void = ["void"]
special_keywords = ["var", "println", "array", "tuple", "if", "else", "then", "loop", "through", "fn", "return", "try", "catch", "throw", "BREAK", "CONTINUE"]

error_type = ["TypeError", "DivisionByZeroError", "NameError", "IndexError", "e"]
operators = ["+", "-", "*", "/", "%", "==", "=", "<", ">", "<=", ">=", "!=", "!", "|", "."]
logical_operators = ["and", "or", "not"]
whitespace = [" ", "\t"]
array_op = ["length", "head", "tail", "cons"]
left_braces = ["{"]
left_parenthesis = ["("]
left_barcket = ["["]
right_braces = ["}"]
right_parenthesis = [")"]
right_barcket = ["]"]
double_colon  = ["::"]
seprator = [",", ":"]
endOfStmt   = [";"]

# keyword can be termed as idnentifiers
# identifiers can't start with a number
# if the word starts with a number then it has to be a number(partially)
# if it starts with a _ then it has to be a identifier
# if it starts with a letter then it can be a keyword or an identifier or a logical operator or array methods
# DONE: if whitespace ingore it
# if operator or bracket then self explanatory
# error must be thrown if there is 


def lexer(code : str, tokens : list):
    # print(code)
    line = code.split()
    if len(line) == 0:
        return

    string_found = False
    collect_string = ""
    comment_found = False
    for word in line:
        if comment_found == True:
            comment_found = False
            break;
        cur_pos = 0
        temp = word
        while(cur_pos < len(temp)):
            if comment_found == True:
                break
            if word in whitespace or word in "\n":
                continue

            #<---------------------string starts------------------------>

            # The whole string is in one line
            elif re.match(pattern='\"[^\"]*\"', string=word):
                match = re.match(pattern='\"[^\"]*\"', string=word)
                string_value = match.group()
                tokens.append(["STRING", string_value])
                cur_pos += len(string_value)

            # If not in one line: starts and ends somewhere else
            # Starting
            elif re.match(pattern='\"[^"]*', string=word):
                if string_found == False:
                    collect_string += word + " "
                    string_found = True
                    cur_pos += len(word)
                else:
                    collect_string += word[0]
                    tokens.append(["STRING", collect_string])
                    string_found = False
                    cur_pos += 1

            # Ending
            elif string_found and re.match(pattern='[^"]*\"', string=word):
                match = re.match(pattern='[^"]*\"', string=word)
                collect_string += match.group()
                string_found = False
                tokens.append(["STRING", collect_string])
                collect_string = ""
                cur_pos += len(match.group())

            # In between phases
            elif string_found == True:
                collect_string += word +  " "
                cur_pos += len(word)
            #<---------------------string ends------------------------>

            elif re.match(pattern="#", string=word):
                comment_found = True

            elif re.match(pattern="0|[1-9][0-9]*", string=word):
                match = re.match(pattern="0|[1-9][0-9]*", string=word)
                num_value = match.group()
                # print(num_value)
                tokens.append(["NUMBER", num_value])
                cur_pos += len(num_value)

            elif re.match(pattern="[a-zA-Z][a-zA-Z0-9]*", string=word):
                match = re.match(pattern="[a-zA-Z][a-zA-Z0-9]*", string=word)
                identifier_value = match.group()
                # print(identifier_value)
                if identifier_value in ["true", "false"]:
                    tokens.append(["BOOLEAN", identifier_value])
                elif identifier_value in array_op:
                    tokens.append(["ARRAY_OPERATION", identifier_value])
                elif identifier_value in error_type:
                    tokens.append(["ERROR_TYPE", identifier_value])
                elif identifier_value in special_keywords:
                    tokens.append([identifier_value.upper(), identifier_value])
                elif identifier_value in data_type:
                    tokens.append(["DATA_TYPE", identifier_value])
                elif identifier_value in void:
                    tokens.append(["VOID", identifier_value])
                elif identifier_value in keywords:
                    tokens.append(["KEYWORD", identifier_value])
                elif identifier_value in logical_operators:
                    tokens.append([identifier_value.upper(), identifier_value])
                    # tokens.append(["LOGICAL_OPERATOR", identifier_value])
                else:
                    tokens.append(["IDENTIFIER", identifier_value])
                cur_pos += len(identifier_value)

            elif re.match(pattern="::", string=word):
                match = re.match(pattern="::", string=word)
                symbol_value = match.group()
                # print(symbol_value)
                tokens.append(["DOUBLE_COLON", symbol_value])
                cur_pos += len(symbol_value)

            elif re.match(pattern=",|:", string=word):
                match = re.match(pattern=",|:", string=word)
                seperator_value = match.group()
                # print(seperator_value)
                tokens.append(["SEPERATOR", seperator_value])
                cur_pos += len(seperator_value)

            # plus, minus, multiply, divide
            elif re.match(pattern="\+|\-|\*|\/|\%", string=word):
                match = re.match(pattern="\+|\-|\*|\/|\%", string=word)
                operator_value = match.group()
                # print(operator_value)
                operator_to_token = {'+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'DIVIDE', '%': 'MODULO'}
                tokens.append([operator_to_token[operator_value], operator_value])
                cur_pos += len(operator_value)

            elif re.match(pattern="\=\=|\!\=|\<\=|\>\=|\<|\>", string=word):
                match = re.match(pattern="\+|\-|\*|\/|\=\=|\!\=|\<\=|\>\=|\<|\>", string=word)
                operator_value = match.group()
                # print(operator_value)
                tokens.append(["COMPARISON_OPERATOR", operator_value])
                cur_pos += len(operator_value)

            elif re.match(pattern="\=", string=word):
                match = re.match(pattern="\=", string=word)
                operator_value = match.group()
                # print(operator_value)
                tokens.append(["ASSIGN", operator_value])
                cur_pos += len(operator_value)

            elif re.match(pattern="\.", string=word):
                match = re.match(pattern="\.", string=word)
                operator_value = match.group()
                # print(operator_value)
                tokens.append(["ARRAY_OPERATOR", operator_value])
                cur_pos += len(operator_value)

            elif re.match(pattern="!", string=word):
                match = re.match(pattern="!", string=word)
                operator_value = match.group()
                # print(operator_value)
                tokens.append(["UNARY_NOT", operator_value])
                cur_pos += len(operator_value)

            elif re.match(pattern="\|", string=word):
                match = re.match(pattern="\|", string=word)
                operator_value = match.group()
                # print(operator_value)
                tokens.append(["STRING_OPERATOR", operator_value])
                cur_pos += len(operator_value)

            # elif re.match(pattern="\+|\-|\*|\/|\=\=|\!\=|\<\=|\>\=|\<|\>|\=|\.|!|\|", string=word):
            #     match = re.match(pattern="\+|\-|\*|\/|\=\=|\!\=|\<\=|\>\=|\<|\>|\=|\.|!|\|", string=word)
            #     operator_value = match.group()
            #     # print(operator_value)
            #     tokens.append(["OPERATOR", operator_value])
            #     cur_pos += len(operator_value)

            elif re.match(pattern="and|or|not", string=word):
                match = re.match(pattern="and|or|not", string=word)
                logical_operator_value = match.group()
                # print(logical_operator_value)
                tokens.append(["LOGICAL_OPERATOR", logical_operator_value])
                cur_pos += len(logical_operator_value)

            # <---------------------left parenthesis/braces/bracket------------------------>
            elif re.match(pattern="\(", string=word):
                match = re.match(pattern="\(", string=word)
                left_parenthesis_value = match.group()
                # print(left_parenthesis_value)
                tokens.append(["LEFT_PARENTHESIS", left_parenthesis_value])
                cur_pos += len(left_parenthesis_value)
            elif re.match(pattern="\{", string=word):
                match = re.match(pattern="\{", string=word)
                left_braces_value = match.group()
                # print(left_braces_value)
                tokens.append(["LEFT_BRACES", left_braces_value])
                cur_pos += len(left_braces_value)
            elif re.match(pattern="\[", string=word):
                match = re.match(pattern="\[", string=word)
                left_bracket_value = match.group()
                # print(left_bracket_value)
                tokens.append(["LEFT_BRACKET", left_bracket_value])
                cur_pos += len(left_bracket_value)

            # <---------------------right parenthesis/braces/bracket------------------------>
            elif re.match(pattern="\)", string=word):
                match = re.match(pattern="\)", string=word)
                right_parenthesis_value = match.group()
                # print(right_parenthesis_value)
                tokens.append(["RIGHT_PARENTHESIS", right_parenthesis_value])
                cur_pos += len(right_parenthesis_value)
            elif re.match(pattern="\}", string=word):
                match = re.match(pattern="\}", string=word)
                right_braces_value = match.group()
                # print(right_braces_value)
                tokens.append(["RIGHT_BRACES", right_braces_value])
                cur_pos += len(right_braces_value)
            elif re.match(pattern="\]", string=word):
                match = re.match(pattern="\]", string=word)
                right_bracket_value = match.group()
                # print(right_bracket_value)
                tokens.append(["RIGHT_BRACKET", right_bracket_value])
                cur_pos += len(right_bracket_value)

            elif re.match(pattern=";", string=word):
                match = re.match(pattern=";", string=word)
                endOfStream = match.group()
                # print(endOfStream)
                tokens.append(["END_OF_STMT", endOfStream])
                cur_pos += len(endOfStream)
            else:
                # print("Token:", word)
                tokens.append(["INVALID", word])
                cur_pos += len(word)
                # raise Exception("Invalid token found")
                # cur_pos += 1e4
                # pass
        
            if cur_pos > len(temp):
                break
            word = temp[cur_pos:]
        
    if string_found == True:
        # raise Exception("String not closed")
        string_found = False
        collect_string = ""

# if len(sys.argv) != 2:
#     print(f"Expected 2 argments given {len(sys.argv)} arguments") 
#     sys.exit(1)
# file_name = sys.argv[1]

# tokens = []
# file_path = os.path.join("..", "testcases", f"{file_name}")
# with open(file_path, "r") as code:
#     for line in code:
#         lexer(line, tokens)
# print(tokens)