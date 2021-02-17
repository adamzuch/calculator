def calculate(expression):
    """
    Calculates a value from a literal expression (no 'x' variables).
    """
    tokens = Scanner(expression).scan()
    return Parser(tokens).parse()


def substitute(expression, value):
    """
    Substitutes a value for 'x' in the expression and calculates it.
    """
    tokens = Scanner(expression).scan()
    for i, token in enumerate(tokens):
        if token.type == "x":
            if isinstance(value, float):
                tokens[i] = Token("float", value)
            elif isinstance(value, int):
                tokens[i] = Token("int", value)
            else:
                raise ParserError
    return Parser(tokens).parse()


class Token:
    """
    Data class for storing an individual token. Token types are the following:
    { "(", ")", "+", "-", "*", "/", "int", "float", "x"}. Token types "int"
    and "float" also contain the literal value of the token. "x" token
    represents an unknown variable which can be substituted for a value.
    """
    def __init__(self, type, value=None):
        self.type = type
        self.value = value


class Scanner:
    """
    Tokenizes the expression string. Strips all whitespace before processing.
    """
    def __init__(self, text):
        self.text = "".join(text.split())
        self.start = 0
        self.current = 0
        self.tokens = []

    def scan(self):
        while not self.is_finished():
            self.start = self.current
            try:
                self.scan_token()
            except ScanError:
                return []
        self.tokens.append(Token(""))
        return self.tokens

    def scan_token(self):
        c = self.advance()  # next character

        # need to do additional scanning when encountering a digit.
        # e.g. Number could be a float or an int.
        if c.isdigit():
            self.number()

        elif c == "x":
            if self.peek() in ")/*+-":
                self.tokens.append(Token(c))
            else:
                raise ScanError

        elif c in "()/*+-":  # just add the token if encountered.
            self.tokens.append(Token(c))
        else:
            raise ScanError  # any other character is invalid.

    def number(self):
        """
        Handles case where the scanner encounters a digit.
        """
        while self.peek().isdigit():
            self.advance()

        # check that a period is followed by another digit and continue
        # scanning.
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

            self.tokens.append(Token("float", float(self.text[self.start:self.current])))
        else:
            self.tokens.append(Token("int", int(self.text[self.start:self.current])))

    def advance(self):
        """
        Return character at current index and increment.
        """
        self.current += 1
        return self.text[self.current - 1]

    def peek(self):
        """
        Return character at current index without incrementing.
        """
        if self.is_finished():
            return ""  # empty string represents end of line.
        return self.text[self.current]

    def peek_next(self):
        """
        Similar to peek() but checks one step ahead of current.
        """
        if self.current + 1 < len(self.text):
            return self.text[self.current + 1]
        return ""

    def is_finished(self):
        return self.current >= len(self.text)


class Parser:
    """
    Parses and evaluates list of tokens from scanner. Uses recursive descent
    parsing. Parser grammar is shown below.

    expression  <-  term (("+" | "-") term)*
    term        <-  negation (("/" | "*") negation)*
    negation    <-  ("-" negation) | literal
    literal     <-  INT | FLOAT | "(" expression ")"
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            if len(self.tokens) == 0:
                return None
            return self.expression()
        except ParserError:
            return None

    def expression(self):
        expr = self.term()

        while self.match(["+", "-"]):
            operator = self.previous().type
            right = self.term()
            expr = binary_operation(expr, operator, right)
        return expr

    def term(self):
        expr = self.negation()

        while self.match(["/", "*"]):
            operator = self.previous().type
            right = self.negation()
            expr = binary_operation(expr, operator, right)
        return expr

    def negation(self):
        if self.match(["-"]):
            operator = self.previous().type
            right = self.negation()
            return unary_operation(operator, right)
        return self.literal()

    def literal(self):
        if self.match(["int", "float"]):
            return self.previous().value
        if self.match(["("]):
            expr = self.expression()
            # need to check for closing bracket or syntax is invalid.
            if self.peek().type == ")":
                self.advance()
            else:
                raise ParserError
            return expr
        raise ParserError

    def match(self, tokens):
        """
        Checks that current token type matches one of those in the input token
        list. Returns True and increments the current index if there is a
        match. Returns False otherwise.
        """
        for t in tokens:
            if t == self.peek().type:
                self.advance()
                return True
        return False

    def previous(self):
        """
        Returns the token before the token at the current index. Used to
        retrieve token after matching one.
        """
        return self.tokens[self.current - 1]

    def advance(self):
        """
        Same as Scanner.advance() but returns token instead of single character.
        """
        self.current += 1
        return self.tokens[self.current - 1]

    def peek(self):
        """
        Same as Scanner.peek() but returns token instead of single character.
        """
        if not self.is_finished():
            return self.tokens[self.current]

    def is_finished(self):
        return self.current >= len(self.tokens)


def binary_operation(left, operator, right):
    if operator == "/":
        return left / right
    if operator == "*":
        return left * right
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right


def unary_operation(operator, right):
    if operator == "-":
        return -right


class ParserError(Exception):
    pass


class ScanError(Exception):
    pass

