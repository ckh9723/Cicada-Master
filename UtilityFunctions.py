import os
import pathlib
import pandas as pd
import numpy as np
from xlrd import XLRDError
from os.path import isfile, join

# Important global variables
dir = str(pathlib.Path(__file__).parent.absolute()) + '\\Models'
single_result = {}

# Universal methods
def getShowHelp(string):
    line_dict = {'Tutorial':-5, 'Classify':-4, 'Create':-3, 'CreateFeatureWarn':-2, 'CreateWarn':-1}
    num = line_dict[string]

    with open('{}\\config.txt'.format(dir)) as f:
        lines = f.readlines()
        if string == 'CreateWarn':
            return lines[num].split(': ')[1]
        else:
            return (lines[num].split(': ')[1])[:-1]

def setConfigNoHelp(string):
    line_dict = {'Tutorial':-5, 'Classify':-4, 'Create':-3, 'CreateFeatureWarn':-2, 'CreateWarn':-1}
    num = line_dict[string]

    with open('{}\\config.txt'.format(dir), 'r') as f:
        lines = f.readlines()

    with open('{}\\config.txt'.format(dir), 'w') as g:
        if string == 'CreateWarn':
            g.writelines(lines[:num])
            g.write(lines[num].split(': ')[0]+': '+'False')
        else:
            g.writelines(lines[:num])
            g.write(lines[num].split(': ')[0]+': '+'False\n')
            g.writelines(lines[num+1:])



# =====================================================================================================================
# Classify screen methods
def getFeatureInfo():
    with open('{}\\config.txt'.format(dir)) as f:
        lines = f.readlines()

    # Get features & feature values
    f = []
    f_vals = {}
    for i in range(3, 3 + int(lines[2].split(': ')[1])):
        index = lines[i].rfind('(')
        feature = lines[i][2:index - 1]
        feature_val = lines[i][index + 1:-2]
        f.append(feature)

        if len(feature_val) != 0:
            feature_val = feature_val.split(',')[:-1]
            f_vals[feature] = feature_val

    return f, f_vals


def checkInput(entry,combobox):
    try:
        input_dict = {}
        for feature in entry:
            input_dict[feature] = float(entry[feature].get())

        for feature in combobox:
            for val in combobox[feature]['values']:
                input_dict[feature+'_'+val] = val if combobox[feature].get() == val else '<#*&=->'  # Intentionally set incorrect value

        return input_dict,1  # Input OK

    except ValueError:
        return [],-1  # Input is incomplete/invalid


def storeSingleResult(single_result_dict):
    global single_result
    single_result = single_result_dict


def exportSingleToExcel(save_path):
    ds = pd.DataFrame(single_result, index=[0])
    ds.to_excel(save_path)


def checkClassifyFile(file_path):
    # Check file type
    try:
        ds = pd.read_excel(file_path)
    except XLRDError:
        return -1  # Invalid format

    # Check feature order & name
    feature_list,feature_vals = getFeatureInfo()
    ds_feature_list = [f for f in ds]
    if len(ds_feature_list) != len(feature_list):
        return -2  # Invalid features
    for i in range(len(feature_list)):
        if ds_feature_list[i] != feature_list[i]:
            return -2

    # Check feature values
    for f in feature_list:
        if f in feature_vals:  # If feature is categorical
            ds_uniq_vals = list(set(ds[f][row] for row in range(len(ds.index))))
            ds_uniq_vals.sort()
            if ds_uniq_vals != feature_vals[f]:
                return -3  # Invalid feature values

        else:  # If feature is numerical
            if (not isinstance(ds[f][0],np.int64)) and not (isinstance(ds[f][0],np.float64)):
                return -3

    return 1  # File is valid


# =====================================================================================================================
# Create Screen methods
def checkCreateFile(file_path):
    # 1. Check file format
    try:
        ds = pd.read_excel(file_path)
    except XLRDError:
        return -1

    # 2. Columns must be at least 2
    cols = ds.columns
    if len(cols) == 1:
        return -2

    # 3. Check missing values & data type consistency
    for col in cols:
        ref_dtype = type(ds[col][0])
        for j in range(len(ds.index)):
            if pd.isna(ds[col][j]) or (type(ds[col][j]) != ref_dtype):
                return -3

    # 4. Check if label is categorical
    for i in range(len(ds.index)):
        if not isinstance(ds[cols[-1]][i],str):
            return -4

    # 5. Must be at least 2 labels
    label_vals = set(ds[cols[-1]][row] for row in range(len(ds.index)))
    if len(label_vals) == 1:
        return -5

    # 6. Check features
    if len(cols) < 4 or len(cols) > 4:
        return 0  # File OK! but different features
    elif len(cols) == 4:
        default_f = ['Echeme Duration','Echeme Period','Inter-Echeme Duration']
        for col in cols[:-1]:
            if (not isinstance(ds[col][0],np.int64)) and (not isinstance(ds[col][0],np.float64)):
                return 0
            if col in default_f:
                default_f.remove(col)
        if len(default_f) > 0:
            return 0

    return 1  # File OK!


def processInputDetails(input_list):
    # Remove '\n' from Description
    input_list[2] = input_list[2][:-1]

    # Remove leading whitespace
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if input_list[i][j] != ' ':
                input_list[i] = input_list[i][j:]
                break

    # Remove trailing whitespace
    for i in range(len(input_list)):
        for j in range(-1, -len(input_list[i]), -1):
            if input_list[i][j] != ' ':
                if j != -1:
                    input_list[i] = input_list[i][:j + 1]
                break

    # Handle 'only whitespace' input
    for i in range(len(input_list)):
        cond = False
        for j in range(len(input_list[i])):
            if input_list[i][j] != ' ':
                cond = True
                break
        if cond is False:
            input_list[i] = ''

    return input_list


def checkName(name):
    folder_path = dir
    config_files = {}
    model_files = {}

    # Search for all config & model files
    files = [f for f in os.listdir(folder_path) if isfile(join(folder_path, f))]
    for f in files:
        if f.split('.')[1] == 'txt':
            config_files[f.split('.')[0]] = 1  # Dummy val
        elif f.split('.')[1] == 'sav':
            model_files[f.split('.')[0]] = 1  # Dummy val

    # Check for model name to prevent duplicate
    for key in config_files:
        if key in model_files:
            if key == name:
                return -1  # Duplicate Name
    return 1  # Name OK!


def getTempDetails():
    with open('{}\\temp.txt'.format(dir)) as f:
        lines = f.readlines()
    acc = (lines[0].split(': ')[1])[:-2]
    n_feature = int((lines[1].split(': ')[1])[:-1])
    n_class = int((lines[2+n_feature].split(': ')[1])[:-1])
    return acc,n_feature,n_class


# ======================================================================================================================
# Manage Screen methods
def getModelDetails(names=False, details=False, edit=False, model_name=''):
    config_files = {}
    model_files = {}

    # Search for all txt & sav files
    files = [f for f in os.listdir(dir) if isfile(join(dir, f))]
    for f in files:
        if f.split('.')[1] == 'txt':
            config_files[f.split('.')[0]] = 1  # Dummy val
        elif f.split('.')[1] == 'sav':
            model_files[f.split('.')[0]] = 1  # Dummy val

    # Get current model name
    with open('{}\\config.txt'.format(dir)) as f:
        current_model_name = (f.readline().split(': ')[1])[:-1]

    # Get list of model names for combobox
    if names is True:
        model_names = []
        for key in config_files:
            if key in model_files:
                model_names.append(key)

        # Assign model-in-use to index 0
        for i in range(len(model_names)):
            if model_names[i] == current_model_name:
                if i!=0:
                    temp = model_names[0]
                    model_names[0] = current_model_name
                    model_names[i] = temp
        return model_names

    # Get model details given model_name
    elif details is True:
        f = open('{}\\{}.txt'.format(dir,model_name), 'r')
        lines = f.readlines()
        f.close()

        # Format accuracy line
        acc = float((lines[2].split(': ')[1])[:-2])*100
        lines[2] = lines[2].split(': ')[0] + ': {:.2f}%\n'.format(acc)

        # Format feature lines
        n_features = int((lines[6].split(': ')[1])[:-1])
        for i in range(7, 7+n_features):
            index = lines[i].rfind('(')

            if lines[i][index+1] == ')':
                lines[i] = lines[i][:index]
                lines[i] += '(numerical)\n'
            else:
                lines[i] = lines[i][:index]
                lines[i] += '(categorical)\n'

        # Format name line if current_model selected
        if model_name == current_model_name:
            if edit is False:
                lines[0] = lines[0].replace('\n', ' (Currently-In-Use)\n')
            return lines, True
        else:
            return lines, False


def updateDetails(input_list, detail_list):
    # If details are changed
    if input_list[0]!=detail_list[0] or input_list[1]!=detail_list[1] or input_list[2]!=detail_list[2]:

        # Check for duplicate name
        check_name = 0
        if input_list[0] != detail_list[0]:
            check_name = checkName(input_list[0])
        if check_name == -1:
            return -1
        else:
            # Get original details
            with open('{}\\{}.txt'.format(dir,detail_list[0]), 'r') as f:
                lines = f.readlines()

            # Update details
            name_head = lines[0].split(': ')[0]
            ds_head = lines[4].split(': ')[0]
            lines[0] = name_head+': '+input_list[0]+'\n'
            lines[4] = ds_head+': '+input_list[1]+'\n'
            lines[-1] = input_list[2]
            with open('{}\\{}.txt'.format(dir, detail_list[0]), 'w') as f:
                f.writelines(lines)

            # Rename file
            os.rename(r'{}\{}.txt'.format(dir,detail_list[0]), r'{}\{}.txt'.format(dir,input_list[0]))
            os.rename(r'{}\{}.sav'.format(dir, detail_list[0]), r'{}\{}.sav'.format(dir, input_list[0]))

            # Check if model is currently-in-use
            with open('{}\\config.txt'.format(dir)) as f:
                current_model_name = (f.readline().split(': ')[1])[:-1]
            if detail_list[0] == current_model_name:
                updateConfig(lines=lines)
            return True
    else:
        return False


def updateConfig(lines):
    with open('{}\\config.txt'.format(dir), 'r') as f:
        # Get showHelp lines
        config_lines = f.readlines()
        showTutorialLine = config_lines[-5]
        showClassifyHelpLine = config_lines[-4]
        showCreateHelpLine = config_lines[-3]
        showCreateFeatureWarnLine = config_lines[-2]
        showCreateWarnLine = config_lines[-1]

    with open('{}\\config.txt'.format(dir), 'w') as g:
        # Write name
        g.write(lines[0] + '\n')

        # Write features
        g.write(lines[6])
        n_features = int((lines[6].split(': ')[1])[:-1])
        for i in range(7, 7 + n_features):
            g.write(lines[i])
        g.write('\n')

        # Write classes
        g.write(lines[8 + n_features])
        n_classes = int((lines[8 + n_features].split(': ')[1])[:-1])
        for i in range(9 + n_features, 9 + n_features + n_classes):
            g.write(lines[i])
        g.write('\n')

        # Write remaining lines
        g.write(showTutorialLine)
        g.write(showClassifyHelpLine)
        g.write(showCreateHelpLine)
        g.write(showCreateFeatureWarnLine)
        g.write(showCreateWarnLine)


def changeModel(model_name):
    # Update config file with new model information
    with open('{}\\{}.txt'.format(dir,model_name), 'r') as f:
        lines = f.readlines()
    updateConfig(lines=lines)


def deleteModel(model_name):
    os.remove('{}\\{}.txt'.format(dir,model_name))
    os.remove('{}\\{}.sav'.format(dir,model_name))

