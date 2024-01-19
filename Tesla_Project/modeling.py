from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

#LDA모델링을 위한 install
#pip install gensim 
#pip install scikit-learn

#기사 수(news_cnt) : X, 주식거래량(stock_volume) : y
def LASSO_KFold(X, y, alpha, n_splits) :
    # MinMaxScaler : 특성들을 (0,1)에 위치하도록 스케일링 (가장 작은 값 : 0, 가장 큰값 : 1)
    # 그래서 분류보단 회귀에 유용

    #X(기사 수)값 스케일링
    scaler_X = MinMaxScaler() 
    # fit : 주어진 데이터로 스케일링을 수행하기 위해 필요한 파라미터 계산 즉, 최소값, 최대값 계산하여 저장 (주어진 데이터를 통해 스케일링에 필요한 파라미터 학습하는 단계)
    # transform : fit의 계산한 값을 0,1의 값으로 스케일링 함 즉, 학습한 데이터를 사용하여 주어진 데이터를 스케일링하는 단계
    X = scaler_X.fit_transform(X)

    # y값(주식 거래량)값 스케일링
    scaler_y = MinMaxScaler()
    y = scaler_y.fit_transform(y) 

    # 데이터를 훈련 세트와 테스트 세트로 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=55)

    # 라쏘 회귀 모델 생성
    # alpha값은 k-fold를 통해 구함
    lasso_model = Lasso(alpha)

    # K-fold 교차 검증을 사용하여 성능 평가
    # 일반화 성능을 추정하기 위한 검증 세트를 사용 : 주어진 데이터를 여러 개의 폴도로 나누고 
    # 각 폴드에 대해 모델을 훈련하고 평가하는 것으로 데이터를 효과적으로 활용
    # n_splits  : K-fold 분할 수
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    mse_scores = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        lasso_model.fit(X_train, y_train)
        y_pred = lasso_model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        mse_scores.append(mse)

    # 각 fold에서의 MSE 출력
    for i, mse in enumerate(mse_scores):
        print(f"Fold {i + 1} - MSE: {mse}")

    # mse는 1이하로 나오는게 좋음
    # mse = mean_squared_error(y_test, y_pred)
    # print(f"평균 제곱 오차 (MSE): {mse}")

    # R-squared (결정 계수) 계산 :
    # 0 ~ 1사이의 범위를 가짐 1에 가까울수록 선형회귀 모델에 높은 연관성을 가짐
    # 음수는 성능을 안좋게 나타냄
    r2 = r2_score(y, lasso_model.predict(X))

    # 평균 MSE 출력
    mean_mse = sum(mse_scores) / len(mse_scores)
    print(f"평균 MSE : {mean_mse}")
    print(f"R-squared (결정 계수): {r2}")

# 최적의 alpha값 
def optimize_alpha(X, y, alphas, n_splits) :
    #n_splits = 5
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    scaler_X = MinMaxScaler() #0,1분산으로 조정
    # TF-IDF 행렬을 벡터화 배열로 변환 및 2차원 배열로 변경
    X = scaler_X.fit_transform(X)

    # y값(주식 거래량)을 벡터화 배열로 변환 2차원 배열로 변경
    scaler_y = MinMaxScaler()
    y = scaler_y.fit_transform(y)

    best_alpha = None
    best_mean_mse = float('inf')

    for alpha in alphas:
        mse_scores = []
        lasso_model = Lasso(alpha=alpha)

        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            lasso_model.fit(X_train, y_train)
            y_pred = lasso_model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            mse_scores.append(mse)

        mean_mse = np.mean(mse_scores)

        if mean_mse < best_mean_mse:
            best_mean_mse = mean_mse
            best_alpha = alpha

    print(f"최적의 alpha: {best_alpha}")
    print(f"최적의 평균 MSE: {best_mean_mse}")

def LASSO(X, y, n_splits) :
    # 데이터 스케일링
    scaler_X = MinMaxScaler()
    X = scaler_X.fit_transform(X)

    scaler_y = MinMaxScaler()
    y = scaler_y.fit_transform(y.reshape(-1, 1)).flatten()

    # 데이터를 훈련 세트와 테스트 세트로 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=55)

    lasso_model = Lasso()

    # 탐색할 alpha 값의 분포 설정
    param_dist = {'alpha': uniform(0.001, 10)}

    # 랜덤 서치 수행
    # RandomizedSearchCV : 주어진 범위내에서 랜덤한 하이퍼파라미터 조합을 시도하여 k-fold보다 더 다양한 조합 탐색가능
    random_search = RandomizedSearchCV(lasso_model, param_distributions=param_dist, n_iter=5, cv=n_splits)
    random_search.fit(X_train, y_train)

    # 최적의 alpha 값 출력
    print("Best Alpha:", random_search.best_params_['alpha'])