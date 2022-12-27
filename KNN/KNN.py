from collections import Counter
from metrics import *


class KNN:

    def __init__(self, k=3):
        self.k = k
        self.training_data = None
        self.training_labels = None

    def fit(self, training_data, training_labels):
        if self.training_data is None or self.training_labels is None:
            self.training_data = training_data
            self.training_labels = training_labels
        else:
            self.training_data = np.concatenate((self.training_data, training_data))
            self.training_labels = np.concatenate((self.training_labels, training_labels))

    def predict(self, test_data, metric=euclidean):
        if self.training_data is None or self.training_labels is None:
            raise ValueError("You have to train model first.")

        lengths = metric(test_data, self.training_data)

        k_neighbours_indices = np.argsort(lengths)[:, :self.k]

        rows, columns = k_neighbours_indices.shape

        predictions = []

        for row_index in range(rows):
            dummy = []

            for column_index in range(columns):
                cell = k_neighbours_indices[row_index][column_index]
                dummy.append(self.training_labels[cell])

            prediction = Counter(dummy).most_common(1)[0][0]
            predictions.append(prediction)

        return np.array(predictions)


if __name__ == "__main__":
    from sklearn import datasets
    from sklearn.model_selection import train_test_split


    def measure_accuracy(correct_labels, predicted_labels):
        accuracy = np.sum(correct_labels == predicted_labels) / len(correct_labels)

        return accuracy


    iris = datasets.load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=1234
    )

    knn_3 = KNN()
    knn_5 = KNN(5)
    knn_7 = KNN(7)

    knn_3.fit(X_train, y_train)
    knn_5.fit(X_train, y_train)
    knn_7.fit(X_train, y_train)

    print(15 * "-")

    predictions_3 = knn_3.predict(X_test, metric=euclidean)
    predictions_5 = knn_5.predict(X_test, metric=euclidean)
    predictions_7 = knn_7.predict(X_test, metric=euclidean)

    print("accuracy: ", measure_accuracy(y_test, predictions_3))
    print("accuracy: ", measure_accuracy(y_test, predictions_5))
    print("accuracy: ", measure_accuracy(y_test, predictions_7))

    print(15 * "-")

    predictions_3 = knn_3.predict(X_test, metric=chebyshev)
    predictions_5 = knn_5.predict(X_test, metric=chebyshev)
    predictions_7 = knn_7.predict(X_test, metric=chebyshev)

    print("accuracy: ", measure_accuracy(y_test, predictions_3))
    print("accuracy: ", measure_accuracy(y_test, predictions_5))
    print("accuracy: ", measure_accuracy(y_test, predictions_7))

    print(15 * "-")

    predictions_3 = knn_3.predict(X_test, metric=manhattan)
    predictions_5 = knn_5.predict(X_test, metric=manhattan)
    predictions_7 = knn_7.predict(X_test, metric=manhattan)

    print("accuracy: ", measure_accuracy(y_test, predictions_3))
    print("accuracy: ", measure_accuracy(y_test, predictions_5))
    print("accuracy: ", measure_accuracy(y_test, predictions_7))

    print(15 * "-")

    predictions_3 = knn_3.predict(X_test, metric=cosine)
    predictions_5 = knn_5.predict(X_test, metric=cosine)
    predictions_7 = knn_7.predict(X_test, metric=cosine)

    print("accuracy: ", measure_accuracy(y_test, predictions_3))
    print("accuracy: ", measure_accuracy(y_test, predictions_5))
    print("accuracy: ", measure_accuracy(y_test, predictions_7))
