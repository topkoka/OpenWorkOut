import numpy as np
import pickle
import matplotlib.pyplot as plt
from ReadData import CreateData as cd
from sklearn.linear_model import LogisticRegression as logire
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier as Knn
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier as Ditri

class DecisionTree:
    mz = []
    mx = []
    my = []
    mX = []
    mz_ = []

    def __init__(self, X, z, target_names):

        self.X = X
        self.z = z
        self.mz = self.mz
        self.mx = self.mx
        self.my = self.my
        self.mX = self.mX
        self.target_names = target_names
        self.name = ' Decision Tree '
        self.mz_ = self.mz_
        self.nmesh = 200

        def decisionTree(self):
            try:
                file_model = open('d_t.pkl', 'rb')
                stored_d_t = pickle.load(file_model)
                file_model.close()
            except IOError as e:
                print(e)
            self.mz_ = stored_d_t.predict(self.X)

            self.mx, self.my = np.meshgrid(np.linspace(self.X[:, 0].min(), self.X[:, 0].max(), self.nmesh),
                                           np.linspace(self.X[:, 1].min(), self.X[:, 1].max(), self.nmesh))
            self.mX = np.stack([self.mx.ravel(), self.my.ravel()], 1)
            self.mz = stored_d_t.predict(self.mX).reshape(self.nmesh, self.nmesh)
            show_Data(self.X, self.z, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)

class RandomForest:
    mz = []
    mx = []
    my = []
    mX = []
    mz_ = []

    def __init__(self, X, z, target_names):

        self.X = X
        self.z = z
        self.mz = self.mz
        self.mx = self.mx
        self.my = self.my
        self.mX = self.mX
        self.target_names = target_names
        self.name = 'random forest'
        self.mz_ = self.mz_
        self.nmesh = 200
    def randomforest(self):
        try:
            file_model = open('d_t.pkl', 'rb')
            stored_d_t = pickle.load(file_model)
            file_model.close()
        except IOError as e:
            print(e)
        self.mz_ = stored_d_t.predict(self.X)

        self.mx, self.my = np.meshgrid(np.linspace(self.X[:, 0].min(), self.X[:, 0].max(), self.nmesh),
                                       np.linspace(self.X[:, 1].min(), self.X[:, 1].max(), self.nmesh))
        self.mX = np.stack([self.mx.ravel(), self.my.ravel()], 1)
        self.mz = stored_d_t.predict(self.mX).reshape(self.nmesh, self.nmesh)
        show_Data(self.X, self.z, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)


class Lori:
    mz = []
    mz_ = []

    def __init__(self, X, z, X2, z2, target_names):
        self.X = X
        self.z = z
        self.X2 = X2
        self.z2 = z2
        self.target_names = target_names
        self.name = 'LogisticRegression'
        self.nmesh = 200

    def lori(self):
        lori = logire()
        lori.fit(self.X, self.z)
        self.mz_ = lori.predict(self.X2)

        self.mx, self.my = np.meshgrid(np.linspace(self.X[:, 0].min(), self.X[:, 0].max(), self.nmesh),
                                       np.linspace(self.X[:, 1].min(), self.X[:, 1].max(), self.nmesh))
        self.mX = np.stack([self.mx.ravel(), self.my.ravel()], 1)
        self.mz = lori.predict(self.mX).reshape(self.nmesh, self.nmesh)
        show_Data(self.X, self.z, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)


class Knn_:
    print('knn')
    mz = []
    mz_ = []

    def __init__(self, X, z, target_names):
        self.X = X
        self.z = z
        self.mz = self.mz
        self.target_names = target_names
        self.nmesh = 200
        self.name = 'k-nearest neighbor'
        self.mz_ = self.mz_

    def knn(self):
        try:
            file_model = open('knn.pkl', 'rb')
            stored_knn = pickle.load(file_model)
            file_model.close()
        except IOError as e:
            print(e)

        self.mz_ = stored_knn.predict(self.X)
        self.mx, self.my = np.meshgrid(np.linspace(self.X[:, 0].min(), self.X[:, 0].max(), self.nmesh),
                                       np.linspace(self.X[:, 1].min(), self.X[:, 1].max(), self.nmesh))
        self.mX = np.stack([self.mx.ravel(), self.my.ravel()], 1)
        self.mz = stored_knn.predict(self.mX).reshape(self.nmesh, self.nmesh)
        show_Data(self.X, self.z, self.mx, self.my, self.mz, self.name, self.target_names, self.mz_)


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


def tuni(mz, name):
    print(name)
    x0 = 0
    x1 = 0
    x2 = 0
    x3 = 0
    x4 = 0

    for h in mz:

        for h1 in h:
            if h1 == 0:
                x0 += 1
            elif h1 == 1:
                x1 += 1
            elif h1 == 2:
                x2 += 1
            elif h1 == 3:
                x3 += 1
            elif h1 == 4:
                x4 += 1

    max_h = max(x0, x1, x2, x3, x4)
    print(name, target_names[0], 'x0', x0)
    print(name, target_names[1], 'x1', x1)
    print(name, target_names[2], 'x2', x2)
    print(name, target_names[3], 'x3', x3)
    print(name, target_names[4], 'x4', x4)
    if x0 == max_h:
        print(target_names[0])
    if x1 == max_h:
        print(target_names[1])
    if x2 == max_h:
        print(target_names[2])
    if x3 == max_h:
        print(target_names[3])
    if x4 == max_h:
        print(target_names[4])


squat = cd("dataSet/Squat")
curl = cd("dataSet/Barbell Curl")
pushup = cd('dataSet/Push Ups')
dumbbellShoulderPress = cd('dataSet/Dumbbell Shoulder Press')
deadlift = cd('dataSet/Deadlift')
cam = cd('dataSet/cam')
target_names = np.array(['squat', 'curl', 'pushup', 'dumbbellShoulderPress', 'deadlift'], dtype='<U10')

path = [squat, curl, pushup, dumbbellShoulderPress, deadlift]
idc = 0
nxy, z = cd.allpath(path, idc)
x = cd.xx(nxy)
y = cd.yy(nxy)
z = cd.cen_z(z)
X = np.stack((x, y), axis=1)
z = np.array(z)
X = (X - X.mean(0)) / X.std(0)
X_train, X_test, z_train, z_test = train_test_split(X, z, test_size=0.2)
print('Showdata OK...')
# plt.scatter(X[:, 0], X[:, 1], 50, c=z, edgecolor='k', cmap='rainbow')
# plt.show()

if __name__ == '__main__':
    print(__name__)
    knn = Knn_(X_test, z_test, target_names)
    knn.knn()
    randomforest = RandomForest(X_test, z_test, target_names)
    randomforest.randomforest()
    # lori = Lori(X_train,z_train,X_test,z_test,target_names)
    # lori.lori()
    # tuni(d_tree.mz, 'decision tree')
