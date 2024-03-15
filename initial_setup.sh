echo [$(date)]: "START"


echo [$(date)]: "creating env with latest python version" 


conda create --prefix ./Nolangchain python=3.11.5 -y


echo [$(date)]: "activating the environment" 

source activate ./Nolangchain

echo [$(date)]: "installing the dev requirements" 

pip install -r requirements.txt

echo [$(date)]: "END" 
