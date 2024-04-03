import hubtools
import os, traceback
from level import Level
from pathlib import Path

def loadlevel(self):
    # Reset hubtools when we load a level
    self.hub = hubtools.HubTools(self)
    kwargs = {}
    self.level_name = self.files[self.file_choice]
    hub_parent = False
    level_number = 0
    credits = ''
    difficulty = 0
    possess_vfx = 0
    if self.level_name != 'hub.txt':
        hub_parent = os.path.exists('puzzle_data.txt')
    else:
        try:
            with open('credits.txt','r', encoding="utf8") as f:
                credits = f.read()
        except:
            credits = ""
    if os.path.exists("area_data.txt"):
        kwargs["area_data"] = open('area_data.txt', 'r', encoding="utf8").read()
    if hub_parent:
        try:
            with open('puzzle_data.txt','r', encoding="utf8") as file:
                puzzle_data = {line.split(' ')[0]:line.split(' ')[1:] for line in file.read().split('\n')}
            difficulty, possess_vfx, level_number = [int(n) for n in puzzle_data[Path(self.level_name).stem]]
        except (FileNotFoundError, KeyError):
            pass
    with open(self.level_name, encoding="utf8") as file:
        try:
            self.level = Level(self.level_name, file.read(), level_number, hub_parent, difficulty, bool(possess_vfx), credits, **kwargs)
        except Exception as Err:
            print(traceback.format_exc())
            self.level_invalid=True
            
def savelevel(self):
        save_data, is_hub, parent, level_number, areas, credits, possess_fx, difficulty = self.level.save()
        with open(self.level_name, "w" if os.path.exists(self.level_name) else "x", encoding="utf8") as file:
            file.write(save_data)
        if is_hub:
            with open('credits.txt','x' if not os.path.exists('credits.txt') else 'w', encoding="utf8") as f:
                f.write(credits)
            with open('area_data.txt','x' if not os.path.exists('area_data.txt') else 'w', encoding="utf8") as f:
                f.write('\n'.join([f'{name.replace(" ","_")} {music}' if name is not None else '' for name, music in areas]))
            if not os.path.exists('save0.txt'):
                with open('save0.txt','x'):
                    pass
            if len(areas) == 0:
                self.open_warn = True
        # TODO figure out what parent is
        elif parent:
            if not os.path.exists('puzzle_data.txt'):
                with open('puzzle_data.txt','x', encoding="utf8"):
                    pass
                puzzle_data = {}
            else:
                with open('puzzle_data.txt', "r", encoding="utf8") as file:
                    puzzle_data = {line.split(' ',1)[0]:line.split(' ',1)[1] for line in file.read().split('\n')}
            # Edits puzzle data for one file (no existence check needed)
            puzzle_data[Path(self.level_name).stem] = f'{difficulty} {possess_fx} {level_number}'
            with open('puzzle_data.txt', "w", encoding="utf8") as file:
                file.write('\n'.join([key + ' ' + value for key,value in puzzle_data.items()]))