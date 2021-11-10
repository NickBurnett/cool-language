LINE: int = 0
KEYWORDS = [
  "print",
  "get",
  "if",
  "then",
  "else",
  "end",
  "while",
  "do",
  "and",
  "or",
  "not",
  "shift",
]

class OutputType:
  TOKEN_ID: str = "ID"
  TOKEN_KEYWORD: str = "KEYWORD"
  TOKEN_INT: str = "INT"
  TOKEN_STRING: str = "STRING"
  TOKEN_COMMENT: str = "COMMENT"
  LEXEME: str = "LEXEME"
  ERROR: str = "ERROR"
  NONE: str = "NONE"


class LexOutput:
  output_type: OutputType
  output: str
  rest: str

  def __init__(self, output_type, output, rest):
    self.output_type = output_type
    self.output = output
    self.rest = rest


def lexID(line: str):
  id = ""
  if len(line) <= 0:
    return LexOutput(OutputType.ERROR, "Unexpected end-of-input at line {0} while lexing an ID".format(LINE), line)
  while len(line) > 0 and (line[0].isdigit() or line[0].isalpha() or line[0] == "_"):
    id += line[0]
    line = line[1:]
  if id in KEYWORDS:
    return LexOutput(OutputType.TOKEN_KEYWORD, id, line)
  return LexOutput(OutputType.TOKEN_ID, id, line)


def lexInt(line: str):
  num = ""
  if len(line) <= 0:
    return LexOutput(OutputType.ERROR, "Unexpected end-of-input at line {0} while lexing an INT".format(LINE), line)
  neg = True if line[0] == "-" else False
  if line[0] == "+" or line[0] == "-":
    line = line[1:]
  while len(line) > 0 and line[0].isdigit():
    num += line[0]
    line = line[1:]
  if neg:
    num = "-" + num
  return LexOutput(OutputType.TOKEN_INT, num, line)


def lexString(line: str):
  s = ""
  complete = False
  if len(line) <= 0:
    return LexOutput(OutputType.ERROR, "Unexpected end-of-input at line {0} while lexing a STRING".format(LINE), line)
  while len(line) > 0:
    if line[0] == "\\":
      if len(line[1:]) <= 0:
        break
      line = line[1:]
      if line[0] == "\\":
        s += "\\"
      elif line[0] == "t":
        s += "\t"
      elif line[0] == "n":
        s += "\n"
      elif line[0] == "\"":
        s += "\""
      line = line[1:]
    elif line[0] == "\"":
      complete = True
      line = line[1:]
      break
    else:
      s += line[0]
      line = line[1:]
  if not complete:
    return LexOutput(OutputType.ERROR, "Unexpected end-of-input at line {0} while lexing a STRING (quote)".format(LINE), line)
  return LexOutput(OutputType.TOKEN_STRING, s, line)


def lex(line: str):
  global LINE
  if len(line) <= 0 or line == "\n":
    return LexOutput(OutputType.NONE, "End-of-line", "")
  while len(line) > 0 and (line[0].isspace() or line[0] == '\n'):
    line = line[1:]
  if len(line) <= 0:
    return LexOutput(OutputType.ERROR, "Unexpected end-of-input at line {0}".format(LINE), line)
  if line[0].isdigit():
    return lexInt(line)
  elif line[0] == "+":
    if len(line[1:]) > 0 and line[1:][0].isdigit():
      return lexInt(line)
    elif len(line[1:]) > 0 and line[1:][0] == "+":
      return LexOutput(OutputType.LEXEME, "++", line[2:])
    else:
      return LexOutput(OutputType.LEXEME, "+", line[1:])
  elif line[0] == "-":
    if len(line[1:]) > 0 and line[1:][0].isdigit():
      return lexInt(line)
    elif len(line[1:]) > 0 and line[1:][0] == "-":
      return LexOutput(OutputType.LEXEME, "--", line[2:])
    else:
      return LexOutput(OutputType.LEXEME, "-", line[1:])
  elif line[0] == ";":
    return LexOutput(OutputType.LEXEME, ";", line[1:])
  elif line[0] == ",":
    return LexOutput(OutputType.LEXEME, ",", line[1:])
  elif line[0] == "(":
    return LexOutput(OutputType.LEXEME, "(", line[1:])
  elif line[0] == ")":
    return LexOutput(OutputType.LEXEME, ")", line[1:])
  elif line[0] == "=":
    return LexOutput(OutputType.LEXEME, "=", line[1:])
  elif line[0] == "!":
    if len(line[1:]) > 0 and line[1:][0] == "=":
      return LexOutput(OutputType.LEXEME, "!=", line[2:])
    else:
      return LexOutput(OutputType.ERROR, "Unexpected input at line {0}".format(LINE), line)
  elif line[0] == "/":
    return LexOutput(OutputType.LEXEME, "/", line[1:])
  elif line[0] == "*":
    return LexOutput(OutputType.LEXEME, "*", line[1:])
  elif line[0] == "%":
    return LexOutput(OutputType.LEXEME, "%", line[1:])
  elif line[0] == "=":
    if len(line[1:]) > 0 and line[1:][0] == "=":
      return LexOutput(OutputType.LEXEME, "==", line[2:])
    else:
      return LexOutput(OutputType.LEXEME, "=", line[1:])
  elif line[0] == "<":
    if len(line[1:]) > 0 and line[1:][0] == "=":
      return LexOutput(OutputType.LEXEME, "<=", line[2:])
    elif len(line[1:]) > 1 and line[1:3] == "->":
      return LexOutput(OutputType.LEXEME, "<->", line[3:])
    else:
      return LexOutput(OutputType.LEXEME, "<", line[1:])
  elif line[0] == ">":
    if len(line[1:]) > 0 and line[1:][0] == "=":
      return LexOutput(OutputType.LEXEME, ">=", line[2:])
    else:
      return LexOutput(OutputType.LEXEME, ">", line[1:])
  elif line[0] == "\"":
    return lexString(line[1:])
  elif line[0].isalpha() or line[0] == "_":
    return lexID(line)
  else:
    return LexOutput(OutputType.ERROR, "Unrecognized token at line {0}".format(LINE), line)
  