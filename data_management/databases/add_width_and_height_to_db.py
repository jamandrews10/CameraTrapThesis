########
#
# add_width_and_height_to_db.py
#
# Grabs width and height from actual image files for a .json database that is missing w/h.
#
########

#%% Imports and constants

import json
from PIL import Image

datafile = '/datadrive/snapshotserengeti/databases/snapshotserengeti.json'
image_base = '/datadrive/snapshotserengeti/images/'


#%% Execution

with open(datafile,'r') as f:
    data = json.load(f)

for im in data['images']:
    if 'height' not in im:
        im_w, im_h = Image.open(image_base+im['file_name']).size
        im['height'] = im_h
        im['width'] = im_w

json.dump(data, open(datafile,'w'))
