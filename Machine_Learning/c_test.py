import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import warnings
warnings.filterwarnings("ignore")
from sklearn import metrics
from pylab import rcParams
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.tree import DecisionTreeClassifier

# 讀取 CSV 檔案
file_path = './product_overview_selected_medinev2.csv'
df = pd.read_csv(file_path)


# Data to plot
sizes = df['sale_grades'].value_counts(sort = True)
colors = ["blue","red"] 
rcParams['figure.figsize'] = 5,5
# Plot
plt.pie(sizes, explode=[0.1, 0.1], labels=["0", "1"], colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=270,)
plt.title('Percentage of sale_grades in Dataset')
plt.show()

# df.drop(['date_time'], axis=1, inplace=True) 
df['each_buyer_sales'] = pd.to_numeric(df['each_buyer_sales'],errors='coerce')

df=df.apply(LabelEncoder().fit_transform)   #apply LabelEncoder to all Categorical column
print(df)

df["sale_grades"] = df["sale_grades"].astype(int)
Y = df["sale_grades"].values
X = df.drop(labels = ["sale_grades"],axis = 1)

# Create Train & Test Data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=101)

Names=[
    # "Logistic Regression", 
    # "Decision Tree",
    # "Gaussian Naive Bayes",
    # "Linear Discriminant",
    # "Quadratic Discriminant",
    # "K Nearest Neighbors",
    "Support Vector Machine"
]

Models=[
    # LogisticRegression(solver = 'newton-cg'),
    # DecisionTreeClassifier(max_depth = 4, random_state = 1),
    # GaussianNB(),
    # LinearDiscriminantAnalysis(),
    # QuadraticDiscriminantAnalysis(),
    # KNeighborsClassifier(),
    SVC(kernel='linear')
]

for name, model in zip(Names, Models):
    result = model.fit(X_train, y_train)
    prediction_test = model.predict(X_test)
    # Print the prediction accuracy
    print(f"Accuracy of {name} is: {metrics.accuracy_score(y_test, prediction_test):2.2f}")
    print(metrics.classification_report(y_test, prediction_test))

    # To get the weights of all the variables
    weights = pd.Series(model.coef_[0], index=X.columns.values)
    print(weights.sort_values(ascending = False))

    predictions = result.predict(X_test)
    cm = confusion_matrix(y_test, predictions, labels=result.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=result.classes_)
    disp.plot()
    plt.show()

    scores = cross_val_score(model, X, Y, cv=10)
    print(scores)
    print(scores.mean())