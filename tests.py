import sys
import unittest
from lexer import LINE, LexOutput, OutputType, lex

def run(name: str):
  global LINE
  f = open("programs/{0}".format(name), "r")
  lines = f.readlines()
  f.close()
  error = False
  for line in lines:
    LINE += 1
    while len(line) > 0 and not error:
      output: LexOutput = lex(line)
      line = output.rest
      if output.output_type == OutputType.NONE:
        break
      elif output.output_type == OutputType.ERROR:
        error = True
      else:
        yield output


class Test(unittest.TestCase):
  def test_a(self):
    expected = [
      LexOutput(OutputType.TOKEN_KEYWORD, "print", ""),
      LexOutput(OutputType.TOKEN_STRING, "hello, world!", ""),
      LexOutput(OutputType.TOKEN_ID, "my_var", ""),
      LexOutput(OutputType.LEXEME, "=", ""),
      LexOutput(OutputType.TOKEN_INT, "39", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "print", ""),
      LexOutput(OutputType.TOKEN_ID, "my_var", ""),
    ]
    expected = list(map(lambda out: [out.output_type, out.output], expected))
    output = list(map(lambda out: [out.output_type, out.output], run("a.txt")))
    self.assertListEqual(expected, output)
  def test_b(self):
    expected = [
      LexOutput(OutputType.TOKEN_INT, "985", ""),
      LexOutput(OutputType.TOKEN_INT, "84393", ""),
      LexOutput(OutputType.TOKEN_INT, "-293", ""),
      LexOutput(OutputType.TOKEN_INT, "0", ""),
      LexOutput(OutputType.TOKEN_STRING, "test", ""),
      LexOutput(OutputType.TOKEN_STRING, "another \ttest with \"193784 <- numbers", ""),
      LexOutput(OutputType.TOKEN_ID, "my_var", ""),
      LexOutput(OutputType.TOKEN_INT, "0", ""),
      LexOutput(OutputType.TOKEN_ID, "my_value0298", ""),
      LexOutput(OutputType.TOKEN_ID, "x", ""),
      LexOutput(OutputType.LEXEME, "<->", ""),
      LexOutput(OutputType.TOKEN_ID, "y", ""),
      LexOutput(OutputType.LEXEME, "++", ""),
    ]
    expected = list(map(lambda out: [out.output_type, out.output], expected))
    output = list(map(lambda out: [out.output_type, out.output], run("b.txt")))
    self.assertListEqual(expected, output)
  def test_c(self):
    expected = [
      LexOutput(OutputType.TOKEN_KEYWORD, "print", ""),
      LexOutput(OutputType.TOKEN_STRING, "Hello World!", ""),
      LexOutput(OutputType.LEXEME, ";", ""),
    ]
    expected = list(map(lambda out: [out.output_type, out.output], expected))
    output = list(map(lambda out: [out.output_type, out.output], run("c.txt")))
    self.assertListEqual(expected, output)
  def test_d(self):
    expected = [
      LexOutput(OutputType.TOKEN_KEYWORD, "get", ""),
      LexOutput(OutputType.TOKEN_ID, "x", ""),
      LexOutput(OutputType.LEXEME, ";", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "get", ""),
      LexOutput(OutputType.TOKEN_ID, "y", ""),
      LexOutput(OutputType.LEXEME, ";", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "get", ""),
      LexOutput(OutputType.TOKEN_ID, "z", ""),
      LexOutput(OutputType.LEXEME, ";", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "if", ""),
      LexOutput(OutputType.LEXEME, "(", ""),
      LexOutput(OutputType.TOKEN_ID, "x", ""),
      LexOutput(OutputType.LEXEME, ">", ""),
      LexOutput(OutputType.TOKEN_ID, "y", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "and", ""),
      LexOutput(OutputType.TOKEN_ID, "y", ""),
      LexOutput(OutputType.LEXEME, ")", ""),
      LexOutput(OutputType.LEXEME, "-", ""),
      LexOutput(OutputType.TOKEN_ID, "z", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "then", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "print", ""),
      LexOutput(OutputType.TOKEN_STRING, "\t It is true!\n", ""),
      LexOutput(OutputType.LEXEME, ";", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "else", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "print", ""),
      LexOutput(OutputType.TOKEN_STRING, "\t It is false!!\n", ""),
      LexOutput(OutputType.LEXEME, ";", ""),
      LexOutput(OutputType.TOKEN_KEYWORD, "end", ""),
      LexOutput(OutputType.LEXEME, ";", ""),
    ]
    expected = list(map(lambda out: [out.output_type, out.output], expected))
    output = list(map(lambda out: [out.output_type, out.output], run("d.txt")))
    self.assertListEqual(expected, output)