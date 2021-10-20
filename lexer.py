LINE: int = 0

class OutputType:
  TOKEN_ID: str = "ID"
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

def lexInt(line: str):
  num = ""
  if len(line) <= 0:
    return LexOutput(OutputType.ERROR, "Unexpected end-of-line at line {0} while lexing an INT".format(LINE), line)
  neg = True if line[0] == "-" else False
  if line[0] == "+" or line[0] == "-":
    line = line[1:]
  while len(line) > 0 and line[0].isdigit():
    num += line[0]
    line = line[1:]
  if neg:
    num = "-" + num
  return LexOutput(OutputType.TOKEN_INT, num, line)

def lex(line: str):
  global LINE
  LINE += 1
  if len(line) <= 0 or line == "\n":
    return LexOutput(OutputType.NONE, "End-of-line", "")
  while len(line) > 0 and (line[0].isspace() or line[0] == '\n'):
    line = line[1:]
  if len(line) <= 0:
    return LexOutput(OutputType.ERROR, "Unexpected end-of-line at line {0}".format(LINE), line)
  if line[0].isdigit():
    return lexInt(line)
  elif line[0] == "+":
    if len(line[1:]) > 0 and line[1:][0].isdigit():
      return lexInt(line)
    else:
      return LexOutput(OutputType.LEXEME, "+", line[1:])
  elif line[0] == "-":
    if len(line[1:]) > 0 and line[1:][0].isdigit():
      return lexInt(line)
    else:
      return LexOutput(OutputType.LEXEME, "-", line[1:])
  else:
    return LexOutput(OutputType.ERROR, "Unrecognized token at line {0}".format(LINE), line)
  