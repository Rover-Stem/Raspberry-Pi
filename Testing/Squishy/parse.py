import storage

def checkDel (lexedCode):

	delCounts = {"(" : 0, ")" : 0, "{" : 0, "}" : 0, "[" : 0, "]" : 0, "\"" : 0, "\'" : 0}

	for i in range(len(lexedCode)):

		if (lexedCode[i - 1][0] == "\\"):

			continue

		if (lexedCode[i][0] == "("):

			delCounts["("] += 1

		elif (lexedCode[i][0] == ")"):

			delCounts[")"] += 1

		elif (lexedCode[i][0] == "{"):

			delCounts["{"] += 1

		elif (lexedCode[i][0] == "}"):

			delCounts["}"] += 1

		elif (lexedCode[i][0] == "["):

			delCounts["["] += 1

		elif (lexedCode[i][0] == "]"):

			delCounts["]"] += 1

		elif (lexedCode[i][0] == "\""):

			delCounts["\""] += 1

		elif (lexedCode[i][0] == "\'"):

			delCounts["\'"] += 1

	if ((delCounts["("] == delCounts[")"]) and (delCounts["{"] == delCounts["}"]) and (delCounts["["] == delCounts["]"]) and (delCounts["\""] % 2 == 0) and (delCounts["\'"] % 2 == 0)):

		return True

	return False

#Splits line up
def lexer (line, count, functions):

	#Known functions, key characeters, and key words

	functions = functions
	lexedLine = []

	cont = False
	defs = False
	pointer = -1

	i = 0

	# Iterates through line
	while i < len(line):

		if (len(functions) > 0):

			for j in range(len(functions)):

				try:

					if (line[i:(i + len(functions[j]))] == functions[j]):

						if not(pointer == -1):

							lexedLine.append([line[pointer:i], count])

						lexedLine.append([functions[j], count])
						i += len(functions[j])

						pointer = -1

						cont = True

				except:

					pass

		# Passes after function key is found
		if (cont):

			cont = False
			continue

		# Identifies multi char key
		for j in range(len(storage.multiCharKeys) - 1):

			try:

				if ((line[i:(i + len(storage.multiCharKeys[j]))] == storage.multiCharKeys[j]) and not(defs)):

					if not(pointer == -1):

						lexedLine.append([line[pointer:i], count])

					lexedLine.append([storage.multiCharKeys[j], count])
					i += len(storage.multiCharKeys[j])

					pointer = -1

					cont = True

					if (storage.multiCharKeys[j] == "def"):

						defs = True

			except:

				pass

		# Passes after multichar key is found
		if (cont):

			cont = False
			continue

		# Identifies single char key
		for j in range(len(storage.singleCharKeys) - 1):

			try:

				if (((storage.singleCharKeys[j] == "(") or (storage.singleCharKeys[j] == ")") or (storage.singleCharKeys[j] == "[") or (storage.singleCharKeys[j] == "]")) and ((lexedLine[-1][0] == "\"") or (lexedLine[-1][0] == "\'") or (lexedLine[-1][0] == "\\\'") or (lexedLine[-1][0] == "\\\""))):

					continue

				if (line[i] == storage.singleCharKeys[j]):

					if not(pointer == -1):

						lexedLine.append([line[pointer:i], count])

					if (defs):

						functions.append(line[pointer:i].strip(" "))
						defs = False

					lexedLine.append([storage.singleCharKeys[j], count])
					i += 1

					pointer = -1

					cont = True

			except:

				pass

		# Passes after multi char key is found
		if (cont):

			cont = False
			continue

		# Used to identify variables
		if (pointer == -1):

			pointer = i

		i += 1

	if not(pointer == -1):

		lexedLine.append([line[pointer:], count])

	toBePopped = []

	for i in range(0, len(lexedLine)):

		temp = lexedLine[i][0]
		temp = temp.replace(" ", "")

		if (i == 0):

			lexedLine[i][0] = lexedLine[i][0].replace(" ", "")
			continue

		if (temp == ""):

			toBePopped.append(i)

		elif not(lexedLine[i - 1][0] == "\"" or lexedLine[i - 1][0] == "\'"):

			lexedLine[i][0] = lexedLine[i][0].replace(" ", "")

	for i in range(len(toBePopped) - 1, -1, -1):

		lexedLine.pop(toBePopped[i])

	return lexedLine, functions

# Goes from python-ish language to interpreter instructions
def parser (file):

	#print(f"In:\n{file}\n")
	#print("----------------------\n")

	# Seperate out lines
	code = file.replace(";", "\n").split("\n")

	# Keep Track of what needs to be popped
	toBePopped = []

	#print(f"Filtered:\n{code}\n")
	#print("----------------------\n")
	# Removes blank lines
	for i in range(len(code)):

		#print(f"Processing {i}:\n{code[i]}\n")

		temp = code[i]
		temp = temp.replace(" ", "")

		#print(f"Scrubbed:\n{temp}\n")

		if (temp == ""):

			toBePopped.append(i)

		else:

			counter = code[i].replace("\t", " ")

			count = 0

			for j in counter:

				if (j == " "):

					count += 1

				else:

					break

			counter = counter[count:]

			code[i] = [counter, count]

		#print(f"Updated:\n{code}\n")
		#print(f"To be popped:\n{toBePopped}\n")

		#print("----------------------\n")

	for i in range(len(toBePopped) - 1, -1, -1):

		code.pop(toBePopped[i])

	#print(f"Filtered:\n{code}\n")
	#print("----------------------\n")

	lexed = []
	functions = []

	for i in code:

		lexedLine, functions = lexer(i[0], i[1], functions)

		for j in lexedLine:

			lexed.append(j)

	lexed.append(["EOF"])
	lexed.append(["EOF"])

	#print(f"Lexed:\n{lexed}\n")

	#print("Checking Delimiter Matches:\n")

	delimiterCheck = checkDel(lexed)

	#if (delimiterCheck):

		#print("Passed\n")

	#else:

		#print("Failed\n")

	#print("----------------------\n")
	#print("Passing to Interpreter\n")

	return lexed