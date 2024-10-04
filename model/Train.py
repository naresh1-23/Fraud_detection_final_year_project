import pandas as pd
from model.LogisticRegression import LogisticRegression


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
    model = LogisticRegression(learning_rate=0.01, num_iterations=1000)
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
    print(model.calculate_accuracy(Y_test, predictions))
    while True:
        x = int(input("Auction Count"))
        y = int(input("Sells count"))
        print(model.predict([[x, y]]))
