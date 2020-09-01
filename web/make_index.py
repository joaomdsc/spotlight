# spotlight/web/make_index.py

"""This script generates the index.html file with all the image thumbnails.

It first checks to see whether any new files have been added that do not have a
thumbnail, in which case it will create the thumbnail.
"""

import os

from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Directory where we store the Spotlight service image files
home_path = os.getenv('HOME')
spot_path = os.path.join(home_path, r'privé\Spotlight\master')
thumbs_path = os.path.join(home_path, r'privé\Spotlight\thumbnails')

#-------------------------------------------------------------------------------
# resize
#-------------------------------------------------------------------------------

def resize(src, dst):
    """Transform 1920x1080 images into 192x108."""
    im = Image.open(src)
    im_resized = im.resize((192, 108))
    im_resized.save(dst)

#-------------------------------------------------------------------------------
# thumbnails
#-------------------------------------------------------------------------------

def thumbnails():
    if not os.path.isdir(thumbs_path):
        os.makedirs(thumbs_path)

    for f in os.listdir(spot_path):
        src = os.path.join(spot_path, f)
        if not os.path.isfile(src) or not src.endswith('.jpg'):
            continue
        dst = f'{os.path.join(thumbs_path, f)}'
        if not os.path.exists(dst):
            resize(src, dst)

#-------------------------------------------------------------------------------
# image_array
#-------------------------------------------------------------------------------

def image_array():
    """Return a portion of HTML with all the image links."""
    arr = []

    for f in os.listdir(spot_path):
        if not f.endswith('.jpg'):
            continue
        spot_filepath = os.path.join(spot_path, f)
        thumb_filepath = os.path.join(thumbs_path, f)

        # The 'file:///" protocol is required by firefox
#         arr.append(f""" --><a href="file://{spot_filepath}"><!--
#   --><img id="spot" src="file:///{thumb_filepath}"/><!--
# --></a><!--""")
        
        arr.append(f' --><img src="file:///{thumb_filepath}"/><!--')

    return '\n'.join(arr)

#-------------------------------------------------------------------------------
# render_html
#-------------------------------------------------------------------------------

def render_html():
    """Render the HTML template with the image array data."""
    env = Environment(
        loader=FileSystemLoader('.'),
    )
    t = env.get_template('index.tmpl.html')
    s = t.render(image_array=image_array())

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(s)

#===============================================================================
# main
#===============================================================================

thumbnails()
render_html()