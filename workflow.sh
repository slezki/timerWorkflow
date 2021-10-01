#! /bin/bash

#chmod a+x workflow.sh
#./workflow.sh ${number of events} ${number of threads} ${event resolution for ThroughputService}

nEvt=$1  	#${number of events}
nThread=$2  #${number of threads}
evtRes=$3   #${event resolution for ThroughputService}

rm step3_RAW2DIGI_RECO.py

echo "  "
echo " ########### cmsDriver is running ########### "
echo "  "
cmsDriver.py step3 \
	--mc \
	--conditions auto:phase2_realistic_T15 \
	-s RAW2DIGI,RECO:reconstruction_trackingOnly \
	--datatier GEN-SIM-RECO,DQMIO \
	-n $nEvt \
	--geometry Extended2026D49 \
	--era Phase2C9 \
	--eventcontent RECOSIM,DQM \
	--filein file:step2.root \
	--fileout file:step3.root \
	--python_filename step3_RAW2DIGI_RECO.py \
	--no_exec

sed -i "/.*FrontierConditions\_GlobalTag.*/a process.MessageLogger.categories.append('FastReport')\nprocess.MessageLogger.cerr.FastReport = cms.untracked.PSet( limit = cms.untracked.int32( 10000000 ) )" step3_RAW2DIGI_RECO.py
sed -i "/.*Input\ source.*/i from inputFiles import pu50" step3_RAW2DIGI_RECO.py
sed -i "s/'file\:step2\.root'/pu50/g" step3_RAW2DIGI_RECO.py

sed -i "/.*cms.EndPath(process.DQMoutput).*/a process.consumer = cms.EDAnalyzer(\"GenericConsumer\", \n\teventProducts = cms.untracked.vstring('generalTracks')\n)\nprocess.consume_step = cms.EndPath(process.consumer)" step3_RAW2DIGI_RECO.py
sed -i "s/,process.reconstruction_step/,process.reconstruction_step,process.consume_step/g" step3_RAW2DIGI_RECO.py

sed -i "s/numberOfThreads = cms.untracked.uint32(1),/numberOfThreads = cms.untracked.uint32($nThread),/g" step3_RAW2DIGI_RECO.py

cat >> step3_RAW2DIGI_RECO.py << EOF

# remove any instance of the FastTimerService
if 'FastTimerService' in process.__dict__:
    del process.FastTimerService

# instrument the menu with the FastTimerService
process.load( "HLTrigger.Timer.FastTimerService_cfi" )

process.FastTimerService = cms.Service( "FastTimerService",
    printEventSummary = cms.untracked.bool( False ),
    printRunSummary = cms.untracked.bool( False ),
    printJobSummary = cms.untracked.bool( True ),
    writeJSONSummary = cms.untracked.bool( True ),
    jsonFileName = cms.untracked.string( "cpu.json" ),
    enableDQM = cms.untracked.bool( True ),
    enableDQMbyModule = cms.untracked.bool( True ),
    enableDQMbyPath = cms.untracked.bool( True ),
    enableDQMbyLumiSection = cms.untracked.bool( True ),
    enableDQMbyProcesses = cms.untracked.bool( True ),
    enableDQMTransitions = cms.untracked.bool( False ),
    dqmTimeRange = cms.untracked.double( 1000.0 ),
    dqmTimeResolution = cms.untracked.double( 5.0 ),
    dqmMemoryRange = cms.untracked.double( 1000000.0 ),
    dqmMemoryResolution = cms.untracked.double( 5000.0 ),
    dqmPathTimeRange = cms.untracked.double( 100.0 ),
    dqmPathTimeResolution = cms.untracked.double( 0.5 ),
    dqmPathMemoryRange = cms.untracked.double( 1000000.0 ),
    dqmPathMemoryResolution = cms.untracked.double( 5000.0 ),
    dqmModuleTimeRange = cms.untracked.double( 40.0 ),
    dqmModuleTimeResolution = cms.untracked.double( 0.2 ),
    dqmModuleMemoryRange = cms.untracked.double( 100000.0 ),
    dqmModuleMemoryResolution = cms.untracked.double( 500.0 ),
    dqmLumiSectionsRange = cms.untracked.uint32( 2500 ),
    dqmPath = cms.untracked.string( "HLT/TimerService" ),
)

# add ThroughputService
process.ThroughputService = cms.Service('ThroughputService',
    eventRange = cms.untracked.uint32(1000),
    eventResolution = cms.untracked.uint32($evtRes),
    printEventSummary = cms.untracked.bool(True),
    enableDQM = cms.untracked.bool(True),
    dqmPathByProcesses = cms.untracked.bool(False),
    dqmPath = cms.untracked.string('HLT/Throughput'),
    timeRange = cms.untracked.double(1000),
    timeResolution = cms.untracked.double(1)
)

process.MessageLogger.categories.append('ThroughputService')
process.MessageLogger.cerr.ThroughputService = cms.untracked.PSet(
    limit = cms.untracked.int32(10000000)
)

EOF

rm fastTimerService_Harvester_cfg.py

cat >> fastTimerService_Harvester_cfg.py <<timerCfg
import FWCore.ParameterSet.Config as cms

process = cms.Process('HARVESTING')

# read all the DQMIO files produced by the previous jobs
process.source = cms.Source("DQMRootSource",
    fileNames = cms.untracked.vstring(
        "file:step3_inDQM.root",
    )
)

# DQMStore service
process.load('DQMServices.Core.DQMStore_cfi')
process.DQMStore.enableMultiThread = True

# FastTimerService client
process.load('HLTrigger.Timer.fastTimerServiceClient_cfi')
process.fastTimerServiceClient.dqmPath = "HLT/TimerService"

process.throughputServiceClient = cms.EDProducer('ThroughputServiceClient',
  dqmPath = cms.untracked.string('HLT/Throughput'),
  createSummary = cms.untracked.bool(True),
  mightGet = cms.optional.untracked.vstring
)

# DQM file saver
process.load('DQMServices.Components.DQMFileSaver_cfi')
process.dqmSaver.workflow = "/HLT/FastTimerService/All"

process.DQMFileSaverOutput = cms.EndPath( process.fastTimerServiceClient + process.throughputServiceClient + process.dqmSaver )
timerCfg

rm run.log
echo "  "
echo " ########### running samples ########### "
echo "  "
cmsRun step3_RAW2DIGI_RECO.py &> run.log

echo "  "
echo " ########### running timer harvester ########### "
echo "  "
cmsRun fastTimerService_Harvester_cfg.py

# create plots directory
mkdir -p plots
echo "  "
echo " ########### plotting is started ########### "
echo "  "
python timePlot.py
