import opensim as osim

modelFilename = 'Model/Driving.osim'
actuatorFilename = 'Actuator/Actuators_upper_limb.xml'
settingFile  = 'so.xml'
resultDir = 'Result'
#Subject file list
subjectList = ['SubUnknown']
#External force list
exforceList = [220, 260]
#Motion file list
motList = [30,-30]

model = osim.Model(modelFilename)
model.initSystem()
aTool = osim.AnalyzeTool()

##Set actuator (Optional)
actuatorSet = osim.ArrayStr()
actuatorSet.append(actuatorFilename)
aTool.setForceSetFiles(actuatorSet)

##Set the directory for the result
aTool.setResultsDir(resultDir)

##Set the condition of SO
aSet = aTool.getAnalysisSet()
so = osim.StaticOptimization()
so.setName('StaticOptimization')
aSet.insert(0,so)

for sub in subjectList:
    for mot in motList:
        for exf in exforceList:
            motionFilename = sub + ".mot"
            exforceFilename = sub + "_" + str(mot) + "_" + str(exf) + ".xml"
            outputFilename = sub + "_" + str(mot) + "_" + str(exf)
            
            motData = osim.Storage(motionFilename)

##Get the time of Start and End
            initial_time = motData.getFirstTime()
            final_time = motData.getLastTime()


            aTool.setName(outputFilename)
##Calculation start time
            aTool.setInitialTime(initial_time)
##Calculation finish time
            aTool.setFinalTime(final_time)
##Output precision
            aTool.setOutputPrecision(8)
            aTool.setLowpassCutoffFrequency(6.0)
            aTool.setSolveForEquilibrium(False)
##Set the model
            aTool.setModel(model)
            aTool.setModelFilename(modelFilename)
##Set .mot file
            aTool.setCoordinatesFileName(motionFilename)

##Set external load (Optional)
            aTool.setExternalLoadsFileName(exforceFilename)

			
            so.setStartTime(initial_time)
            so.setEndTime(final_time)

            model.getAnalysisSet().insert(0, so)
            model.updAnalysisSet()

            aTool.printToXML(settingFile)

            tool = osim.AnalyzeTool(settingFile) 
            tool.run()