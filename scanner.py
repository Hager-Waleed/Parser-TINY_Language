import io


class Scanner(object):
    def __init__(self, tiny_code=""):

        self.tiny_code = tiny_code
        self.tokens_list = []
        self.code_list = []
        self.tokens_types = []

    # def setTinyCode(self, tiny_code):
    #     tiny_code.encode(encoding="utf-8")
    #     self.tiny_code = tiny_code

    def scan(self):
        tokens_list = []
        for tiny_in in io.StringIO(self.tiny_code):
            token_str = ""
            special_chars = ['(', ')', '+', '-', '*', '/',
                             '=', ';', '<', '>', '<=', '>=',':=']
            reversed_words = ["if", "then", "else",
                              "end", "repeat", "until", "read", "write"]
            state = "start"
            i = 0
            while i < len(tiny_in):
                if tiny_in[i] in special_chars and state != "inassign" and state != "incomment" and state != "compare" and \
                        tiny_in[i] != '<' and tiny_in[i] != '>':
                    if (token_str != ""):
                        tokens_list.append(token_str)
                        token_str = ""
                    tokens_list.append(tiny_in[i])
                    state = "start"
                elif state == "start":
                    if tiny_in[i] == " ":
                        state = "start"
                    elif tiny_in[i].isalpha():
                        token_str += tiny_in[i]
                        state = "inid"
                    elif tiny_in[i].isdigit():
                        token_str += tiny_in[i]
                        state = "innum"
                    elif tiny_in[i] == ':':
                        token_str += tiny_in[i]
                        state = "inassign"
                    elif tiny_in[i] == '{':
                        token_str += tiny_in[i]
                        state = "incomment"
                    elif (tiny_in[i] == '>') or (tiny_in[i] == '<'):
                        #print("hello")
                        token_str += tiny_in[i]
                        state = "compare"
                    else:
                        state = "done"
                elif state == "inid":
                    if tiny_in[i].isalpha():
                        token_str += tiny_in[i]
                        state = "inid"
                    elif (tiny_in[i] == '>') or (tiny_in[i] == '<'):
                        #print("com")
                        tokens_list.append(token_str)
                        token_str = ""
                        state = "start"
                        i -= 1
                    elif tiny_in[i] == ':':
                        #print("com")
                        tokens_list.append(token_str)
                        token_str = ""
                        state = "start"
                        i -= 1
                    else:
                        state = "done"
                elif state == "compare":
                    if tiny_in[i] == '=':
                        token_str += tiny_in[i]
                        state = "done"
                        #print(tiny_in[i])
                    elif tiny_in[i].isalpha():
                        #print("com")
                        tokens_list.append(token_str)
                        token_str = ""
                        state = "start"
                        i -= 1
                    else:
                        state = "done"
                elif state == "innum":
                    if tiny_in[i].isdigit():
                        token_str += tiny_in[i]
                        state = "innum"
                    else:
                        state = "done"
                elif state == "inassign":
                    if tiny_in[i] == "=":
                        token_str += tiny_in[i]
                        state = "done"
                    else:
                        state = "done"
                elif state == "incomment":
                    if tiny_in[i] == "}":
                        token_str += tiny_in[i]
                        state = "start"
                    else:
                        token_str += tiny_in[i]
                elif state == "done":
                    tokens_list.append(token_str)
                    token_str = ""
                    state = "start"
                    i -= 1

                i += 1
            if (token_str != ""):
                tokens_list.append(token_str)
                token_str = ""
        tokens_list = [x for x in tokens_list if not x.startswith('{')]
        tokens_list = [i for i in tokens_list if i]
        tokens_output = []
        tokens_type = []
        for t in tokens_list:
            if t in reversed_words:
                tokens_output.append(t)
                if t == 'if':
                    tokens_type.append('IF')
                elif t == 'read':
                    tokens_type.append('READ')
                elif t == 'write':
                    tokens_type.append('WRITE')
                elif t == 'repeat':
                    tokens_type.append('REPEAT')
                elif t == 'until':
                    tokens_type.append('UNTIL')
                elif t == 'then':
                    tokens_type.append('THEN')
                elif t == 'end':
                    tokens_type.append('END')
                elif t == 'else':
                    tokens_type.append('ELSE')
            elif t in special_chars:
                tokens_output.append(t)
                if t == '+':
                    tokens_type.append('PLUS')
                elif t == '-':
                    tokens_type.append('MINUS')
                elif t == '*':
                    tokens_type.append('MULT')
                elif t == '/':
                    tokens_type.append('DIV')
                elif t == '+':
                    tokens_type.append('PLUS')
                elif t == '<':
                    tokens_type.append('LESSTHAN')
                elif t == '>':
                    tokens_type.append('GRATERTHAN')
                elif t == '=':
                    tokens_type.append('EQUAL')
                elif t == ';':
                    tokens_type.append('SEMICOLON')
                elif t == ')':
                    tokens_type.append('OPENBRACKET')
                elif t == '(':
                    tokens_type.append('CLOSEDBRACKET')
                elif t == ":=":
                    tokens_type.append('ASSIGN')

                elif t == '<=':
                    tokens_type.append('LESSTHAN|EQUAL')
                elif t == '>=':
                    tokens_type.append('GREATERTHAN|EQUAL')
            elif t.isdigit():
                tokens_output.append("number")
                tokens_type.append('NUMBER')
            elif t.isalpha():
                tokens_output.append("identifier")
                tokens_type.append('IDENTIFIER')
            else:
                pass
                # tokens_output.append("comment")
        self.tokens_types = tokens_type
        self.code_list = tokens_list
        self.tokens_list = tokens_output

    def createOutputFile(self, filename):
        output_code = self.scan()
        with open(filename, 'w+') as out:
            out.write(output_code)
