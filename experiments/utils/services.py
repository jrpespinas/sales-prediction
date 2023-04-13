import glob
import shutil
import os
from joblib import dump

def get_current_model() -> str:
    """Retrieve filename of the existing model from the model store"""
    path = r"../model_store/*.joblib"
    try:
        return glob.glob(path)[0]
    except:
        return ""

def move_current_model_to_archive():
    """Move existing model to archive"""
    try:
        src_path = get_current_model()
        dst_path = r"../model_store/archive"
        shutil.move(src_path, dst_path)
    except:
        return
    
def get_number_of_models_in_archive() -> int:
    """Count the number of models in the archive"""
    count = 0
    dir_path = r"../model_store/archive/"
    for path in os.scandir(dir_path):
        if path.is_file():
            count += 1
    return count

def save_to_model_store(model):
    """Save model to model store"""
    get_current_model()
    move_current_model_to_archive()
    model_num = get_number_of_models_in_archive() + 1
    dump(model, f"../model_store/sales_prediction_{model_num}.joblib")