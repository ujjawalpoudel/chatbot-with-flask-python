from service.machineLearning.machineLearningModel import (
    clf,
    symptoms_dict,
    input_vector,
)


def make_suggestion(symptoms_exp):
    """
    Given a set of symptoms, creates an input vector and predicts the most likely disease using a trained decision tree classifier.

    Args:
    symptoms_exp (dict): A dictionary of symptoms and their values.

    Returns:
    A string representing the predicted disease based on the given symptoms.
    """
    # * Set the values of the symptoms in the input vector
    for item in symptoms_exp:
        input_vector[[symptoms_dict[item]]] = symptoms_exp[item]

    # * Predict the most likely disease using the trained decision tree classifier
    predicted_disease = clf.predict([input_vector])[0]

    # * Return the predicted disease as a string
    return predicted_disease
