import re
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


from getDescription import getDescription
from getSeverityDict import getSeverityDict
from getprecautionDict import getprecautionDict
from machine_learning_model import x, le,reduced_data,clf,cols


severityDictionary=getSeverityDict()
description_list = getDescription()
precautionDictionary=getprecautionDict()

symptoms_dict = {}

for index, symptom in enumerate(x):
       symptoms_dict[symptom] = index

def calc_condition(exp,days):
    sum=0
    for item in exp:
         sum=sum+severityDictionary[item]
    if((sum*days)/(len(exp)+1)>13):
        print("You should take the consultation from doctor. ")
    else:
        print("It might not be that bad but you should take precautions.")


# def check_pattern(dis_list,inp):
#     pred_list=[]
#     inp=inp.replace(' ','_')
#     patt = f"{inp}"
#     regexp = re.compile(patt)
#     pred_list=[item for item in dis_list if regexp.search(item)]
#     if(len(pred_list)>0):
#         return 1,pred_list
#     else:
#         return 0,[]
    
    
def sec_predict(symptoms_exp):
    df = pd.read_csv('Data/Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
      input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])


def print_disease(node):
    node = node[0]
    val  = node.nonzero() 
    disease = le.inverse_transform(val[0])
    return list(map(lambda x:x.strip(),list(disease)))



def recurse(tree_predict,feature_name,disease_input,node=0, depth=1):
    symptoms_given = []
    symptoms_present = []
    indent = "  " * depth
    if tree_predict.feature[node] != _tree.TREE_UNDEFINED:
        print("if running")
        name = feature_name[node]
        threshold = tree_predict.threshold[node]

        if name == disease_input:
            val = 1
        else:
            val = 0
        if  val <= threshold:
            print("first recursion")
            return recurse(tree_predict,feature_name,disease_input,tree_predict.children_left[node], depth + 1)
        else:
            print("second recursion")
            symptoms_present.append(name)
            return recurse(tree_predict,feature_name,disease_input,tree_predict.children_right[node], depth + 1)
    else:
        print("aayo ke nae")
        present_disease = print_disease(tree_predict.value[node])
        red_cols = reduced_data.columns 
        symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
        
        print("symptoms_given", symptoms_given)
        print("yaha bata gayo ke nae")
        
    print("return k garxas", list(symptoms_given))
    return list(symptoms_given)
        
        
def tree_to_code(tree, feature_names,disease_input, days):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    chk_dis=",".join(feature_names).split(",")
    print("Start")  
    # print("main call",recurse(tree_,feature_name,disease_input))
    symptoms_given= recurse(tree_,feature_name,disease_input)
    print("End")
    # print("yaha chae k aayo hola", symptoms_given)
    return symptoms_given
# getSeverityDict()
# getprecautionDict()
# tree_to_code(clf,cols)
# tree_to_code(clf,cols, "knee_pain",2)

