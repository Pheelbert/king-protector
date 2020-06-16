import os
import setproctitle
import subprocess
import time
import utilities

def main():
	time_interval = 1 # seconds
	setproctitle.setproctitle('bash')
	pid = str(os.getpid())
	slave_pid_filepath = f'.slave-{pid}.pid'
	master_pid_filepath = '.king.pid'

	while True:
		utilities.create_file_with_contents(slave_pid_filepath, pid)

		master_pid = utilities.read_file_contents(master_pid_filepath)
		is_running = utilities.is_pid_running(master_pid)
		if not is_running:
			print('Master isn\'t running! Spawning...')
			subprocess.Popen(['python3', 'king_protector_master.py'])

		time.sleep(time_interval)

if __name__ == '__main__':
	main()
