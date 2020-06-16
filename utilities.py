import os

def create_file_with_contents(filepath, content):
	with open(filepath, 'w') as ffile:
		ffile.write(content)

def read_file_contents(filepath):
	if not os.path.exists(filepath):
		return None

	contents = ''
	with open(filepath) as ffile:
		contents = ffile.read()

	return contents

def is_pid_running(pid):
	if not pid:
		return False

	pid = int(pid)
	try:
	    os.kill(pid, 0)
	except OSError:
		return False
	else:
	    return True