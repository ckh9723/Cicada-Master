# Self-defined modules
import RF as rf
import UtilityFunctions as uf


# Universal methods
def getShowHelp(string):
    return uf.getShowHelp(string)

def setConfigNoHelp(string):
    uf.setConfigNoHelp(string)


# Classify Screen methods
def getFeatureInfo():
    return uf.getFeatureInfo()

def checkInput(entry,combobox):
    return uf.checkInput(entry,combobox)

def classifySingle(input_dict):
    result_dict,single_result = rf.classifySingle(input_dict)
    uf.storeSingleResult(single_result)
    return result_dict

def exportSingleToExcel(save_path):
    uf.exportSingleToExcel(save_path)

def checkClassifyFile(file_path):
    return uf.checkClassifyFile(file_path)

def classify(file_path, save_path):
    rf.classify(file_path,save_path)


# Create screen methods
def checkCreateFile(file_path):
    return uf.checkCreateFile(file_path)

def processInputDetails(input_list):
    return uf.processInputDetails(input_list)

def checkName(name):
    return uf.checkName(name)

def createModel(file_path):
    rf.createModel(file_path)

def getTempDetails():
    return uf.getTempDetails()

def saveModel(name,dataset,description):
    rf.saveModel(name=name,dataset=dataset,description=description)


# Manage screen methods
def getModelDetails(names=False, details=False, edit=False, model_name=''):
    return uf.getModelDetails(names=names,details=details,edit=edit,model_name=model_name)

def updateDetails(input_list, detail_list):
    return uf.updateDetails(input_list,detail_list)

def changeModel(model_name):
    uf.changeModel(model_name)

def deleteModel(model_name):
    uf.deleteModel(model_name)
