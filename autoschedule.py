import os
A = os.path.join(os.path.dirname(__file__), '..')
# A is the parent directory of the directory where program resides.

B = os.path.dirname(os.path.realpath(__file__))
# B is the canonicalised (?) directory where the program resides.

C = os.path.abspath(os.path.dirname(__file__))
# C is the absolute path of the directory where the program resides.

import sys
from importlib import reload

import schedule
import time
import git  # GitPython
from git.exc import GitCommandError
import logging
from datetime import datetime, timedelta
import threading

sys.path.append(C)

logging.basicConfig(filename=os.path.join(C, "main.log"), level=logging.DEBUG, format="%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
logging.getLogger("schedule").setLevel(logging.WARNING + 10)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING + 10)

jobs = dict()


def live_exec():
	"You can add jobs on the fly"
	current_file_directory = os.path.abspath(os.path.dirname(__file__))
	# sys.path.append(current_file_directory)  # TODO à tester

	for file in os.listdir(C):
		if file.startswith("command_"):
			logging.info(f"New script to be live evaluating: {file}")
			abs_path_file = os.path.join(C, file)
			with open(abs_path_file, "r") as f_in:
				code = f_in.read()
			try:
				exec(code)
			except Exception:
				import traceback
				logging.error(f"ERROR live evaluating: {file}\n{traceback.format_exc()}")
				os.rename(os.path.join(current_file_directory, file),
						os.path.join(current_file_directory, "error_" + file))
				abs_path_error_file = os.path.join(current_file_directory, "error_" + file)
				with open(abs_path_error_file, "w") as f_out:
					f_out.write(code + "\n#" + str(e))
			else:
				logging.info(f"SUCCESS live evaluating: {file}")
				os.rename(os.path.join(current_file_directory, file),
						os.path.join(current_file_directory, "old_" + file))


def update_price_wubook():
	wubook_abs_path = os.path.join(C, "PyWubook")
	g = git.cmd.Git(wubook_abs_path)
	sys.path.append(wubook_abs_path)
	from PyWubook import main as main_pywubook
	
	def wrapper(days):
		logging.info("Fonction update_price_wubook en cours d’exécution")
		
		try:
			pull_result = g.pull()
			if pull_result != 'Already up to date.':
				[reload(module) for module in list(sys.modules.values())[::-1] if "PyWubook" in str(module)]
				logging.info("Changed in PyWubook code. PyWubook’s modules reloaded.")

		except GitCommandError as e:
			logging.warning(f"Git not accessible, the function continue: {e}")
		
		
		try:
			main_pywubook.main(days)
		except Exception:
			# Annuler la plannification du job
			# if "update_price_wubook" in jobs:
			# 	schedule.cancel_job(jobs.get("update_price_wubook"))
			import traceback
			logging.error(f"Exception dans la fonction update_price_wubook, ce job est arrêté: \n{traceback.format_exc()}")
		logging.info("Fonction update_price_wubook FIN d’exécution")
	
	return wrapper

def ring_door_bell():
	def job():
		logging.info("Fonction ring_door_bell en cours d’exécution")

		doorbird_abs_path = os.path.join(C, "PyDoorbird")
		g = git.cmd.Git(doorbird_abs_path)
		sys.path.append(doorbird_abs_path)
		try:
			pull_result = g.pull()
			if pull_result != 'Already up to date.':
				logging.info("Changed in PyDoorbird code")
		except GitCommandError as e:
			logging.warning(f"Git not accessible, the function continue: {e}")
		
		
		from PyDoorbird import pydoorbird
		try:
			pydoorbird.main()
		except Exception:
			import traceback
			logging.error(f"Exception dans la fonction ring_door_bell, ce job est à execution unique: \n{traceback.format_exc()}")

	job_thread = threading.Thread(target=job)
	job_thread.start()
	return schedule.CancelJob


try:
	jobs["update_price_wubook"] = schedule.every().hour.do(update_price_wubook(), 360)
	jobs["live_exec"] = schedule.every().minute.do(live_exec)
	t_plus_2 = (datetime.now() + timedelta(minutes=2)).strftime("%H:%M")
	jobs["ring_door_bell"] = schedule.every().day.at(t_plus_2).do(ring_door_bell)

	logging.info("Les taches démarrent")
	while True:
		schedule.run_pending()
		time.sleep(1)
except Exception:
	import traceback
	logging.critical(f"une exception s’est levée, les taches vont s’arrêter: {traceback.format_exc()}")
finally:
	logging.info("Les taches ne sont plus exécutées")