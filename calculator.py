from collections import deque


def calculate(inp):
    try:
        eval_statement(deque(normalize_input(inp).split()))
    except KeyError:
        print("Unknown variable")
    except NameError:
        print("Invalid identifier")
    except (AssertionError, IndexError, TypeError):
        print("Invalid assignment")


def eval_statement(inp):
    if len(inp) >= 2 and inp[1] == '=':
        eval_assignment(inp)
    else:
        print(eval_expression(inp))


def eval_assignment(inp):
    name = inp.popleft()
    if not name.isalpha():
        raise NameError

    inp.popleft()
    storage[name] = eval_expression(inp)


def eval_expression(inp):
    postfix = convert_to_postfix(inp)
    stack = deque()

    while postfix:
        token = postfix.popleft()
        if not isinstance(token, str):
            stack.append(token)
            continue

        a = stack.pop()
        b = stack.pop() if len(stack) else None

        if token == "^":
            stack.append(b ** a)
        elif token == "*":
            stack.append(b * a)
        elif token == "/":
            stack.append(b // a)
        elif token == "+":
            stack.append((0 if b is None else b) + a)
        elif token == "-":
            stack.append((0 if b is None else b) - a)

    return stack.pop()


def convert_to_postfix(inp):
    stack = deque()
    postfix = deque()

    while inp:
        token = inp.popleft()
        if token in "+-*/^":
            move_operators(stack, postfix, token)
            stack.append(token)
        elif token == "(":
            postfix.extend(convert_to_postfix(inner_parentheses(inp)))
        else:
            postfix.append(eval_var(token))

    postfix.extend(stack)

    return postfix


def inner_parentheses(inp):
    level = 0
    sequence = deque()

    while True:
        token = inp.popleft()
        if token == "(":
            level += 1
        elif token == ")":
            level -= 1

        if level < 0:
            break
        else:
            sequence.append(token)

    return sequence


def move_operators(stack, postfix, token):
    if len(stack) == 0 or is_lower_precedence(stack[-1], token):
        return

    while stack and not is_lower_precedence(stack[-1], token):
        postfix.append(stack.pop())


def is_lower_precedence(op1, op2):
    if op1 == "^":
        return False
    elif op1 in "*/":
        return op2 == "^"
    elif op1 in "+-":
        return op2 in "*/^"
    else:
        raise AssertionError


def eval_var(inp):
    if inp.isalpha():
        return storage[inp]
    elif inp.isnumeric():
        return int(inp)
    else:
        raise AssertionError


def normalize_input(inp):
    inp = inp \
        .replace(" ", "") \
        .replace("+", " + ") \
        .replace("-", " - ") \
        .replace("=", " = ") \
        .replace("(", " ( ") \
        .replace(")", " ) ") \
        .replace("*", " * ") \
        .replace("/", " / ")

    while True:
        length = len(inp)
        inp = inp \
            .replace("  ", " ") \
            .replace(" - - ", " + ") \
            .replace(" + + ", " + ") \
            .replace(" - + ", " - ") \
            .replace(" + - ", " - ")

        if inp[:2] == " +":
            inp = inp[2:]
        elif len(inp) == length:
            break

    return inp.strip()


if __name__ == "__main__":
    storage = {}

    while True:
        command = input()
        if command == "/exit":
            print("Bye!")
            break
        elif command == "/help":
            print("The program calculates the sum of numbers")
        elif command[:1] == "/":
            print("Unknown command")
        elif command != "":
            calculate(command)
