from streamlit import bootstrap

#real_script = 'main.py'
real_script = 'map3.py'
bootstrap.run(real_script, f'run.py {real_script}', [], {})