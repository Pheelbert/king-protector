# Dependencies
- python 3.8 is needed for setproctitle to work
- Look at requirements.txt

# Usage
Since you're supposed to be root when you need this, you can git clone directly or upload a zip. Once it's on the machine, change the king.txt path and run master with no arguments.

# Explanation
Master writes to king.txt in a while True loop. X slaves are spawned which are tasked to look if the master is alive and respawning him if he isn't. The master also respawns slaves if they are killed. Kill -9 cannot be handled afaik, but other signals are handled and ignored on both the master and slaves.

# TODO
- Hide master and slaves in other processes
- Create "game" environment where a referee is checking every x interval whose username is in the king.txt file. Try running two different implementations and see who wins!
