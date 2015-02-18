import subprocess, os

read_the_docs_build = os.environ.get('READTHEDOCS', None) == 'True'

if read_the_docs_build:

    subprocess.call('cd ../; doxygen doxygen_config_pyclustering', shell=True)