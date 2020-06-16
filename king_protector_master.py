import os
import time
import glob
import setproctitle
import subprocess
import utilities

def main():
	username = 'pheelbert'
	king_filepath = 'king.txt'
	pid_filepath = '.king.pid'
	time_interval = 1 # seconds
	time_elapsed = 0
	max_slave_count = 10

	setproctitle.setproctitle('bash')
	pid = str(os.getpid())
	utilities.create_file_with_contents(pid_filepath, pid)
	subprocess.call('rm -rf slave-*.pid', shell=True)

	while True:
		running_slaves_count = 0
		slave_filepaths = glob.glob('.slave-*.pid')
		for slave_filepath in slave_filepaths:
			pid = slave_filepath.replace('.slave-', '').replace('.pid', '')
			is_running = utilities.is_pid_running(pid)
			if is_running:
				running_slaves_count += 1
			else:
				os.remove(slave_filepath)

		if running_slaves_count < max_slave_count:
			slaves_spawn_count = max_slave_count - running_slaves_count
			for i in range(slaves_spawn_count):
				print(f'{slaves_spawn_count} slaves down! Spawning...')
				subprocess.Popen(['python3', 'king_protector_slave.py'])
		else:
			print(f'{running_slaves_count} slaves are protecting you...')

		previous_pid = utilities.read_file_contents(pid_filepath)
		if previous_pid and previous_pid != pid:
			print('Killing process because another master has arrived.')
			exit()

		previous_username = utilities.read_file_contents(king_filepath)
		if previous_username and previous_username != username:
			print(f'{previous_username} had replaced you as a king!')
		else:
			print(f'You\'ve remained king for {time_elapsed} seconds')

		utilities.create_file_with_contents(king_filepath, username)
		utilities.create_file_with_contents(pid_filepath, pid)

		time.sleep(time_interval)
		time_elapsed += time_interval

if __name__ == '__main__':
	main()
