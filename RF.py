import os
import pickle
import pathlib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold


# Initialize global variables
dir = str(pathlib.Path(__file__).parent.absolute()) + '\\Models'

feature_list = []
with open('{}\\config.txt'.format(dir)) as g:
    lines = g.readlines()
for i in range(3, 3 + int(lines[2].split(': ')[1])):
    index = lines[i].rfind('(')-1
    feature_list.append(lines[i][2:index])


def get_param_range(param,step,features,labels):
    # Prepare stratified 5-fold CV
    skf = StratifiedKFold(n_splits=5)
    cv_dataset = [(features[train_i], labels[train_i], features[test_i], labels[test_i]) for train_i, test_i in skf.split(features,labels)]

    # Important variables
    param_val = 0
    param_list = []
    cur_max_acc = 0
    plateau_count = 0

    # Increment param by step every loop
    while True:
        final_acc = 0
        param_val += step

        # 5-fold CV
        for cur_fold in cv_dataset:
            feature_x = cur_fold[0]
            label_x = cur_fold[1]
            feature_y = cur_fold[2]
            label_y = cur_fold[3]

            # Train model
            rf = RandomForestClassifier()
            rf.set_params(**{param:param_val})
            rf.fit(feature_x, label_x)
            predictions = (rf.predict(feature_y) == label_y)

            # Get current-fold accuracy & update CV accuracy
            correct_predictions = np.delete(predictions, np.where(predictions == False))
            acc = len(correct_predictions) / len(predictions)
            final_acc += acc
        final_acc /= 5

        # Check for accuracy gain plateau
        if final_acc - cur_max_acc < 0.01:  # If acc gain less than 1%
            plateau_count += 1
            param_list.append(param_val)
        else:
            plateau_count = 0
            param_list.clear()

        # Update current max accuracy
        if final_acc > cur_max_acc:
            cur_max_acc = final_acc

        # Check for terminating condition
        if plateau_count == 5:
            break

    return param_list


def createModel(file_path):
    # Load & shuffle dataset
    ds = pd.read_excel(file_path)
    ds_shuffled = ds.sample(frac=1).reset_index(drop=True)

    # Get features & labels
    labels = np.array(ds_shuffled[ds_shuffled.columns[-1]])
    features = ds_shuffled.drop(ds_shuffled.columns[-1], axis=1)
    model_f = [f for f in features]
    features = np.array(pd.get_dummies(features))

    # Stratified 5-fold Outer CV
    skf = StratifiedKFold(n_splits=5)
    cv_dataset = [(features[train_i], labels[train_i], features[test_i], labels[test_i]) for train_i, test_i in skf.split(features,labels)]

    # Perform Nested CV
    count = 0
    final_acc = 0
    max_features = np.arange(1, features.shape[1] + 1, 1) if features.shape[1] <= 5 else [0.2, 0.4, 0.6, 0.8, 1.0,'sqrt','log2']

    for cur_fold in cv_dataset:
        count+=1
        # Train & Test data for current fold
        feature_x = cur_fold[0]
        label_x = cur_fold[1]
        feature_y = cur_fold[2]
        label_y = cur_fold[3]

        # Hyperparameter Tuning
        param_grid = {
            'n_estimators': get_param_range('n_estimators', 20, feature_x, label_x),
            # 'max_features': max_features,
            # 'max_depth': get_param_range('max_depth', 20, feature_x, label_x) + [None]
        }
        grid_search = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_grid, cv=5, n_jobs=-1, verbose=0)
        grid_search.fit(feature_x, label_x)

        # Calculate accuracy
        best_model = grid_search.best_estimator_
        predictions = best_model.predict(feature_y) == label_y
        correct_predictions = np.delete(predictions, np.where(predictions == False))
        acc = len(correct_predictions)/len(predictions)
        final_acc += acc

    final_acc /= 5  # Final model accuracy


    # Train on full dataset
    final_param_grid = {
        'n_estimators': get_param_range('n_estimators', 20, features, labels),
        # 'max_features': max_features,
        # 'max_depth': get_param_range('max_depth', 20, features, labels) + [None]
    }
    grid_search = GridSearchCV(estimator=RandomForestClassifier(), param_grid=final_param_grid, cv=5, n_jobs=-1, verbose=0)
    grid_search.fit(features, labels)
    final_rf = grid_search.best_estimator_

    # Get unique values for categorical features
    uniq_vals = {feature:None for feature in model_f}
    for feature in model_f:
        if isinstance(ds[feature][0],str):
            uniq_vals[feature] = list(set([ds[feature][row] for row in range(len(ds[feature].index))]))
            uniq_vals[feature].sort()

    # Create temporary model files
    saveModel(model=final_rf, model_f=model_f, model_f_vals=uniq_vals, model_acc=final_acc)

    # Return n_feature & n_class
    return len(model_f), len(final_rf.classes_)


def saveModel(model=None, model_f=None, model_f_vals=None, model_acc=None, name='', dataset='', description=''):
    # Create temporary model & description file
    if model is not None:
        pickle.dump(model, open('{}\\temp.sav'.format(dir), 'wb'))

        with open('{}\\temp.txt'.format(dir), 'w') as f:
            # Write model accuracy
            f.write('Estimated Accuracy: {}\n'.format(model_acc))

            # Write feature & unique vals if any
            f.write('Features: {}\n'.format(len(model_f)))
            for feature in model_f:
                f.write('- {}'.format(feature))
                if model_f_vals[feature] is None:
                    f.write(' ()\n')
                else:
                    f.write(' (')
                    for val in model_f_vals[feature]:
                        f.write('{},'.format(val))
                    f.write(')\n')

            # Write classes
            f.write('Classes: {}\n'.format(len(model.classes_)))
            for c in model.classes_:
                f.write('- {}\n'.format(c))

    # Create model & description file
    if name != '':
        # Get details from temp description file
        with open('{}\\temp.txt'.format(dir), 'r') as f:
            lines = f.readlines()
            row_f = 1
            n_features = int((lines[1].split(': ')[1])[:-1])
            row_c = int(row_f + n_features + 1)
            n_classes = int((lines[row_c].split(': ')[1])[:-1])

            model_acc = (lines[0].split(': ')[1])[:-1]
            model_f = [(lines[i])[2:-1] for i in range(row_f+1, row_f+1+n_features)]
            model_c = [(lines[i])[2:-1] for i in range(row_c+1, row_c+1+n_classes)]

        # Update temp file & rename
        with open('{}\\temp.txt'.format(dir), 'w') as g:
            g.write('Model Name: {}\n\n'.format(name))
            g.write('Estimated Accuracy: {}\n\n'.format(model_acc))
            g.write('Dataset: {}\n\n'.format(dataset))

            g.write('Features: {}\n'.format(len(model_f)))
            for feature in model_f:
                g.write('- {}\n'.format(feature))
            g.write('\n')

            g.write('Classes: {}\n'.format(len(model_c)))
            for c in model_c:
                g.write('- {}\n'.format(c))
            g.write('\n')

            g.write('Description: \n{}'.format(description))

        os.rename(r'{}\temp.sav'.format(dir), r'{}\{}.sav'.format(dir,name))
        os.rename(r'{}\temp.txt'.format(dir), r'{}\{}.txt'.format(dir,name))


def classifySingle(input_dict):
    # Transform feature values into dataframe
    # Transform categorical value into 0 & 1
    for feature in input_dict:
        if '_' in feature:
            try:
                input_dict[feature] = float(input_dict[feature])
            except ValueError:
                input_dict[feature] = 1 if input_dict[feature] == feature[feature.rfind('_')+1:] else 0
    ds = pd.DataFrame(input_dict, index=[0])

    # Get current model
    with open('{}\\config.txt'.format(dir)) as f:
        current_model_name = (f.readline().split(': ')[1])[:-1]
    model = pickle.load(open('{}\\{}.sav'.format(dir,current_model_name), 'rb'))

    # Perform classification & format results to return
    results = model.predict_proba(ds)
    class_list = model.classes_
    result_dict = {}
    for i in range(len(class_list)):
        result_dict[class_list[i]] = results[0][i]
    result_dict = {c: p for c, p in sorted(result_dict.items(), key=lambda item: item[1], reverse=True)}

    single_result = {**input_dict, **result_dict}
    return result_dict, single_result


def classify(file_path, save_path):
    # Load dataset & get file name
    ds = pd.read_excel(file_path)

    # Get current model
    with open('{}\\config.txt'.format(dir)) as f:
        current_model_name = (f.readline().split(': ')[1])[:-1]
    model = pickle.load(open('{}\\{}.sav'.format(dir,current_model_name), 'rb'))

    # Perform classification & format results to return
    results = model.predict_proba(ds)
    class_list = model.classes_

    results_dict = {c:[] for c in class_list}
    for result in results:
        for i in range(len(class_list)):
            results_dict[class_list[i]].append(round(result[i],3))

    # Export results to Excel file
    results_ds = pd.DataFrame(results_dict)
    final_ds = pd.concat([ds, results_ds], axis=1)
    final_ds.to_excel(save_path)
