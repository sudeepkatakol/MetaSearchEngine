WIKIDIRECTORY="./enwiki_dbow"
MODELDIRECTORY="./model"
if [ ! -d "$WIKIDIRECTORY" ]; then
  echo Download the file, 'enwiki_dbow.tgz' from 'https://ibm.ent.box.com/s/3f160t4xpuya9an935k84ig465gvymm2' and extract the folder in this directory
  echo If you have already downloaded make sure the folder is named as 'enwiki_dbow' itself and nothing else
  exit
fi

if [ ! -d "$MODELDIRECTORY" ]; then
  echo Model directory not found 
  exit
fi

source activate metasearchengine
if [ $? == '1' ]; then
	echo Conda environment not found.
	echo Creating it.
	conda env create -f environment.yml
	if [ ! $? == '0' ]; then
		echo Please make sure environment.yml is present in this directory and anaconda is installed properly in the system. 
	fi
	source activate metasearchengine
fi

pip install -r requirements.txt

python Webapp.py