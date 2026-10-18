import math

priority = {'+': 1, '-': 1, '*': 2, '/': 2, '>>': 0, 'u-': 3}


def tokenize(s):
    s = s.replace(' ', '')
    tokens = []
    i = 0
    while i < len(s):
        ch = s[i]

        if ch.isdigit() or ch == '.':
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            tokens.append(float(s[i:j]))
            i = j
        elif ch == '>':
            tokens.append('>>')
            i += 2
        elif ch == 's':
            tokens.append('sqrt')
            i += 4
        elif ch in '+-()*/':
            tokens.append(ch)
            i += 1
        else:
            raise ValueError()

    result = []
    for ind, token in enumerate(tokens):
        if token == '-':
            if ind == 0 or tokens[ind-1] in ('>>', '+', '-', '*', '/', '(', 'sqrt'):
                result.append('u-')
            else:
                result.append('-')
        else:
            result.append(token)
    return result

def calculate(nums, operator):
    if operator == 'u-':
        a = nums.pop()
        nums.append(-a)
        return

    if operator == 'sqrt':
        a = nums.pop()
        nums.append(math.sqrt(a))
        return

    b = nums.pop()
    a = nums.pop()
    if operator == '+':
        nums.append(a + b)
    elif operator == '-':
        nums.append(a - b)
    elif operator == '*':
        nums.append(a * b)
    elif operator == '/':
        nums.append(a / b)
    elif operator == '>>':
        nums.append(int(a) >> int(b))

def evaluate(tokens):
    values = []
    ops = []

    for token in tokens:
        if isinstance(token, float):
            values.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops[-1] != '(':
                calculate(values, ops.pop())
            ops.pop()
            if len(ops) > 0 and ops[-1] == 'sqrt':
                calculate(values, ops.pop())
        elif token == 'sqrt':
            ops.append(token)
        elif token == 'u-':
            ops.append(token)
        else:
            while len(ops) > 0 and ops[-1] != '(' and priority[ops[-1]] >= priority[token]:
                calculate(values, ops.pop())
            ops.append(token)

    while len(ops) > 0:
        calculate(values, ops.pop())

    return values[0]

try:
    s = input()
    tokens = tokenize(s)
    print("результат: ", evaluate(tokens))
except ZeroDivisionError:
    print("Ошибка: деление на ноль!")
except Exception:
    print("Ошибка: некорректное выражение")