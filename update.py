import requests
import os
import time
import json
import shutil
from zipfile import ZipFile
# Very jank. Use file to determine if update is new or not
INITIAL_PUSH_TIME = int(time.time())
V_FILE = "Version"
class UpdateThread:
    def __init__(self):
        self.running = False
        self.progress = [""]
        self.updated = False
class Updater:
    def __init__(self, helper: UpdateThread):
        REPO_API = "https://api.github.com/repos/"
        REPO = "sudo-hazel/Parabox-Editor"
        GIT_BRANCH = "updater"
        self.dir = os.path.dirname(__file__) + os.sep
        # Five minutes
        # Used to prevent github timeout by waiting ourselves
        # TODO fix timeout for prod
        self.TIMEOUT = 5 * 60 * 1 #000
        # Builds more values
        self.helper = helper
        self.commit_url = REPO_API + REPO + "/commits/" + GIT_BRANCH
        self.zip_url = REPO_API + REPO + "/zipball/" + GIT_BRANCH 
    def upgrade(self):
        UPDATE_ZIP = "update.zip"
        self.helper.running=True
        self.helper.progress.append("update.found")
        with requests.get(self.zip_url, stream=True) as r:
            with open(self.dir + UPDATE_ZIP, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        self.helper.progress.append("update.downloaded")
        with ZipFile("update.zip", 'r') as zip:
            files = zip.namelist()
            prefix = files[0]
            for path in [f for f in files if f.endswith(".py")]:
                zip.extract(path, self.dir)
            files = os.listdir(self.dir+prefix)
            self.helper.progress.append("update.warn")
            for file in files:
                if os.path.isdir(self.dir + file):
                    shutil.rmtree(self.dir + file)
                if os.path.isdir(self.dir + prefix + file):
                    shutil.copytree(self.dir + prefix + file, self.dir + file)
                else:
                    shutil.copy(self.dir + prefix + file, self.dir + file)
            shutil.rmtree(self.dir + prefix)
            os.remove(self.dir+UPDATE_ZIP)
        self.helper.updated = True
    # Also updates helper state
    def update_version(self, hash):
        v_data = {
            "hash" : str(hash),
            "last_check" : int(time.time())
        }
        self.helper.running = False
        self.helper = None
        with open(self.dir+"version","w") as v_file:
            json.dump(v_data, v_file)
    def check_latest(self, curr_hash):
        # Check for updates (popup?)
        commit_data = requests.get(self.commit_url).json()
        hash = commit_data["sha"]
        if curr_hash != hash:
            self.upgrade()
            self.update_version(hash)
        else:
            self.update_version(curr_hash)
    def update(self):
        # give imgui a little bit of time to become presentable
        if not os.path.exists(self.dir+"version"):
            # Literally just update at this point.
            self.check_latest(None)
        else:
            with open(self.dir+"version") as v_file:
                v_data = json.load(v_file)
                if v_data["last_check"] + self.TIMEOUT < int(time.time()):
                    self.check_latest(v_data["hash"])


    