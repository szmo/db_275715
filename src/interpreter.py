import sys


INTEGER = 'INTEGER'
PLUS = 'ADD'
MINUS = 'SUB'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LBR'
RPAREN = 'RBR'
EOF = 'END'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value


    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )


    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        self.br_counter = 0
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]
        self.current_token = self.get_next_token()
        #print('at start im' + str(self.current_token) + ' now pos is ' + str(self.pos))


    def error(self, token, pos):
        sys.stderr.write('Unexpected token {0} at {1}'.format(token.type, pos))
        sys.exit(-1)
        #raise Exception('Invalid syntax')


    def pos_helper(self):
        if self.text[self.pos] == '(' or self.text[self.pos] == ')':
            self.br_counter += 1 
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]


    def skip_spaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.pos_helper()


    def form_int(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.pos_helper()
        return int(result)


    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_spaces()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.form_int())

            if self.current_char == '+':
                self.pos_helper()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.pos_helper()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.pos_helper()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.pos_helper()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.pos_helper()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.pos_helper()
                return Token(RPAREN, ')')

            self.error(self.token, self.pos)
            #self.error()

        return Token(EOF, None)


    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
            #print('eating ' + token_type + ' now pos is ' + str(self.pos) )
        else:
            #self.error()
            self.error(self.current_token, (self.pos-1))


    def factor(self):
        token = self.current_token
        #print(token)
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            #print(self.current_token)
            self.eat(RPAREN)
            return result
        if self.current_token.type == EOF:
            self.error(self.current_token, (self.pos-1))
        else:
           self.error(self.current_token, (self.pos-1))



    def term(self):
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                try:
                    result = result / self.factor()
                except ZeroDivisionError:
                    sys.stderr.write('Division by 0.')
                    sys.exit(-1)

        return int(result)


    def expr(self):
        #self.current_token = self.get_next_token()
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()   

        return result


    def helper(self):
        result = self.expr()
        if self.br_counter % 2 == 0:
            return result
        self.error(self.current_token, (self.pos-1))


def main():
    text = next(sys.stdin)
    interpreter = Interpreter(text)
    result = interpreter.helper()
    print(result)


if __name__ == '__main__':
    main()
