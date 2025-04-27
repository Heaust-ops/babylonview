import os
import shutil

from .globals import SCRIPT_DIR, TMP_PATH

tmp_path = TMP_PATH
class TmpFolder():
    @staticmethod
    def ensure():
        os.makedirs(tmp_path, exist_ok=True)

    @staticmethod
    def mirror(path):
        os.makedirs(tmp_path, exist_ok=True)

        filename = os.path.basename(path)
        dest = os.path.join(tmp_path, filename)

        shutil.copy2(path, dest)
        return os.path.relpath(dest, SCRIPT_DIR)
        
    
    @staticmethod
    def remake():
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
        os.makedirs(tmp_path)
