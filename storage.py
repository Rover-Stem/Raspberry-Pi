import queue
import threading

messagesIn = queue.Queue(maxsize = 50)
messagesOut = queue.Queue(maxsize = 10)

now = ""
status = ""

exiting = False
testing = None

multiChars = ["\\", "\\\""]
multiLogic = ["+=", "-=", "*=", "/=", "--", "++"]
multiSaved = ["continue", "forever", "return", "break", "elif", "else", "def", "rep", "if"]
multiFunctions = ["analyze", "follow", "pr", "input", "send", "wait", "run"]
multiKeyWords = multiSaved + multiFunctions
multiOperators = ["==", ">=", "=>", "=<", "<="]

singles = [":"]
singleLogic = [">", "<"]
singleOperators = ["*", "%", "+", "=", "-", "/", "^"]
singleDelimiters = ["\"", "\'", "(", ")", "{", "}", "[", "]"]

multiCharKeys = multiChars + multiLogic + multiKeyWords + multiOperators
singleCharKeys = singles + singleLogic + singleOperators + singleDelimiters

reserved = multiCharKeys + singleCharKeys