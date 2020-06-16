import os
import time

def main():
	# Start master process which is protected by a bunch of slaves which boot it back up if taken down.
	# The master keeps spawning slaves as long as there is less than x.
	# Master process simply squashes the file repeatedly with the username to remain king.

	username = 'pheelbert'
	king_filepath = 'king.txt'
	time_interval = 1 # seconds
	time_elapsed = 0

	while True:
		previous_username = read_file_contents(king_filepath)
		if previous_username and previous_username != username:
			print(f'{previous_username} had replaced you as a king!')
		else:
			print(f'You\'ve remained king for {time_elapsed} seconds')

		write_username_to_king_file(username, king_filepath)

		time.sleep(time_interval)
		time_elapsed += time_interval

def write_username_to_king_file(username, king_filepath):
	create_file_with_contents(king_filepath, username)

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

if __name__ == '__main__':
	main()
