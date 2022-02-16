#from controlLoop import switch

def analyze ():

	pass

def follow (line):

	pass

def pr (msg):

	print(msg)

def input ():

	msg = None

	storage.messagesOut.put("I")

	while True:

		if not(storage.messagesIn.empty()):

			msg = storage.messagesIn.get()

			break

	return msg

def send (msg):

	storage.messagesOut.put(msg)

def run (cmd):

	switch(cmd)