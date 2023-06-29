import jinja2
import subprocess

class DocumentGenerator:
    def __init__(self):
        self.TEMPLATE_PATH="./template.jinja"
    
    def GenerateTEX(self, filename, data):
        fid = filename.rsplit('.', 1)[0]
        outputFile = fid + '.tex'
        templateLoader = jinja2.FileSystemLoader( searchpath="./" )
        templateEnv = jinja2.Environment( loader=templateLoader )
        template = templateEnv.get_template( self.TEMPLATE_PATH )
        templateVars = {
            "translated": data
        }
        outputText = template.render(templateVars) #need to figure out how to do this without loading all to memory
        with open(outputFile, mode="w", encoding="utf-8") as message:
            message.write(outputText)
        return outputFile
    
    def GeneratePDF(self, filename):
        fid = filename.rsplit('.', 1)[0]
        subprocess.run(["pdflatex", f"-jobname={fid}", filename])