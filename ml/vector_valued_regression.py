import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

from IPython import embed

def get_y(X, noise=True):
    n_samples = X.shape[0]
    y1 = X[:, 0] + 2 * X[:, 1] + 3 * X[:, 2]
    y2 = -X[:, 0] + 0.5 * X[:, 1] -0.1 * X[:, 2]
    if noise:
        y1 += np.random.normal(size=(n_samples, ))
        y2 += np.random.normal(size=(n_samples, ))

    Y = np.vstack((y1, y2)).T
    return Y

def evaluate(regressor, X, Y):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    regressor.fit_optim(X_train, Y_train)
    Y_pred = regressor.predict(X_test)
    Y_mean = Y_train.mean(axis=0)    
    mse = np.sum((Y_pred - Y_test) ** 2)
    mse_mean = np.sum((Y_test - Y_mean) ** 2)
    return mse, mse_mean

def main():
    n_samples = 1000
    x1 = np.linspace(0, 10, n_samples)
    X = np.vstack((x1, 0.5 * x1, 0.25 * x1)).T
    X += np.random.normal(size=X.shape)
    Y = get_y(X, noise=True)

    knn = KNeighborsRegressor(n_neighbors=5)
    gpr = GaussianProcessRegressor()
    svr = SVR()
    mse, mse_mean = evaluate(svr, X, Y)
    print(mse, mse_mean)
if __name__ == '__main__':
    main()
