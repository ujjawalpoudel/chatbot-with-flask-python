from service.machineLearning.machineLearningModel import le


# Define a function to predicted disease labels
def disease_prediction(predictions):
    # Extract the predicted label indices from the first element of the predictions array
    predicted_label_indices = predictions[0].nonzero()[0]

    # Map the predicted label indices to their corresponding label names using the label encoder
    predicted_labels = le.inverse_transform(predicted_label_indices)

    # predicted disease labels, stripping any leading or trailing white space
    predicted_labels = list(map(lambda x: x.strip(), list(predicted_labels)))

    # Return the predicted disease labels as a list
    return predicted_labels
