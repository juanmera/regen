import enum


class State(enum.Enum):
    Initial = 0
    Literal = 1
    DotAll = 2
    StartList = 3
    EndList = 4


class Parser:
    def __init__(self, str):
        self.str = str
        self.state = State.Initial
        self.index = 0
        self.value = ''

    def _len(self):
        return len(self.str)

    def _char(self):
        return self.str[self.index]

    def _next_char(self):
        self.index += 1
        return self._char()

    def _not_last_index(self):
        return self.index+1 < self._len()

    def _consume_count(self):
        count_str = ''
        j = self.index+1
        c = self.str[j]
        while c in '0123456789':
            count_str += c
            j += 1
            c = self.str[j]
        if len(count_str) > 0 and c == '}':
            self.index = j
            return int(count_str, 10)
        return 0

    def _range(self, start, end):
        result = ''
        for i in range(ord(start), ord(end)+1):
            result += chr(i)
        return result

    def iter(self):
        self.state = State.Initial
        self.index = 0
        self.value = ''
        while self.index < self._len():
            c = self._char()
            if self.state == State.Initial:
                if c == '[':
                    self.state = State.StartList
                else:
                    self.state = State.Literal
                    if c == '\\' and self._not_last_index():
                        self.value = self._next_char()
                    elif c == '.':
                        self.value = self._range('\x00', '\xff')
                    else:
                        self.value = c
            elif self.state == State.StartList:
                if c == ']':
                    self.state = State.Literal
                elif c == '\\' and self._not_last_index():
                    self.value += self._next_char()
                elif c == '-' and len(self.value) > 0 and self._not_last_index() and self.str[self.index+1] != ']':
                    last_c = self.value[-1]
                    self.value = self.value[:-1] + self._range(last_c, self._next_char())
                else:
                    self.value += c
            elif self.state == State.Literal:
                count = 0
                if c == '{':
                    count = self._consume_count()
                if count == 0:
                    count = 1
                    self.index -= 1
                for _ in range(count):
                    yield self.value
                self.value = ''
                self.state = State.Initial
            self.index += 1
        if self.state == State.Literal:
            yield self.value


#if __name__ == '__main__':
#    p = Parser(r'\{"a":.[b-f-]{3}c\}')
#    print(list(p.iter()))
