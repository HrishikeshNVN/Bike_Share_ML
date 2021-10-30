import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from split_data import Split_data

class Feature_select:

    """
                Class Name: Feature_select
                Description: This class method performs all feature selection processes on user given data.
                Output: training and testing data with selected feature names.
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
    """


    def __init__(self,file_obj,logger_obj):

        self.logger_obj = logger_obj
        self.file_obj=file_obj
        split_obj = Split_data(self.file_obj,self.logger_obj)
        self.X_train,self.X_test,self.y_train,self.y_test = split_obj.get_train_test_os()

    def get_data_selected_features(self):

        self.logger_obj.log(self.file_obj,'Entered in get_data_selected_features of Feature_select class.')

        try:
            self.feature_selection()
            return self.X_train,self.X_test,self.y_train,self.y_test,self.best_feat_df.columns  
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Feature selection failed...'+str(e))
            raise Exception()

        

    def feature_selection(self):
        
        self.logger_obj.log(self.file_obj,'Started Feature selection method......')

        try:
            feat_sel = SelectKBest(score_func=f_regression, k=(len(self.X_train.columns)))
            fs = feat_sel.fit(self.X_train,self.y_train)
            features = pd.DataFrame(self.X_train.columns)
            f_scores = pd.DataFrame(np.round(fs.scores_,4))
            p_value = pd.DataFrame(np.round(fs.pvalues_,4))
            top_features = pd.concat([features,f_scores,p_value], axis=1)
            top_features.columns = ["features","f_scores","p_value"]
            best_features = top_features[top_features["p_value"]<0.05]["features"]
            self.best_feat_df = pd.DataFrame(columns=best_features)
            self.best_feat_df.to_csv("csv_files/best_features.csv",index=False)  
            self.logger_obj.log(self.file_obj,'Features selected Successfully.. Exited Feature selection method....')
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Error occured at feature_selection method of Feature_select ...'+str(e))
            raise Exception()



        
