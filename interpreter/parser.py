from interpreter.lexer import OutputType, LexOutput

# UTILITY

tokens = []
debugging: bool = False

def log(t: str, token: LexOutput):
  if not debugging:
    return
  if not token:
    print("{0}".format(t))
    return
  print("{0}: {1} {2}".format(t, token.output_type, token.output))

def next() -> LexOutput:
  global tokens
  if len(tokens) <= 0:
    return LexOutput(OutputType.NONE, "End-of-line", "")
  token = tokens[0]
  tokens = tokens[1:]
  return token

def revert(token):
  tokens.insert(0, token)

# PARSING
def parseValue():
  token = next()
  log("value", token)
  if token.output_type != OutputType.LEXEME and token.output_type != OutputType.TOKEN_KEYWORD and token.output_type != OutputType.TOKEN_ID and token.output_type != OutputType.TOKEN_INT:
    return False
  if token.output_type == OutputType.TOKEN_ID:
    return True
  elif token.output_type == OutputType.TOKEN_INT:
    return True
  elif token.output == "-":
    return parseValue()
  elif token.output == "not":
    return parseValue()
  elif token.output == "(":
    return parseExpr() and next().output == ")"
  else:
    return False

def parseVExpr():
  token = next()
  log("v_expr", token)
  if token.output_type != OutputType.LEXEME:
    revert(token)
    log("revert", None)
    return True
  if token.output == ">":
    return parseValue()
  elif token.output == ">=":
    return parseValue()
  elif token.output == "<":
    return parseValue()
  elif token.output == "<=":
    return parseValue()
  elif token.output == "==":
    return parseValue()
  elif token.output == "!=":
    return parseValue()
  else:
    revert(token)
    log("revert", None)
    return True

def parseFExpr():
  token = next()
  log("f_expr", token)
  if token.output_type != OutputType.LEXEME:
    revert(token)
    log("revert", None)
    return True
  if token.output == "*":
    return parseTerm()
  elif token.output == "/":
    return parseTerm()
  elif token.output == "%":
    return parseTerm()
  else:
    revert(token)
    log("revert", None)
    return True

def parseFactor():
  log("factor", None)
  return parseValue() and parseVExpr()

def parseTExpr():
  token = next()
  log("t_expr", token)
  if token.output_type != OutputType.LEXEME:
    revert(token)
    log("revert", None)
    return True
  if token.output == "+":
    return parseNExpr()
  elif token.output == "-":
    return parseNExpr()
  else:
    revert(token)
    log("revert", None)
    return True

def parseTerm():
  log("term", None)
  return parseFactor() and parseFExpr()

def parseBExpr():
  token = next()
  log("b_expr", token)
  if token.output_type != OutputType.TOKEN_KEYWORD:
    revert(token)
    log("revert", None)
    return True
  if token.output == "and":
    return parseNExpr()
  elif token.output == "or":
    return parseNExpr()
  else:
    revert(token)
    log("revert", None)
    return True

def parseNExpr():
  log("n_expr", None)
  return parseTerm() and parseTExpr()

def parseExpr():
  log("expression", None)
  return parseNExpr() and parseBExpr()

def parseExitArg():
  return parseExpr()

def parseShiftArg():
  token = next()
  if token.output_type != OutputType.TOKEN_ID:
    return False
  return next().output == "," and parseExpr()

def parsePrintArg():
  token = next()
  log("print", token)
  if token.output_type == OutputType.TOKEN_STRING:
    return True
  revert(token)
  return parseExpr()

def parseStmt():
  token = next()
  log("stmt", token)
  if token.output_type != OutputType.TOKEN_KEYWORD and token.output_type != OutputType.TOKEN_ID:
    return False
  if token.output == "else":
    revert(token)
    log("revert", None)
    return True
  elif token.output == "end":
    revert(token)
    log("revert", None)
    return True
  elif token.output == "print":
    return parsePrintArg()
  elif token.output == "shift":
    return parseShiftArg()
  elif token.output == "exit":
    return parseExitArg()
  elif token.output == "get":
    token = next()
    return token.output_type == OutputType.TOKEN_ID
  elif token.output_type == OutputType.TOKEN_ID:
    token = next()
    return token.output == "=" and parseExpr()
  elif token.output == "if":
    return parseExpr() and next().output == "then" and parseStmtList() and next().output == "else" and parseStmtList() and next().output == "end"
  elif token.output == "while":
    return parseExpr() and next().output == "do" and parseStmtList() and next().output == "end"
  else:
    return False

def parseStmtList():
  token = next()
  log("stmt_list", token)
  if token.output_type == OutputType.NONE:
    return True
  revert(token)
  stmt = parseStmt()
  token = next()
  if token.output != ";":
    if token.output == "else" or token.output == "end":
      revert(token)
      log("revert", None)
      return stmt
    else:
      return False
  return stmt and parseStmtList()

def parseProgram(lexed_tokens, debug = False):
  global tokens
  global debugging
  debugging = debug
  if len(lexed_tokens) <= 0:
    return False
  tokens = lexed_tokens
  return parseStmtList()
