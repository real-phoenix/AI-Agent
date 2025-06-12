from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def run_tests_file_info(): 
    # print("Test 1: current directory '.' ")
    print(get_files_info("calculator", '.'), end = "\n\n")
    # print("Test 2: subdirectory 'pkg' ")
    print(get_files_info("calculator", 'pkg'), end = "\n\n")
    # print("Test 3: forbidden path '/bin' ")
    print(get_files_info("calculator", '/bin'), end = "\n\n")
    # print("Test 4: forbidden path '..' ")
    print(get_files_info("calculator", '..'), end = "\n\n")

def run_tests_file_content():
    print(get_file_content("calculator", "lorem.txt"), end= "\n\n")
    print(get_file_content("calculator", "main.py"), end= "\n\n")
    print(get_file_content("calculator", "pkg/calculator.py"), end= "\n\n")
    print(get_file_content("calculator", "/bin/cat"), end= "\n\n")

def run_tests_write_file(): 
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), end= "\n\n")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"), end= "\n\n")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"), end= "\n\n")

def run_tests_run_python(): 
    print(run_python_file("calculator", "main.py"), end="\n\n")
    print(run_python_file("calculator", "tests.py"), end="\n\n")
    print(run_python_file("calculator", "nonexistent.py"), end="\n\n")
    print(run_python_file("calculator", "../main.py"), end="\n\n")

if __name__ == "__main__": 
    run_tests_run_python()