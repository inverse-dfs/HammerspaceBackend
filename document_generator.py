import jinja2

class DocumentGenerator:
    def __init__(self):
        self.TEMPLATE_PATH="./template.tex"
    
    def GenerateTEX(filename, data):
        templateLoader = jinja2.FileSystemLoader( searchpath="/" )
        templateEnv = jinja2.Environment( loader=templateLoader )
        TEMPLATE_FILE = "templex.tex"
        template = templateEnv.get_template( self.TEMPLATE_FILE )
        templateVars = {
            "translated": data
        }
        outputText = template.render(templateVars) #need to figure out how to do this without loading all to memory
        output_file = filename + '.pdf'
        print(outputText)
        with open(output_file, mode="w", encoding="utf-8") as message:
            message.write(outputText)
        return output_file
    
    def GeneratePDF(filename):
        pass