
from sklearn.tree import _tree

from machine_learning_model import le,reduced_data


def print_disease(node):
    node = node[0]
    val  = node.nonzero() 
    disease = le.inverse_transform(val[0])
    return list(map(lambda x:x.strip(),list(disease)))

def recurse(tree_predict, feature_name, disease_input, node=0, depth=1):
    symptoms_given = []    # list of symptoms to ask about
    symptoms_present = []  # list of symptoms already present in the diagnosis
    
    # Check if the current node is a leaf node
    if tree_predict.feature[node] != _tree.TREE_UNDEFINED:
        # If not, get the name of the current feature and its threshold value
        name = feature_name[node]
        threshold = tree_predict.threshold[node]
        
        # Check if the current feature is the disease we are diagnosing
        if name == disease_input:
            val = 1
        else:
            val = 0
            
        print("val, threshold", val, threshold)
        print (val <= threshold)
            
        # Determine which child node to traverse based on the feature value
        if val <= threshold:
            # If the feature value is less than or equal to the threshold, go left
            return recurse(tree_predict, feature_name, disease_input, tree_predict.children_left[node], depth + 1)
        else:
            # If the feature value is greater than the threshold, go right
            symptoms_present.append(name)
            return recurse(tree_predict, feature_name, disease_input, tree_predict.children_right[node], depth + 1)
    else:
        # If the current node is a leaf node, we have diagnosed a disease
        present_disease = print_disease(tree_predict.value[node])
        red_cols = reduced_data.columns
        # Get the list of symptoms associated with the diagnosed disease
        symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
    
    # Return the list of symptoms to ask about
    return list(symptoms_given)

        
        
def tree_to_code(tree, feature_names, disease_input, days):
    # Get the underlying decision tree object
    tree_ = tree.tree_
    
    # Map the feature indices to feature names
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    # Recursively traverse the decision tree to determine which symptoms to ask about
    symptoms_given = recurse(tree_, feature_name, disease_input)
    
    # Return the list of symptoms to ask about
    return symptoms_given



