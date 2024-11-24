import math
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
import pandas as pd
from model.LogisticRegression import LogisticRegression
from sklearn.model_selection import train_test_split


def change_bool_to_number(row):
    if row["is_fraud"]:
        return 1
    else:
        return 0


def clean_csv(df):
    df["SellerAuctionCount"].fillna(df["SellerAuctionCount"].mean())
    df["SellerAuctionSaleCount"].fillna(df["SellerAuctionSaleCount"].mean())
    # df["is_fraud"] = df.apply(change_bool_to_number, axis=1)
    return df


def precision_curve(y_test, y_scores):

    # Assuming y_test and y_scores are defined
    precision, recall, thresholds = precision_recall_curve(y_test, y_scores)

    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, marker='.')
    plt.title("Precision-Recall Curve")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.grid()
    plt.show()
    plt.savefig("precision.png")
    plt.close()


def plot_roc_curve(y_test, y_scores):
    """
    Plot the ROC curve for the model.

    Parameters:
    - y_test: True labels
    - y_scores: Predicted probabilities or decision scores
    """
    fpr, tpr, thresholds = roc_curve(y_test, y_scores)
    auc_score = roc_auc_score(y_test, y_scores)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f"AUC = {auc_score:.2f}", color="darkorange")
    plt.plot([0, 1], [0, 1], 'k--', label="Random Guess")
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.grid()
    plt.savefig("roc_curve.png")
    plt.show()
    plt.close()


def plot_prediction_distribution(y_test, y_scores):
    """
    Plot the distribution of predicted probabilities.

    Parameters:
    - y_test: True labels
    - y_scores: Predicted probabilities for the positive class
    """
    plt.figure(figsize=(8, 6))
    plt.hist(y_scores[y_test == 0], bins=30, alpha=0.5, label="Class 0", color="blue")
    plt.hist(y_scores[y_test == 1], bins=30, alpha=0.5, label="Class 1", color="red")
    plt.title("Distribution of Predicted Probabilities")
    plt.xlabel("Predicted Probability")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid()
    plt.savefig("predicted_probability_distribution.png")
    plt.show()
    plt.close()


def main():
    df = pd.read_csv('data/ebay_dataset.csv')
    df = clean_csv(df)
    model = LogisticRegression(learning_rate=0.0001, num_iterations=1500)
    print(df.head())
    df = df.drop(columns=["EbayID", "SellerName", "AuctionSaleRatio",
                 "MedianPriceDeviation", "ReturnRate", "HighReturnRate"])
    X = df.drop(columns=['is_fraud'])  # Replace 'is_fraud' with your actual target column name
    y = df['is_fraud']
    print(X)
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

    model.fit(X_train, y_train)
    model.plot_loss()
    print(model.bias)
    print(model.weights)
    predictions = model.predict(X_test)
    model.plot_confusion_matrix(y_test, predictions)
    print(model.calculate_accuracy(y_test, predictions))
    precision_curve(y_test, predictions)
    plot_roc_curve(y_test, predictions)
    plot_prediction_distribution(y_test, predictions)
    while True:
        x = int(input("enter autcion count: "))
        b = int(input("enter sale count: "))
        z = int(input("enter return count: "))
        c = float(input("enter median price: "))
        print(model.predict([[x, b, c, z]]))
