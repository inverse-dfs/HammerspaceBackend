import os

class FormatSymbol:
    def __init__(self, START: str, STOP: str):
        self.START = START
        self.STOP = STOP

class FormatInjector:
    def __init__(self):
        self.symbols_dict = {
            "\\subsection*": FormatSymbol("$1=1$", "$1\\neq1$"),
        }
    
    def run(self, latex: str) -> str:
        for key, value in self.symbols_dict.items():
            # run some semblance of input validation
            stack = False
            for i in range(len(latex)):
                if i+len(value.START) < len(latex) and latex[i:i+len(value.START)] == value.START:
                    if stack == True:
                      return ''
                    stack = True
                elif i+len(value.STOP) < len(latex) and latex[i:i+len(value.STOP)] == value.STOP:
                    if stack == False:
                      return ''
                    stack = False

            # so much can go wrong, but this is an mvp!
            replace_start = latex.replace(value.START, key + "{")
            replace_end = replace_start.replace(value.STOP, "}")

            print(replace_end)
            return replace_end
        
class TestRunner:
    def __init__(self, directory):
        self.directory = directory

    def run_tests(self, test_function):
        files = os.listdir(self.directory)
        for file_name in files:
            file_path = os.path.join(self.directory, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    file_contents = file.read()
                output = test_function(file_contents)
                print(f"File: {file_name}\n Input: \n{file_contents}\n Output: \n{output}\n")

directory = './tests/injection_tests'
fi = FormatInjector()
runner = TestRunner(directory)
runner.run_tests(fi.run)


                
