from parse import lexer

line = ['var="Hello"', "forever", "print(var)", "if(var==\"Hello\")", "break"]

for i in range(len(line)):

	line[i] = lexer(line[i])

print(line)