import sys
import interpreter.lexer as lexer
import interpreter.parser as parser

f = open("programs/{0}.txt".format(sys.argv[1] if len(sys.argv) > 1 else "a"), "r")
lines = f.readlines()
f.close()

lexed = []

for line in lines:
  lexer.LINE += 1
  while len(line) > 0:
    output: lexer.LexOutput = lexer.lex(line)
    line = output.rest
    if output.output_type == lexer.OutputType.NONE:
      break
    lexed.append(output)
    if output.output_type == lexer.OutputType.ERROR:
      print("[{0}, {1}]".format(output.output_type, output.output))
      sys.exit(1)

if parser.parseProgram(lexed):
  print("Parsing succeeded...")
else:
  print("Parsing failed...")