from controlLoop import switch

def analyze ():

	print("Analyze")
	pass

def follow (line):

	print("Follow")
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

def wait (time):

	sleep(time)

def run (cmd):

	cmd = cmd.split(",")
	cmd.insert(0, "R")

	switch(cmd)