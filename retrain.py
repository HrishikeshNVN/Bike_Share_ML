import pandas as pd
import numpy as np
from logger import App_Logger
from preprocess_data import Pre_Process_data

from train_n_save_model import Model_eval

#data_process = Pre_Process_data()
#X,y = data_process.X, data_process.y
file_obj = open("log_files/logs","a")
logger_obj = App_Logger()

model_eval = Model_eval(file_obj,logger_obj)
print(model_eval.get_saved_model_n_score())
