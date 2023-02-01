ECHO enable environment
call conda activate ..\python_environment\env_home_app
rem
call streamlit run ..\dashboard\home.py
pause

