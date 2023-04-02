import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import pickle

def load_data():
    return pd.read_csv('basic/data/student_data.csv')

def student_perfomance_prediction(gender, race, parent_edu, lunch, prep_course):
    student = load_data()
    X_category = student[['gender','race/ethnicity','parental level of education','lunch','test preparation course']]

    # Applying one-hot encoding to each column with categorical data
    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    X_OH = pd.DataFrame(OH_encoder.fit_transform(X_category))
    X_OH.index = X_category.index #One-hot encoding removes the index so it's necessary to put them back

    input = {'gender':gender,'race/ethnicity':race,'parental level of education':parent_edu,'lunch':lunch,'test preparation course':prep_course}
    df_input = pd.DataFrame(input,index=[0])
    input_oh = OH_encoder.transform(df_input)

    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open('basic/data/'+filename, 'rb'))

    result = loaded_model.predict(input_oh)
    return result
