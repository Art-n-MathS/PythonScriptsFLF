
Rem Define variable 

Rem Directory of python scripts
set pyDir="C:/Users/mm2705/Documents/Cambridge/Scripts/PythonScriptsFLF/"
set pyDir=%pyDir:"=%
Rem Directory of field data - L0 should be a folder containing the original data 
set fpDir="C:/Users/mm2705/Documents/Cambridge/Milto_SPSW/"
set fpDir=%fpDir:"=%

Rem ------------------------------------------------------------------------------
Rem change to directory with field data 
cd %fpDir%
Rem checks if data processed before exists and deletes them
Rem L1 data contains plot data that only "." is used for decimal numbers
Rem and "," is used as a deliminator in the .csv files
if exist L1 (
   del /s /q L1
   rmdir L1 /s /q
   echo L1
) else (
  Rem L1 folder not created - no need to delete it
)
Rem create a new empty folder named L1
mkdir L1
Rem Change to directory with python scripts
cd %pyDir%
Rem Change all plots at both tree and plot level so that decimal points are 
Rem represented with "." and the delimination in the .csv files is ","
python FixCSVs.py -in %fpDir%L0/ -out %fpDir%L1/
Rem ------------------------------------------------------------------------------


Rem ------------------------------------------------------------------------------
Rem change to directory with field data 
cd %fpDir%
Rem L2 data contains plot data at field level only unwrapped
if exist L2 (
   del /s /q L2
   rmdir L2 /s /q
   echo L2
) else (
  Rem L2 folder not created - no need to delete it
)
Rem create a new empty folder named L1
mkdir L2
Rem Change to directory with python scripts
cd %pyDir%
Rem Method that unwraps field plots, so that I can search plots by year
python unwrap.py -in %fpDir%L1/ -out %fpDir%L2
Rem ------------------------------------------------------------------------------


Rem ------------------------------------------------------------------------------
Rem use the FielData_test as an example of how to extract feature vectors from 
Rem sattelite images of interest

Rem ------------------------------------------------------------------------------
Rem use the Masks_test as an example of how to export a combined mask of interest

Rem ------------------------------------------------------------------------------
Rem download makes and feature vectors exported to google drive

set dataDir="C:/Users/mm2705/Documents/Cambridge/Scripts/SampleData/"
set idColName="index"


Rem ------------------------------------------------------------------------------
Rem Method that takes as input the exported field data from the GEE script and 
Rem reduce them to have the mean and std of each plot
Rem ------------------------------------------------------------------------------
python reduceCSVgetStats.py -icsv %dataDir%TestIndClassSentinel2c.csv.csv -indexCoName %idColName% -ocsv %dataDir%TestIndClassSentinel2b_reduced_c.csv


Rem ------------------------------------------------------------------------------
Rem Method that takes the reduced data and 
Rem 
Rem ------------------------------------------------------------------------------
python mergeCSVsBasedOnID.py -icsv1 %dataDir%TestIndClassSentinel2b_reduced_c.csv -icsv2 %dataDir%fieldDatawithIds.csv -label "index" -ocsv  %dataDir%mergedcsv.csv