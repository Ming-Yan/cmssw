###############################################################################
# Way to use this:
#   cmsRun testHitRelabeller_cfg.py geometry=2021
#
#   Options for geometry 2016, 2017, 2018, 2021, 2023
#
###############################################################################
import FWCore.ParameterSet.Config as cms
import os, sys, imp, re
import FWCore.ParameterSet.VarParsing as VarParsing

####################################################################
### SETUP OPTIONS
options = VarParsing.VarParsing('standard')
options.register('geometry',
                 "2021",
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "geometry of operations: 2016, 2017, 2018, 2021, 2023")

### get and parse the command line arguments
options.parseArguments()

print(options)

####################################################################
# Use the options

geomName = "Configuration.Geometry.GeometryExtended" + options.geometry + "Reco_cff"

if (options.geometry == "2016"):
    from Configuration.Eras.Era_Run2_2016_cff import Run2_2016
    process = cms.Process('HitRelabeller',Run2_2016)
    baseName = "auto:run2_data"
elif (options.geometry == "2017"):
    from Configuration.Eras.Era_Run2_2017_cff import Run2_2017
    process = cms.Process('HitRelabeller',Run2_2017)
    baseName = "auto:run2_data"
elif (options.geometry == "2018"):
    from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
    process = cms.Process('HitRelabeller',Run2_2018)
    baseName = "auto:run2_data"
else:
    from Configuration.Eras.Era_Run3_DDD_cff import Run3_DDD
    process = cms.Process('HitRelabeller',Run3_DDD)
    baseName = "auto:run3_data"

print("Base file Name: ", baseName)
print("Geom file Name: ", geomName)


# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13p6TeVEarly2022Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load(geomName)

if hasattr(process,'MessageLogger'):
    process.MessageLogger.HCalGeom=dict()

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(

        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(1)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(1),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('ZMM_14TeV_TuneCP5_cfi nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag 
process.GlobalTag = GlobalTag(process.GlobalTag, baseName, '')

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
                                 pythiaHepMCVerbosity = cms.untracked.bool(False),
                                 maxEventsToPrint = cms.untracked.int32(0),
                                 pythiaPylistVerbosity = cms.untracked.int32(0),
                                 filterEfficiency = cms.untracked.double(1.0),
                                 comEnergy = cms.double(14000.0),
                                 PythiaParameters = cms.PSet(
                                     pythia8CommonSettings = cms.vstring(
                                         'Tune:preferLHAPDF = 2',
                                         'Main:timesAllowErrors = 10000',
                                         'Check:epTolErr = 0.01',
                                         'Beams:setProductionScalesFromLHEF = off',
                                         'SLHA:minMassSM = 1000.',
                                         'ParticleDecays:limitTau0 = on',
                                         'ParticleDecays:tau0Max = 10',
                                        'ParticleDecays:allowPhotonRadiation = on',
                                     ),
                                     pythia8CP5Settings = cms.vstring(
                                         'Tune:pp 14',
                                         'Tune:ee 7',
                                         'MultipartonInteractions:ecmPow=0.03344',
                                         'MultipartonInteractions:bProfile=2',
                                         'MultipartonInteractions:pT0Ref=1.41',
                                         'MultipartonInteractions:coreRadius=0.7634',
                                         'MultipartonInteractions:coreFraction=0.63',
                                         'ColourReconnection:range=5.176',
                                         'SigmaTotal:zeroAXB=off',
                                         'SpaceShower:alphaSorder=2',
                                         'SpaceShower:alphaSvalue=0.118',
                                         'SigmaProcess:alphaSvalue=0.118',
                                         'SigmaProcess:alphaSorder=2',
                                         'MultipartonInteractions:alphaSvalue=0.118',
                                         'MultipartonInteractions:alphaSorder=2',
                                         'TimeShower:alphaSorder=2',
                                         'TimeShower:alphaSvalue=0.118',
                                         'SigmaTotal:mode = 0',
                                         'SigmaTotal:sigmaEl = 21.89',
                                         'SigmaTotal:sigmaTot = 100.309',
                                         'PDF:pSet=LHAPDF6:NNPDF31_nnlo_as_0118',
                                     ),
                                     processParameters = cms.vstring(
                                         'WeakSingleBoson:ffbar2gmZ = on',
                                         '23:onMode = off',
                                         '23:onIfAny = 13',
                                         'PhaseSpace:mHatMin = 75.',
                                     ),
                                     parameterSets = cms.vstring('pythia8CommonSettings',
                                                                 'pythia8CP5Settings',
                                                                 'processParameters',
                                                             )
                                 )
)

process.mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    MaxEta = cms.untracked.vdouble(4.0, 4.0),
    MinEta = cms.untracked.vdouble(-4.0, -4.0),
    MinPt = cms.untracked.vdouble(2.5, 2.5),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13),
    Status = cms.untracked.vint32(1, 1)
)


process.ProductionFilterSequence = cms.Sequence(process.generator+process.mumugenfilter)
process.load("Geometry.HcalCommonData.hcalHitRelabellerTester_cfi")

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.analysis_step = cms.EndPath(process.hcalHitRelabellerTester)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,
                                process.genfiltersummary_step,
                                process.simulation_step,
                                process.endjob_step,
                                process.analysis_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path).insert(0, process.ProductionFilterSequence)


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
