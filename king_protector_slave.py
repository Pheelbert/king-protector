import os
import signal
import subprocess
import time
import utilities
from king_protector_master import kill_switch_secret

current_pid = str(os.getpid())

def main():
	signal.signal(signal.SIGABRT, handler)
	signal.signal(signal.SIGTERM, handler)
	signal.signal(signal.SIGINT, handler)

	try:
		import setproctitle
		setproctitle.setproctitle('bash')
	except ModuleNotFoundError:
		print('setproctitle modile not installed. Skipped renaming process name.')

	time_interval = 1 # seconds
	slave_pid_filepath = f'.slave-{current_pid}.pid'
	master_pid_filepath = '.master.pid'
	utilities.append_log(f'Slave {current_pid} spawned!')

	while True:
		kill_switch_value = utilities.read_file_contents('kill.switch')
		if kill_switch_value == kill_switch_secret:
			utilities.append_log(f'Slave {current_pid} noticed the kill switch! Killing himself.')
			exit()

		utilities.create_file_with_contents(slave_pid_filepath, current_pid)

		master_pid = utilities.read_file_contents(master_pid_filepath)
		if not master_pid:
			utilities.append_log(f'Slave {current_pid} noticed that master\'s PID file is empty...')
		else:
			is_running = utilities.is_pid_running(master_pid)
			if not is_running:
				utilities.append_log(f'Slave {current_pid} noticed that master {master_pid} died.')
				subprocess.Popen(['python3', 'king_protector_master.py'], stdout=subprocess.PIPE)

		time.sleep(time_interval)

def handler(signum, frame):
	handle_message = f'Someone is trying to kill slave {current_pid} with {signum}!'
	utilities.append_log(handle_message)
	print(handle_message)

if __name__ == '__main__':
	main()
