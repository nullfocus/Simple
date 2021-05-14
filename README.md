__This project does not take any security considerations into account currently (or ever)! Please use Jenkins or something similar if you care at all about your system!__


# Zapper
_def: slang for a remote control_

A simple webapp that lists and executes shell scripts, and displays their output.

This grew out of my home automation desires to have a simple page where I could fire off scripts on my home server, and see their output. I wanted to avoid needing to run a full webserver with some CGI layer, or an automation system along with a database, really anything more complex than a simple script. 

Install guide:
- Install Python 3.8
- Create a directory and subdirectory within called "scripts"
- Fill up "scripts" with shell scripts or executables (remember to chmod them)
- Run the zapper.py file in the parent folder
- Hit port 5000 on the machine's ip
