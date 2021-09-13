from streamlit import bootstrap

real_script = 'main.py'
#real_script = 'test.py'

bootstrap.run(real_script, f'run.py {real_script}', [], {})