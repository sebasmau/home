@ECHO OFF
ECHO Creating environment
conda env create --prefix ./env_home_app --file environment.yml --force
pause