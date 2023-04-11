# * Import Python Module
from sklearn.tree import _tree

# * Import User Defined Function
from machine_learning_model import le, reduced_data
from service.machineLearning.getDiseaseName import disease_prediction


def recurse_node_depth(tree_predict, feature_name, disease_input, node=0, depth=1):
    symptoms_given = []  # list of symptoms to ask about
    symptoms_present = []  # list of symptoms already present in the diagnosis

    # Check if the current node is a leaf node
    if tree_predict.feature[node] != _tree.TREE_UNDEFINED:
        # If not, get the name of the current feature
        name = feature_name[node]

        # Check if the current feature is the disease we are diagnosing
        if name == disease_input:
            # If so, add the feature to the list of symptoms present in the diagnosis
            symptoms_present.append(name)
            # Traverse the right child node to continue diagnosing
            return recurse_node_depth(
                tree_predict,
                feature_name,
                disease_input,
                tree_predict.children_right[node],
                depth + 1,
            )
        else:
            # If not, traverse the left child node to continue diagnosing
            return recurse_node_depth(
                tree_predict,
                feature_name,
                disease_input,
                tree_predict.children_left[node],
                depth + 1,
            )
    else:
        # If the current node is a leaf node, we have diagnosed a disease
        present_disease = disease_prediction(tree_predict.value[node])
        red_cols = reduced_data.columns
        # Get the list of symptoms associated with the diagnosed disease
        symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]

    # Return the list of symptoms to ask about
    return list(symptoms_given)


def get_all_symptoms(tree, feature_names, disease_input):
    # Get the underlying decision tree object
    tree_ = tree.tree_

    # Map the feature indices to feature names
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    # Recursively traverse the decision tree to determine which symptoms to ask about
    symptoms_given = recurse_node_depth(tree_, feature_name, disease_input)

    # Return the list of symptoms to ask about
    return symptoms_given
