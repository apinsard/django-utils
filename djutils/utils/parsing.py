# -*- coding: utf-8 -*-
from itertools import product


class ExpandCurlyBraces:

    def __init__(self, expr):
        self.expr = expr
        self.cursor = 0

    @property
    def char(self):
        return self.expr[self.cursor]

    @property
    def next_char(self):
        return self.expr[self.cursor + 1]

    def __call__(self):
        sub_results = []
        current = ''
        while self.cursor < len(self.expr):
            if self.char == '{':
                sub_results.append(self.expand())
                current += '{}'
            elif self.char == '}':
                raise ValueError((
                    "Found unmatched closing curly brace "
                    "at position {} in the expression: \"{}\""
                ).format(self.cursor, self.expr))
            elif self.char == '\\' and self.next_char in '{}\\':
                if self.next_char in '{}':
                    current += self.next_char
                current += self.next_char
                self.forward()
            else:
                current += self.char
            self.forward()
        return self.merge(current, sub_results)

    def expand(self):
        result = []
        sub_results = []
        current = ''
        self.forward()
        while not self.reached_end():
            if self.char == '{':
                sub_results.append(self.expand())
                current += '{}'
            elif self.char == ',':
                result.extend(self.merge(current, sub_results))
                current, sub_results = '', []
            elif self.char == '}':
                result.extend(self.merge(current, sub_results))
                return result
            elif self.char == '\\' and self.next_char in '{,}\\':
                if self.next_char in '{}':
                    current += self.next_char
                current += self.next_char
                self.forward()
            else:
                current += self.char
            self.forward()
        raise ValueError((
            "Found unmatched opening curly brace "
            "at position {} in the expression: \"{}\""
        ).format(self.cursor, self.expr))

    def merge(self, pattern, parts):
        return (pattern.format(*p) for p in product(*parts))

    def forward(self):
        self.cursor += 1

    def reached_end(self):
        return self.cursor >= len(self.expr)


def expand_curly_braces(expr):

    return ExpandCurlyBraces(expr)()
