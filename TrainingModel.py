import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron as Percep
from sklearn.neural_network import MLPClassifier as MLPC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neighbors import KNeighborsClassifier as Knn
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier as Ditri
from sklearn.ensemble import RandomForestClassifier as Rafo
from StackData import DataModel
from StackData import StackData
from sklearn.svm import SVC


class DecisionTree:
    mz = []
    mx = []
    my = []
    mX = []
    mz_ = []

    def __init__(self, X, z, X2, z2, target_names):
        self.X = X
        self.z = z
        self.X2 = X2
        self.z2 = z2
        self.mz = self.mz
        self.mx = self.mx
        self.my = self.my
        self.mX = self.mX
        self.target_names = target_names
        self.name = ' Decision Tree '
        self.mz_ = self.mz_
        self.nmesh = 200
        self.fileName = 'DecisionTree'

    def decisionTree(self):
        ditri = Ditri(max_depth=5)
        ditri.fit(self.X, self.z)

        self.mz_, self.mx, self.my, self.mX, self.mz = predict_Data(self.X2, ditri, self.nmesh)
        show_Data(self.X2, self.z2, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)
        dump_Data(self.fileName, ditri)

class MLPC_:
    mz = []
    mx = []
    my = []
    mX = []
    mz_ = []

    def __init__(self, X, z, X2, z2, target_names):
        self.X = X
        self.z = z
        self.X2 = X2
        self.z2 = z2
        self.mz = self.mz
        self.mx = self.mx
        self.my = self.my
        self.mX = self.mX
        self.target_names = target_names
        self.name = 'Multi-layer Perceptron classifier'
        self.mz_ = self.mz_
        self.nmesh = 200
        self.fileName = 'MLPClassifier'

    def mlpc(self):
        mlpc = MLPC(hidden_layer_sizes=(100,100,100,100,100,100,100,100,100),activation="tanh",learning_rate_init=0.0001
                    ,solver='adam',learning_rate='invscaling',max_iter=500)
        mlpc.fit(self.X, self.z)

        self.mz_, self.mx, self.my, self.mX, self.mz = predict_Data(self.X2, mlpc, self.nmesh)
        show_Data(self.X2, self.z2, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)
        dump_Data(self.fileName, mlpc)

class RandomForest:
    mz = []
    mx = []
    my = []
    mX = []
    mz_ = []

    def __init__(self, X, z, X2, z2, target_names):
        self.X = X
        self.z = z
        self.X2 = X2
        self.z2 = z2
        self.mz = self.mz
        self.mx = self.mx
        self.my = self.my
        self.mX = self.mX
        self.target_names = target_names
        self.name = 'random forest'
        self.mz_ = self.mz_
        self.nmesh = 200
        self.fileName = 'randomforest'

    def randomforest(self):
        rafo = Rafo(n_estimators=100, max_depth=5,n_jobs=-1)
        rafo = rafo.fit(self.X, self.z)
        self.mz_, self.mx, self.my, self.mX, self.mz = predict_Data(self.X2, rafo, self.nmesh)
        show_Data(self.X2, self.z2, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)
        dump_Data(self.fileName, rafo)


class Percep_:
    mz = []
    mx = []
    my = []
    mX = []
    mz_ = []

    def __init__(self, X, z, X2, z2, target_names):
        self.X = X
        self.z = z
        self.X2 = X2
        self.z2 = z2
        self.mz = self.mz
        self.mx = self.mx
        self.my = self.my
        self.mX = self.mX
        self.mz_ = self.mz_
        self.target_names = target_names
        self.name = 'Perceptron'
        self.nmesh = 200
        self.fileName = 'Perceptron'

    def percep(self):
        percep = Percep(n_jobs=-1,max_iter=5000,eta0=0.05)
        percep.fit(self.X, self.z)
        self.mz_, self.mx, self.my, self.mX, self.mz = predict_Data(self.X2, percep, self.nmesh)
        show_Data(self.X2, self.z2, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)
        dump_Data(self.fileName, Percep)


class Knn_:
    mz = []
    mz_ = []

    def __init__(self, X, z, X2, z2, target_names):
        self.X = X
        self.z = z
        self.X2 = X2
        self.z2 = z2
        self.mz = self.mz
        self.target_names = target_names
        self.nmesh = 200
        self.name = 'k-nearest neighbor'
        self.mz_ = self.mz_
        self.fileName = 'Knn'

    def knn(self):
        knn = Knn(n_neighbors=1, p=1, algorithm='kd_tree', n_jobs=-1,leaf_size=45)
        knn = knn.fit(self.X, self.z)
        parameters = {'n_neighbors': range(1, 11)}
        knn_best = GridSearchCV(knn, parameters, cv=5)
        knn_best.fit(self.X, self.z)
        knn_best.best_estimator_

        self.mz_, self.mx, self.my, self.mX, self.mz = predict_Data(self.X2, knn_best, self.nmesh)
        show_Data(self.X2, self.z2, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)
        dump_Data(self.fileName, knn_best)


from sklearn.model_selection import validation_curve


class SVC_:
    mz = []
    mz_ = []

    def __init__(self, X, z, X2, z2, target_names):
        self.X = X
        self.z = z
        self.X2 = X2
        self.z2 = z2
        self.mz = self.mz
        self.target_names = target_names
        self.nmesh = 200
        self.name = 'support vector machine'
        self.mz_ = self.mz_
        self.fileName = 'Svc'

    def svc(self):
        # ccc = 10 ** np.linspace(-5, 5, 41)
        # khanaen_fuek, khanaen_truat = validation_curve(SVC(gamma=1), self.X, self.z, 'C', ccc, cv=5)

        svc = SVC(kernel='rbf', C=10, gamma=10.0)
        svc = svc.fit(self.X, self.z)
        self.mz_, self.mx, self.my, self.mX, self.mz = predict_Data(self.X2, svc, self.nmesh)
        show_Data(self.X2, self.z2, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)
        dump_Data(self.fileName, svc)

        # plt.figure(figsize=[4.5, 6])
        # plt.subplot(211, aspect=1)
        # plt.scatter(self.X2[:, 0], self.X2[:, 1], c=self.z2, edgecolor='k', cmap='rainbow')
        # plt.subplot(212, xscale='log', xlabel='C')
        # plt.plot(ccc, np.mean(khanaen_fuek, 1), color='#992255')
        # plt.plot(ccc, np.mean(khanaen_truat, 1), color='#448965')
        # plt.legend([u'ฝึกฝน', u'ตรวจสอบ'], prop={'family': 'Tahoma'})
        # plt.show()
        # from sklearn.model_selection import validation_curve
        #
        # ccc = 10 ** np.linspace(-5, 5, 41)
        # khanaen_fuek, khanaen_truat = validation_curve(SVC(gamma=1), self.X, self.z, 'C', ccc, cv=5)
        # plt.figure(figsize=[4.5, 6])
        # plt.subplot(211, aspect=1)
        # plt.scatter(self.X[:, 0], self.X[:, 1], c=self.z, edgecolor='k', cmap='rainbow')
        # plt.subplot(212, xscale='log', xlabel='C')
        # plt.plot(ccc, np.mean(khanaen_fuek, 1), color='#992255')
        # plt.plot(ccc, np.mean(khanaen_truat, 1), color='#448965')
        # plt.legend([u'ฝึกฝน', u'ตรวจสอบ'], prop={'family': 'Tahoma'})
        # plt.show()


def dump_Data(fileName, model):
    try:
        f = open('model/'+fileName + '.pkl', 'wb')
        pickle.dump(model, f)
        f.close()
        print('Dump_file OK...')
    except IOError as e:
        print(e)


def predict_Data(X, model, nmesh):
    mz_ = model.predict(X)
    mx, my = np.meshgrid(np.linspace(X[:, 0].min(), X[:, 0].max(), nmesh),
                         np.linspace(X[:, 1].min(), X[:, 1].max(), nmesh))
    mX = np.stack([mx.ravel(), my.ravel()], 1)
    mz = model.predict(mX).reshape(nmesh, nmesh)
    return mz_, mx, my, mX, mz


def show_Data(X, z, mx, my, mz, name, target_names, mz_):
    print('#' * 25 + name + '#' * 25)
    print(classification_report(z, mz_, target_names=target_names))
    print('accuracy_score = ', accuracy_score(z, mz_))
    print('#' * 60)
    plt.figure().gca(aspect=1, xlim=[mx.min(), mx.max()], ylim=[my.min(), my.max()])
    plt.scatter(X[:, 0], X[:, 1], alpha=0.6, c=z, edgecolor='k', cmap='rainbow')
    plt.title(name)
    plt.contourf(mx, my, mz, alpha=0.4, cmap='rainbow', zorder=0)
    plt.show()


def data():
    try:

        dataModel = DataModel()
        squat = dataModel.getSquat()
        curl = dataModel.getCurl()
        pushup = dataModel.getPushup()
        dumbbellShoulderPress = dataModel.getDumbbellShoulderPress()
        deadlift = dataModel.getDeadlift()
        cam = dataModel.getCam()
        unknown = dataModel.getUnknown()
        target_names = dataModel.getTargetNames()
        # target_names = np.array(['squat','unknown'], dtype='<U10')
        path = [squat, curl, pushup, dumbbellShoulderPress, deadlift]
        sd = StackData(path)
        X_train, X_test, z_train, z_test = sd.stackData_Train()
        print('DataSet OK...')
        # plt.scatter(X[:, 0], X[:, 1], 50, c=z, edgecolor='k', cmap='rainbow')
        # plt.show()
    except Exception as e:
        print(e)

    return X_train, X_test, z_train, z_test, target_names


def training_knn():
    print('Training_knn Start..')
    X_train, X_test, z_train, z_test, target_names = data()
    knn = Knn_(X_train, z_train, X_test, z_test, target_names)
    knn.knn()
    print('Training_knn Finish..')


def training_DecisionTree():
    print('training_DecisionTree Start..')
    X_train, X_test, z_train, z_test, target_names = data()
    dt = DecisionTree(X_train, z_train, X_test, z_test, target_names)
    dt.decisionTree()
    print('training_DecisionTree Finish..')


def training_RandomForest():
    print('training_RandomForest Start..')
    X_train, X_test, z_train, z_test, target_names = data()
    randomforest = RandomForest(X_train, z_train, X_test, z_test, target_names)
    randomforest.randomforest()
    print('training_RandomForest Finish..')


def training_percep():
    print('training_percep Start..')
    X_train, X_test, z_train, z_test, target_names = data()
    percep = Percep_(X_train, z_train, X_test, z_test, target_names)
    percep.percep()
    print('training_percep Finish..')

def training_mlpc():
    print('training_MLPC_Start..')
    X_train, X_test, z_train, z_test, target_names = data()
    mlpc = MLPC_(X_train, z_train, X_test, z_test, target_names)
    mlpc.mlpc()
    print('training_MLPC_ Finish..')


def training_Svc():
    print('training_Svc Start..')
    X_train, X_test, z_train, z_test, target_names = data()
    svc = SVC_(X_train, z_train, X_test, z_test, target_names)
    svc.svc()
    print('training_Svc Finish..')


# if __name__ == '__main__':
#     training_DecisionTree()
#     training_knn()
#     training_percep()
#     training_mlpc()
#     training_RandomForest()
#     training_Svc()
