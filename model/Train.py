import pandas as pd
from model.LogisticRegression import LogisticRegression
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.metrics import accuracy_score


def change_bool_to_number(row):
    if row["is_fraud"]:
        return 1
    else:
        return 0


def clean_csv(df):
    df["SellerAuctionCount"].fillna(df["SellerAuctionCount"].mean())
    df["SellerAuctionSaleCount"].fillna(df["SellerAuctionSaleCount"].mean())
    df["is_fraud"] = df.apply(change_bool_to_number, axis=1)
    return df


def main():
    df = pd.read_csv('data/train_dataset.csv')
    df = clean_csv(df)
    breakpoint()
    model = LogisticRegression()
    X_train = df[["SellerAuctionCount", "SellerAuctionSaleCount"]].values
    Y_train = df["is_fraud"].values
    model.fit(X_train, Y_train)
    model.plot_loss()
    # # print(model.bias)
    # # print(model.weights)
    test_data = pd.read_csv('data/test_dataset.csv')
    test_data = clean_csv(test_data)
    X_test = test_data[["SellerAuctionCount", "SellerAuctionSaleCount"]].values
    # # print(X_test)
    Y_test = test_data["is_fraud"].values
    predictions = model.predict(X_test)
    model.plot_confusion_matrix(Y_test, predictions)
    # print(model.calculate_accuracy(Y_test, predictions))
    # while True:
    #     x = int(input("Auction Count"))
    #     y = int(input("Sells count"))
    #     print(model.predict([[x, y]]))
    # model = SklearnLogisticRegression(max_iter=1000)

    # # Train the model
    # model.fit(X_train, Y_train)
    # # Make predictions on the test data
    # predictions = model.predict(X_test)

    # # Calculate accuracy
    # accuracy = accuracy_score(Y_test, predictions)
    # print("Test Accuracy:", accuracy)
    # print(model.predict([[120, 100]]))
    # print(model.predict([[120, 50]]))
    # print(model.predict([[120, 10]]))
