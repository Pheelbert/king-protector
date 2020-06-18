# Dependencies
- python 3.8 is needed for setproctitle to work
- Look at requirements.txt

# Usage
Run master with no arguments.

# Explanation
Master writes to king.txt in a while True loop. X slaves are spawned which are tasked to look if the master is alive and respawning him if he isn't. The master also respawns slaves if they are killed. Kill -9 cannot be handled afaik, but other signals are handled and ignored on both the master and slaves.
