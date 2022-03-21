import squish
import storage

from parse import parser

def functAnalysis (vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer, parsedCmds, lastIf, pointerSaves, varKeys, logicKeys, repeatsKeys, loopPointersKeys, logicPointersKeys, functionPointersKeys, delimiterPointersKeys):

	if (functionPointers[parsedCmds[pointer][0]] == "squish"):

		execClause = ""

		for i in range((pointer + 1), len(parsedCmds)):

			if ((parsedCmds[i][0] in (storage.multiKeyWords + list(functionPointersKeys))) or (parsedCmds[i][0] == "EOF")):

				break

			elif (parsedCmds[i][0] == "="):

				execClause = execClause[:(-1 * (len(parsedCmds[i - 1][0]) - 1))]

				break

			elif (any(parsedCmds[i][0] in x for x in varKeys)):

				loc = findFunct(parsedCmds, i)

				if (loc == "main"):

					try:

						vars[parsedCmds[i][0]][1]

					except:

						continue

					execClause += f"\"{vars[parsedCmds[i][0]][1]}\""

				else:

					location = parsedCmds[i][0] + f":{loc}"

					try:

						vars[location][1]

					except:

						break

					execClause += f"\"{vars[location][1]}\""

				continue

			execClause += parsedCmds[i][0]

		if ((execClause[0] == "(") and (execClause[-1] == ")")):

			execClause = execClause[1:-1]

		# Hope this doesn't break something

		return f'eval(f\'squish.{parsedCmds[pointer][0]}({execClause})\')', vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer, parsedCmds, lastIf, pointerSaves

	else:

		arguments = functionPointers[parsedCmds[pointer][0]][2].split(",")
		argumentsStripped = functionPointers[parsedCmds[pointer][0]][2].replace("*", "").split(",")

		execClause = ""

		for i in range((pointer + 1), len(parsedCmds)):

			if ((parsedCmds[i][0] in (storage.multiKeyWords + list(functionPointersKeys))) or (parsedCmds[i][0] == "EOF") or ((execClause.count("(") == execClause.count(")")) and (execClause.count("(") > 0))):

				break

			elif ((parsedCmds[i][0] == "=") and not(any(x in parsedCmds[i - 1][0].split(",") for x in argumentsStripped))):

				execClause = execClause[:(-1 * (len(parsedCmds[i - 1][0]) + 1))]

				break

			elif (parsedCmds[i][0] in varKeys):

				execClause += vars[parsedCmds[i][0]][1]

				continue

			execClause += parsedCmds[i][0]

		if ((execClause[0] == "(") and (execClause[-1] == ")")):

			execClause = execClause[1:-1]

		execClause = execClause.replace(",", "=").split("=")

		formula = [""]

		for i in execClause:

			if not(i in argumentsStripped):

				if (formula[-1] != ""):

					formula[-1] += ","

				formula[-1] += i

				if ((formula[-1].count("(") == formula[-1].count(")")) and (formula[-1].count("[") == formula[-1].count("]"))):

					formula.append("")

		formula.pop(-1)

		keys = list(varKeys)
		keys.sort(key = len)
		keys.reverse()

		for i in range(len(formula)):

			if ("," in formula[i]):

				temp = ""

				j = 0

				while True:

					if (j >= (len(formula[i]) - 1)):

						break

					for l in range(len(keys)):

						if (formula[i][j:(j + len(keys[l]))] == keys[l]):

							temp += f"\"{vars[formula[i][j:(j + len(keys[l]))]][1]}\""
							j += len(keys[l])

							continue

					temp += formula[i][j]

					j += 1

				formula[i] = temp

			else:

				if (formula[i] in keys):

					formula[i] = f"\"{vars[formula[i]][1]}\""

				else:

					formula[i] = f"\"{formula[i]}\""

			formula[i] = formula[i]

		for i in argumentsStripped:

			vars[(f"{i}:{parsedCmds[pointer][0]}")] = None

		formatList = []

		for i in execClause:

			if (i in argumentsStripped):

				formatList.append(i)

		for i in range((len(formula) - 1), -1, -1):

			if (len(formatList) > 0):

				popped = formula.pop(-1)

				vars[f"{formatList.pop(-1)}:{parsedCmds[pointer][0]}"] = [popped, eval(popped)]

		for i in range(len(formula)):

			vars[f"{argumentsStripped[i]}:{parsedCmds[pointer][0]}"] = [formula[i], eval(formula[i])]

		for i in range(pointer, len(parsedCmds)):

			if ((parsedCmds[i][0] in (storage.multiKeyWords + list(functionPointersKeys))) or (parsedCmds[i][0] == "EOF")):

				pointerSaves.append(i)
				break

			elif ((parsedCmds[i][0] == "=") and not(any(x in parsedCmds[i - 1][0].split(",") for x in argumentsStripped))):

				pointerSaves.append(i - 1)
				break

		pointer = functionPointers[parsedCmds[pointer][0]][0]

		return runProgram(vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer, parsedCmds, lastIf, pointerSaves)

def findFunct (parsedCmds, currentPos):

	for i in range((currentPos - 1), -1, -1):

		if (parsedCmds[i][1] == 0):

			for j in range(i, -1, -1):

				if ((j == 0) or (parsedCmds[j - 1][1] > 0)):

					if (parsedCmds[j][0] == "def"):

						return parsedCmds[j + 1][0]

					return "main"

def evalFormula (lookingAt, function, functionPointersKeys, pointer):

	formula = lookingAt
	parsedFormula = ""

	functions = False
	funtionClause = ""

	for i in range(0, len(formula)):

		if (functions):

			funtionClause += formula[i]

			if ((funtionClause.count("(") == funtionClause.count(")")) and (funtionClause.count("(") > 0)):

				functions = False

		else:

			if ((type(formula[i]) is str) and not((formula[i] in storage.reserved ) or (formula[i] in functionPointersKeys)) and not(formula[i - 1] == "\"") and not(formula[i] == "None")):

				if (function == "main"):

					parsedFormula += f"vars[\"{formula[i]}\"][1]"

				else:

					parsedFormula += f"vars[\"{formula[i]}:{function}\"][1]"

				continue

			elif (formula[i] in functionPointersKeys):

				parsedFormula += f"functAnalysis(vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, ({pointer} + 1), parsedCmds, lastIf, pointerSaves, varKeys, logicKeys, repeatsKeys, loopPointersKeys, logicPointersKeys, functionPointersKeys, delimiterPointersKeys)"

				functions = True
				funtionClause += formula[i]

				continue

			parsedFormula += str(formula[i])

	return parsedFormula

def decodeTypes (parsedCmds):

	for i in range(1, len(parsedCmds)):

		if not(parsedCmds[i - 1][0] == "\""):

			if (all(any(x in ch for x in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]) for ch in parsedCmds[i][0])):

				if ("." in parsedCmds[i][0]):

					parsedCmds[i] = [float(parsedCmds[i][0]), parsedCmds[i][1]]

				else:

					parsedCmds[i] = [int(parsedCmds[i][0]), parsedCmds[i][1]]

			elif ((parsedCmds[i][0].lower() == "true") or (parsedCmds[i][0].lower() == "false")):

				parsedCmds[i] = [bool(parsedCmds[i][0].lower().capitalize()), parsedCmds[i][1]]

	return parsedCmds

def createPointers (parsedCmds):

	vars = {}
	logic = {}
	repeats = {}
	loopPointers = {}
	logicPointers = {}
	functionPointers = {}
	delimiterPointers = {}

	for i in storage.multiFunctions:

		functionPointers[i] = "squish"

	for i in range(len(parsedCmds)):

		functionPointersKeys = functionPointers.keys()

		if (parsedCmds[i][0] == "("):

			delimiterPointers[i] = ["(", -1]

		elif (parsedCmds[i][0] == ")"):

			for j in reversed(list(delimiterPointers.items())):

				if ((j[1][0] == "(") and (j[1][1] == -1)):

					delimiterPointers[j[0]] = ["(", i]

		elif (parsedCmds[i][0] == "{"):

			delimiterPointers[i] = ["{", -1]

		elif (parsedCmds[i][0] == "}"):

			for j in reversed(list(delimiterPointers.items())):

				if ((j[1][0] == "{") and (j[1][1] == -1)):

					delimiterPointers[j[0]] = ["{", i]

		elif (parsedCmds[i][0] == "["):

			delimiterPointers[i] = ["[", -1]

		elif (parsedCmds[i][0] == "]"):

			for j in reversed(list(delimiterPointers.items())):

				if ((j[1][0] == "[") and (j[1][1] == -1)):

					delimiterPointers[j[0]] = ["[", i]

		elif (parsedCmds[i][0] == "\""):

			for j in reversed(list(delimiterPointers.items())):

				if (j[1][0] == "\""):

					if (j[1][1] == -1):

						delimiterPointers[j[0]] = i

					else:

						delimiterPointers[i] = ["\"", -1]

					break

		elif (parsedCmds[i][0] == "\'"):

			for j in reversed(list(delimiterPointers.items())):

				if (j[1][0] == "\'"):

					if (j[1][1] == -1):

						delimiterPointers[j[0]] = i

					else:

						delimiterPointers[i] = ["\'", -1]

					break

		elif (parsedCmds[i][0] == "forever"):

			for j in range((i + 1), len(parsedCmds)):

				if (((parsedCmds[j][0] == "EOF") or (parsedCmds[j][1] <= parsedCmds[i][1])) and not(parsedCmds[j][0] == ":")):

					loopPointers[(j - 1)] = i

		elif (parsedCmds[i][0] == "rep"):

			repeatsClause = []
			repeats[i] = [None, None, None]

			for j in range((i + 1), len(parsedCmds)):

				if (parsedCmds[j][0] == ":"):

					for l in range((j + 1), len(parsedCmds)):

						if ((parsedCmds[l][1] <= parsedCmds[i][1]) or (parsedCmds[j][0] == "EOF")):

							loopPointers[(l - 1)] = i
							repeats[i] = [(l - 1), j, evalFormula(repeatsClause, findFunct(parsedCmds, i), functionPointersKeys, i)]

							break

					break

				repeatsClause.append(parsedCmds[j][0])

		elif ((parsedCmds[i][0] == "if") or (parsedCmds[i][0] == "elif") or (parsedCmds[i][0] == "else")):

			logicClause = []
			logic[i] = [None, None, None]

			for j in range((i + 1), len(parsedCmds)):

				if (parsedCmds[j][0] == ":"):

					for l in range((j + 1), len(parsedCmds)):

						if ((parsedCmds[l][0] == "EOF") or (parsedCmds[l][1] <= parsedCmds[i][1])):

							logicPointers[(l - 1)] = i
							logic[i] = [(l - 1), j, evalFormula(logicClause, findFunct(parsedCmds, i), functionPointersKeys, i)]

							break

					break

				logicClause.append(parsedCmds[j][0])

		elif (parsedCmds[i][0] == "="):

			if (not(parsedCmds[i - 1][0] in vars.keys()) and not((parsedCmds[i - 2][0] == "(") or ("," in parsedCmds[i - 1][0]))):

				vars[parsedCmds[i - 1][0]] = None
				varClause = []
				function = False

				for j in range((i + 1), len(parsedCmds)):

					if (parsedCmds[j][0] in storage.multiKeyWords):

						break

					elif (parsedCmds[j][0] in functionPointersKeys):

						function = True

					elif (function):

						if not(((varClause.count("(") == varClause.count(")")) and (varClause.count("(") > 0))):

							varClause.append(parsedCmds[j][0])
							continue

						else:

							function = False

					elif (parsedCmds[j][0] == "="):

						varClause.pop(-1)

						break

					elif (parsedCmds[j][0] == "EOF"):

						break

					varClause.append(parsedCmds[j][0])

				formula = evalFormula(varClause, findFunct(parsedCmds, i), functionPointersKeys, i)

				vars[parsedCmds[i - 1][0]] = [formula, eval(formula)]

		elif (parsedCmds[i][0] == "def"):

			functionClause = ""

			for j in range((i + 2), len(parsedCmds)):

				if (parsedCmds[j][0] == ":"):

					for l in range((j + 1), len(parsedCmds)):

						if ((parsedCmds[l][1] <= parsedCmds[i][1]) or (parsedCmds[l][0] == "EOF")):

							functionPointers[parsedCmds[i + 1][0]] = [j, (l - 1), functionClause]

							break

					break

				if not(parsedCmds[j][0] in storage.singleCharKeys):

					if (parsedCmds[j - 1][0] == "*"):

						functionClause += "*" + parsedCmds[j][0]

					else:

						functionClause += parsedCmds[j][0]

	if (parsedCmds[0][0] == "def"):

		for i in range(1, len(parsedCmds)):

			if ((parsedCmds[i][1] == 0) and not(parsedCmds[i][0] == "def") and (parsedCmds[i - 1][1] > 0)):

				pointerStart = i
				break

	else:

		pointerStart = 0

	return vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointerStart

def runProgram (vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer, parsedCmds, lastIf, pointerSaves):

	varKeys = vars.keys()
	logicKeys = logic.keys()
	repeatsKeys = repeats.keys()
	loopPointersKeys = loopPointers.keys()
	logicPointersKeys = logicPointers.keys()
	functionPointersKeys = functionPointers.keys()
	delimiterPointersKeys = delimiterPointers.keys()

	#try:

	#print(f"Vars:\n{vars.items()}\n")
	#print(f"Logic:\n{logic.items()}\n")
	#print(f"Reps:\n{repeats.items()}\n")
	#print(f"Loop Points:\n{loopPointers.items()}\n")
	#print(f"Logic Points:\n{logicPointers.items()}\n")
	#print(f"Function Points:\n{functionPointers.items()}\n")

	while True:

		#try:

		#	print(f"Running with pointer at {pointer} which is {parsedCmds[pointer][0]}")

		#except:

		#	print(f"Running with pointer at {pointer} with a length of {len(parsedCmds)}")

		if (pointer == len(parsedCmds)):

			#print("We all done yo")

			break

		if (pointer in logicKeys):

			if (parsedCmds[pointer][0] == "if"):

				val = eval(logic[pointer][2])
				lastIf = False

				if not(val):

					pointer = logic[pointer][0]

				else:

					pointer = logic[pointer][1]
					lastIf = True

			elif ((parsedCmds[pointer][0] == "elif")):

				val = eval(logic[pointer][2])

				if (not(val) or lastIf):

					pointer = logic[pointer][0]

				else:

					pointer = logic[pointer][1]
					lastIf = True

			elif (parsedCmds[pointer][0] == "else"):

				if (lastIf):

					pointer = logic[pointer][0]

				else:

					pointer += 1

				lastIf = False

			continue

		elif (pointer in repeatsKeys):

			repsVal = eval(repeats[pointer][2])

			if (type(repsVal) == type(0)):

				if (repsVal == 0):

					pointer = (repeats[pointer][0] + 1)

				else:

					temp = repeats[pointer]
					temp[2] = temp[2] + " - 1"
					repeats[pointer] = temp
					pointer = repeats[pointer][1]

			else:

				if not(repsVal):

					pointer = (repeats[pointer][0] + 1)

				else:

					pointer = repeats[pointer][1]

			continue

		elif (pointer in loopPointersKeys):

			pointer = loopPointers[pointer]

			continue

		elif ((pointer + 1) in [functionPointers[x][1] for x in functionPointersKeys if functionPointers[x][1] != "q"] or (parsedCmds[pointer][0] == "return")):

			out = None

			if (parsedCmds[pointer][0] == "return"):

				returnClause = ""

				for i in range((pointer + 1), len(parsedCmds)):

					if (parsedCmds[i][1] < parsedCmds[pointer][1]):

						break

					elif ((parsedCmds[i][0] + f":{findFunct(parsedCmds, i)}") in varKeys):

						location = parsedCmds[i][0] + f':{findFunct(parsedCmds, i)}'
						returnClause += f"\"{vars[location][1]}\""
						continue

					returnClause += parsedCmds[i][0]

				pointer = pointerSaves.pop(-1)

				return (f'\'{returnClause}\''), vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer, parsedCmds, lastIf, pointerSaves

			pointer = pointerSaves.pop(-1)

		elif ((parsedCmds[pointer][0] == "=") and not((parsedCmds[pointer - 2][0] == "(") or ("," in parsedCmds[pointer - 1][0]))):

			varClause = []
			function = False

			for j in range((pointer + 1), len(parsedCmds)):

				if (parsedCmds[j][0] in storage.multiKeyWords):

					break

				elif (parsedCmds[j][0] in functionPointersKeys):

					function = True

				elif (function):

					if not(((varClause.count("(") == varClause.count(")")) and (varClause.count("(") > 0))):

						varClause.append(parsedCmds[j][0])
						continue

					else:

						function = False

				elif (parsedCmds[j][0] == "="):

					varClause.pop(-1)

					break

				elif (parsedCmds[j][0] == "EOF"):

					break

				varClause.append(parsedCmds[j][0])

			finishedFormula = evalFormula(varClause, findFunct(parsedCmds, pointer), functionPointersKeys, pointer)

			if ("functAnalysis" in finishedFormula):

				out, vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer, parsedCmds, lastIf, pointerSaves = eval(finishedFormula)

				vars[parsedCmds[pointer - 2][0]] = [finishedFormula, out]

			else:

				vars[parsedCmds[pointer - 1][0]] = [finishedFormula, eval(finishedFormula)]

		elif (parsedCmds[pointer][0] == "break"):

			keys = list(loopPointers.keys())
			vals = list(loopPointers.values())

			for i in range(len(vals) - 1, -1, -1):

				if (vals[i] < pointer):

					pointer = (keys[i] + 1)

					break

		elif (parsedCmds[pointer][0] == "continue"):

			vals = list(loopPointers.values())

			for i in range(len(vals) - 1, -1, -1):

				if (vals[i] < pointer):

					pointer = vals[i]

					break

		elif (parsedCmds[pointer][0] in functionPointersKeys):

			out, vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer, parsedCmds, lastIf, pointerSaves = functAnalysis (vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer, parsedCmds, lastIf, pointerSaves, varKeys, logicKeys, repeatsKeys, loopPointersKeys, logicPointersKeys, functionPointersKeys, delimiterPointersKeys)

			eval(out)

		elif (parsedCmds[pointer][0] == "def"):

			pointer = functionPointers[parsedCmds[pointer + 1][0]][1]

		pointer += 1

# Gets remote file sent and then runs it
def runCmdSetStaged (rover):

	file = ""

	while True:

		if not(storage.messagesIn.empty()):

			msg = storage.messagesIn.get()

			if (msg == "fin"):

				break

			file += msg

	interpret(parser(file), rover)

# Runs local file
def runFile (filePath, rover):

	file = []

	try:

		with open(filePath, 'r') as f:

			file = f.read()

	except:

		storage.messagesOut.put("E,File Path Non-Existent")
		storage.messagesOut.put("F")

	interpret(parser(file), rover)

# Capture start of the file by finding the first thing with indent 0 and does not include def

def interpret (parsedCmds, rover):

	cmds = parsedCmds

	vars = {}
	logic = {}
	repeats = {}
	loopPointers = {}
	logicPointers = {}
	functionPointers = {}
	delimiterPointers = {}

	pointer = 0
	lastIf = False

	pointerSaves = []

	# Sets Data Types
	cmds = decodeTypes(parsedCmds)

	# Sets up pointers
	vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer = createPointers(cmds)

	runProgram(vars, logic, repeats, loopPointers, logicPointers, functionPointers, delimiterPointers, pointer, parsedCmds, lastIf, pointerSaves)

	#print(f"Vars:\n{vars.items()}\n")
	#print(f"Logic:\n{logic.items()}\n")
	#print(f"Reps:\n{repeats.items()}\n")
	#print(f"Loop Points:\n{loopPointers.items()}\n")
	#print(f"Logic Points:\n{logicPointers.items()}\n")

	#except Exception as e:

	#	print(f"Something went wrong: {e}")
	#	storage.messagesOut.put("E,Something went wrong (More descriptive errors to come in the future)")
	#	storage.messagesOut.put("F")