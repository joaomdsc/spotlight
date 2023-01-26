import os
from PIL import Image
from shutil import copyfile

def image_files(path):
    """Spotlight image files beneath a .spot directory hierarchy.

    This code assumes that there is an 'img' directory under path, and a series
    of sub-directories under 'img'. The code generates the filepaths to all the
    horizontal image files found under those sub-directories.
    """
    img_path = os.path.join(path, 'img')
    for f in os.listdir(img_path):
        # Date/time sub-dirs
        dt_path = os.path.join(img_path, f)
        for f in os.listdir(dt_path):
            if not f.endswith('.jpg'):
                continue
            filepath = os.path.join(dt_path, f)
            with Image.open(filepath) as im:
                w, h = im.size
                if w > h:
                    yield filepath

def copy_images(dst, path):
    """Copy all image files under 'path' to 'dst', warn if already existing."""
    cnt = 0
    for filepath in image_files(path):
        filename = os.path.basename(filepath)
        dst_path = os.path.join(dst, filename)
        if not os.path.isfile(dst_path):
            copyfile(filepath, dst_path)
            cnt += 1
    return cnt
        
#===============================================================================
# main
#===============================================================================

if __name__ == '__main__':
    dst = os.path.join(os.getenv ('HOME'), r'privé\Spotlight\master')
    src = os.path.join(os.getenv ('HOME'), '.spot')
    cnt = copy_images(dst, src)
    print(f'Copied {cnt} new images from {src} to {dst}')
    
