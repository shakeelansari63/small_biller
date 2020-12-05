import os
import json

# Identify App Path
apppath = os.path.dirname(__file__)

# settings File
settings_file = os.path.join(apppath, 'res/settings.json')

# Read Settings
with open(settings_file, 'r') as set:
    setting = json.load(set)

# Append Paths to files
setting['appicon'] = os.path.join(apppath, setting['appicon'])
setting['appdb'] = os.path.join(apppath, setting['appdb'])
setting['delbtn'] = os.path.join(apppath, setting['delbtn'])
setting['updbtn'] = os.path.join(apppath, setting['updbtn'])
