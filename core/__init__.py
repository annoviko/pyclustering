import subprocess;
import os;
import re;

def run_execution_object(argv):   
    process = subprocess.Popen(argv, universal_newlines = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE);
    process.wait();
    
    code_result = process.returncode;
    if (code_result != 0):
        stderr_result = process.stderr.read();
        raise NameError("Execution error: ", stderr_result);

    stdout_result = process.stdout.read();    
    return stdout_result;


def dbscan(path_to_file, eps, min_neighbors):
    stdout_result = run_execution_object(['./bin/dbscan.exe', path_to_file, str(eps), str(min_neighbors)]);
    print(stdout_result);
    

def hierarchical(path_to_file, number_clusters):  
    stdout_result = run_execution_object(['./bin/hierarchical.exe', path_to_file, str(number_clusters)]);
    print(stdout_result);


dbscan('../Samples/SampleSimple1.txt', 0.5, 2);
hierarchical('../Samples/SampleSimple1.txt', 2);