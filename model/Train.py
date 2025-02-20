import math
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, roc_curve, roc_auc_score, accuracy_score
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
    print(model.bias)
    print(model.weights)
    predictions, _ = model.predict(X_test)
    model.plot_confusion_matrix(y_test, predictions)
    print(model.calculate_accuracy(y_test, predictions))
    precision_curve(y_test, predictions)
    plot_roc_curve(y_test, predictions)
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1:.2f}")
    while True:
        x = int(input("enter autcion count: "))
        b = int(input("enter sale count: "))
        z = int(input("enter return count: "))
        c = float(input("enter median price: "))
        print(model.predict([[x, b, c, z]]))
