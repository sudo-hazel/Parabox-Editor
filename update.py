import requests
import os
import time
import json
# Very jank. Use file to determine if update is new or not
INITIAL_PUSH_TIME = int(time.time())
V_FILE = "Version"
class Updater:
    def __init__(self, helper):
        REPO_API = "https://api.github.com/repos/"
        REPO = "sudo-hazel/Parabox-Editor"
        GIT_BRANCH = "master"
        # Five minutes
        # Used to prevent github timeout by waiting ourselves
        # TODO fix timeout for prod
        self.TIMEOUT = 5 * 60 * 1 #000
        # We don't need every file. Just the python files
        self.update_as = ["*.py"]
        # Builds more values
        self.helper = helper
        self.commit_url = REPO_API + REPO + "/commits/" + GIT_BRANCH
        self.zip_url = REPO_API + REPO + "/zipball/" + GIT_BRANCH 
    def upgrade(self, *args):
        self.helper.popup.append("update.found")

    def update_version(self, hash):
        v_data = {
            "hash" : str(hash),
            "last_check" : int(time.time())
        }
        with open("version","w") as v_file:
            json.dump(v_data, v_file)
    def check_latest(self, curr_hash, fresh_install=False):
        # Check for updates (popup?)
        commit_data = requests.get(self.commit_url).json()
        hash = commit_data["sha"]
        if curr_hash != hash:
            self.upgrade(hash, fresh_install)
            self.update_version(hash)
        else:
            self.update_version(curr_hash)
    def update(self):
        # give imgui a little bit of time to become presentable
        time.sleep(2)
        if not os.path.exists("version"):
            # Literally just update at this point.
            self.check_latest(None, True)
        else:
            with open("version") as v_file:
                v_data = json.load(v_file)
                if v_data["last_check"] + self.TIMEOUT < int(time.time()):
                    self.check_latest(v_data["hash"])
class UpdateThread:
    def __init__(self):
        self.running = True
        self.popup = [""]