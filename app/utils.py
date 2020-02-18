import os
import shutil
import inspect
def zip_dir(path:str,name:str=None):
    """
    Zip a directory and return the path to the zip file.\n
    `path` The path to the directory to zip\n
    `name` The name to give the .zip file. Defaults to name of zipped directory
    """
    if not name:
        name =os.path.basename(path)
        if not name:
            name='archive'
    if name.endswith('.zip'):
        name=name[:-4]
    return shutil.make_archive(name, 'zip', path)

def unzip_dir(path:str,name:str=None):
    if not name:
        name =os.path.basename(path)
        if not name:
            name='archive'
    return shutil.unpack_archive(path,name)

def local_path(*args):
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    mod_dir_path=os.path.split(mod.__file__)[0]
    return os.path.join(mod_dir_path,*args)