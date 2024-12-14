import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Open and read the file as a dictionary
    with open(filename) as f:
        reader = csv.DictReader(f)
        rows = [list(row.values()) for row in reader]

    # Separate variables and labels
    evidence = [row[0:17] for row in rows]
    label = [int(row[17] == 'TRUE') for row in rows]
    
    # Change data types of the variables
    months = ['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec']
    for e in evidence:
        e[0] = int(e[0])
        e[1] = float(e[1])
        e[2] = int(e[2])
        e[3] = float(e[3])
        e[4] = int(e[4])
        e[5] = float(e[5])
        e[6] = float(e[6])
        e[7] = float(e[7])
        e[8] = float(e[8])
        e[9] = float(e[9])
        e[10] = months.index(e[10])
        e[11] = int(e[11])
        e[12] = int(e[12])
        e[13] = int(e[13])
        e[14] = int(e[14])
        e[15] = int(e[15] == 'Returning_Visitor')
        e[16] = int(e[16] == 'TRUE')
    return(evidence,label)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    # Return a KNN model trained with evidence and labels
    return KNeighborsClassifier(n_neighbors = 1).fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    # Check if all labels are 1s or 0s to avoid dividing by 0
    if sum(labels) == 0:
        raise Exception("All lables are 0s")
    if len(labels) == sum(labels):
        raise Exception("All lables are 1s")

    # Calculate sensitivity using doc product of labels and predictions
    sensitivity = sum([p * l for p, l in list(zip(predictions, labels))]) / sum(labels)

    # Calculate specificity using filter
    specificity = sum([1 for p, l in list(zip(predictions, labels)) if p == 0 and l == 0]) / (len(labels) - sum(labels))
    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
