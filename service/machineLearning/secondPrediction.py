from service.machineLearning.machineLearningModel import (
    clf,
    input_vector,
    symptoms_dict,
)


# Define a function to make a disease prediction based on the symptoms experienced by a patient
def make_disease_prediction(symptoms_experience):
    # Loop through each symptom in the input list and set the corresponding element in the input vector to 1
    for symptom in symptoms_experience:
        symptom_index = symptoms_dict[symptom]
        input_vector[symptom_index] = 1

    # Use the classifier to predict the disease based on the input vector
    prediction = clf.predict([input_vector])

    # Return the predicted disease as an array
    return prediction
