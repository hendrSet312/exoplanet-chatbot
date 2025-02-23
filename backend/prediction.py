import pandas as pd
import joblib 
import xgboost
import matplotlib.pyplot as plt
import shap
import json

class modelling:
    def __init__(self, data_parameter : dict):
        self.__ohe = joblib.load('backend/one_hot_encoder.pkl')
        self.__xgboost = joblib.load('backend/xgboost.pkl')
        self.__name = data_parameter['P_NAME'] if 'P_NAME' in data_parameter else 'new_planet'
        self.__data = pd.DataFrame(data=data_parameter,index = [0])
        self.__transformed_data = self.__data.copy()

        for detected_col in ['P_NAME','P_DETECTION','P_DISCOVERY_FACILITY','P_YEAR']:
            if detected_col in data_parameter:
                self.__transformed_data = self.__transformed_data.drop(columns=detected_col)

    def get_data(self):
        return self.__transformed_data

    def transform_data(self):
        numerical_features= self.get_data().select_dtypes(include=['number']) 
        categorical_features= self.get_data().select_dtypes(include=['object'])

        x_cat = self.__ohe.transform(categorical_features)
        x_cat = pd.DataFrame(x_cat, columns=self.__ohe.get_feature_names_out(categorical_features.columns.tolist()))
        x_cat = pd.concat([numerical_features.reset_index(drop=True), x_cat], axis=1)

        return x_cat
    
    def shap_explainer(self, prediction_data, result : int):
        explainer = shap.TreeExplainer(self.__xgboost)
        shap_values = explainer(prediction_data)

        shap.plots.bar(shap_values[0,:,result])

        link = f"media/image/planets/{self.__name}.png"
        plt.savefig(link, bbox_inches="tight", dpi=300)

        sample_shap_values = shap_values[0].values[:,result].round(4)
        feature_names = shap_values[0].feature_names

        # Combine into a dictionary for easier viewing
        shap_dict = dict(zip(feature_names, sample_shap_values))
        shap_dict = dict(sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True))
        shap_dict = ', '.join(f"{key}: {value}" for key, value in shap_dict.items())
        plt.close()


        return {'link' : link , 'description' : shap_dict}

    
    def predicting_data(self):
        dict_pred = {0 : 'Tidak dapat ditempati', 1 : 'Secara konservatif dapat ditempati', 2: 'Secara optimis dapat ditempati'}
        transformed_data = self.transform_data()
        prediction = self.__xgboost.predict_proba(transformed_data).ravel()

        final_pred = prediction.argmax()

        image_intepret_output = self.shap_explainer(transformed_data, final_pred)

        return {'input': self.__data ,'number' : final_pred ,'label' : dict_pred[final_pred], 'probability' : prediction[final_pred] , 'image': image_intepret_output['link'], 'description': image_intepret_output['description']}
    


