echo Hello, we will begin installing the fitbitETL app. 
echo First, start by creating a new environment for the program. 
echo Then, installing all of the dependencies from Anaconda Distribution. 


conda create -n fitbitETL2 python=3.6
conda init bash
conda activate fitbitETL2
conda install --file requirements.txt

echo install is finished. 
echo " You can start using the program by typing in "
echo " python ETL.py" 