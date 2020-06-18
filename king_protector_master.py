import glob
import os
import signal
import subprocess
import time
import utilities

kill_switch_secret = 'kill' # Set secret in file called 'kill.switch' to kill all.
current_pid = str(os.getpid())

# Usage: python3 king_protector_master.py
def main():
	signal.signal(signal.SIGABRT, handler)
	signal.signal(signal.SIGTERM, handler)
	signal.signal(signal.SIGINT, handler)
	
	try:
		import setproctitle
		setproctitle.setproctitle('bash')
	except ModuleNotFoundError:
		print('setproctitle modile not installed. Skipped renaming process name.')

	username = 'pheelbert'
	king_filepath = 'king.txt'
	pid_filepath = '.master.pid'
	time_interval = 1 # seconds
	time_elapsed = 0
	max_slave_count = 10

	utilities.create_file_with_contents(pid_filepath, current_pid)
	utilities.append_log(f'Master {current_pid} spawned!')

	subprocess.call('rm -rf slave-*.pid', shell=True)

	while True:
		kill_switch_value = utilities.read_file_contents('kill.switch')
		if kill_switch_value == kill_switch_secret:
			utilities.append_log(f'Master {current_pid} noticed the kill switch! Killing himself.')
			print('Kill switch found!')
			exit()

		previous_pid = utilities.read_file_contents(pid_filepath)
		if previous_pid and previous_pid != current_pid:
			print(f'Killing process because another master (new: {previous_pid}, current: {current_pid}) has arrived.')
			exit()

		utilities.create_file_with_contents(king_filepath, username)
		utilities.create_file_with_contents(pid_filepath, current_pid)

		running_slaves_count = 0
		slave_filepaths = glob.glob('.slave-*.pid')
		for slave_filepath in slave_filepaths:
			slave_pid = slave_filepath.replace('.slave-', '').replace('.pid', '')
			is_running = utilities.is_pid_running(slave_pid)
			if is_running:
				running_slaves_count += 1
			else:
				os.remove(slave_filepath)

		if running_slaves_count < max_slave_count:
			slaves_spawn_count = max_slave_count - running_slaves_count
			print(f'{slaves_spawn_count} slaves down! Spawning...')
			for i in range(slaves_spawn_count):
				subprocess.Popen(['python3', 'king_protector_slave.py'], stdout=subprocess.PIPE)
		else:
			print(f'{running_slaves_count} slaves are protecting you...')

		previous_username = utilities.read_file_contents(king_filepath)
		if previous_username and previous_username != username:
			print(f'"{previous_username.strip()}" had replaced you as a king!')
		else:
			print(f'You\'ve remained king for {time_elapsed} seconds')

		time.sleep(time_interval)
		time_elapsed += time_interval

def handler(signum, frame):
	handle_message = f'Someone is trying to kill master {current_pid} with {signum}!'
	utilities.append_log(handle_message)
	print(handle_message)

if __name__ == '__main__':
    main()
