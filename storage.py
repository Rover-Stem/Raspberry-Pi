import queue
import threading

messagesIn = queue.Queue(maxsize = 50)
messagesOut = queue.Queue(maxsize = 10)

now = ""
status = ""

exiting = False
testing = None