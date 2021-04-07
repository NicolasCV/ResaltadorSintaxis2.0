#Nicolas Cardenas Valdez y Jose Pablo Cruz
import string

#Errores universales
LexError=False
ParsingError=False

#Se importa el file y se guarda en una variable global
def inputFile(filename):
    global EXPf

    #Expression Input
    EXPfile=open(filename)
    EXPf=EXPfile.read()

    EXPfile.flush()
    EXPfile.close()


#Regresa que tipo de chartype es
def getChar(stringC):
    if stringC == "int":
        return "INT"

    elif stringC == "float":
        return "FLOAT"

    elif stringC == "+":
        return "PLUS"

    elif stringC == "-":
        return "MINUS"
    
    elif stringC == "*":
        return "ASTER"

    elif stringC == "/":
        return "DIVIDE"
    
    elif stringC in ["(",")"]:
        return "PARENTHESES"

    elif stringC == "=":
        return "EQUAL"

    elif stringC == "begin":
        return "BEGIN"
    
    elif stringC == "program":
        return "PROGRAM"

    elif stringC == "end":
        return "END"
    
    elif stringC[-1] == ".":
        return "ERROR"

    elif stringC.isdecimal() or (stringC.split(".")[0].isdecimal() and stringC.split(".")[1].isdecimal()):
        return "NUM"

    elif stringC[0].isalpha():
        return "ID"

    else:
        return "ERROR"

#Parser que lanza error si esta mal el formato
def parser():
    ''


#Funcion para hacer el output a HTML
def output():
    global ParsingError,LexError, EXPf

    #Se abre el html en el que se pondra
    with open(R"output.html","w") as myFile:
        myFile.write('<html>\n')
        myFile.write('<body style="background-color:black">\n')
        myFile.write('<link rel="stylesheet" href="mystyle.css">\n')
        
        EXPfs=EXPf.split()
        programBegun=False

        for i in range(len(EXPfs)):
            
            #Se comienza el primer header con programa,id,begin
            if getChar(EXPfs[i]) == "PROGRAM":
                myFile.write('<h3>')

            #Siempre que hay int,float,begin o end se pone un endline antes (excepto en la primera)
            if getChar(EXPfs[i]) in ["BEGIN","INT","FLOAT","END"]:
                if getChar(EXPfs[i-1]) != "BEGIN":
                    myFile.write('<br>')

            #Se abre el header para el end 
            if getChar(EXPfs[i]) == "END":
                myFile.write('<h3>') 

            #Si hay dos IDs seguidas,hay un endline entre ellos o un numero antes, siempre y cuando este empezado el programa
            if getChar(EXPfs[i]) == "ID" and getChar(EXPfs[i-1]) in ["ID","NUM"] and programBegun==True:
                myFile.write("<br><span class='INDENT'></span>")          

            #Imprime la linea con el texto y su respectiva clase
            line="<span class='{0}'>{1} ".format(getChar(EXPfs[i]),EXPfs[i])
            myFile.write(line)

            #Se cierra el primer header con programa,id,begin y se comienza el codigo
            if getChar(EXPfs[i]) == "BEGIN":
                myFile.write('</span></h3>\n')
                programBegun=True
                continue
            
            #Se cierra el header para el end
            if getChar(EXPfs[i]) == "END":
                myFile.write('</h3>')
                continue
            
            #Se cierra el span
            myFile.write('</span>\n')

            if getChar(EXPfs[i])=="ERROR":
                LexError=True

        #Da los errores abajo de todo el programa para que el usuario sepa que hubo error
        if ParsingError:
            myFile.write('<h1><span class=FormatERROR>Parsing ERROR</span></h1>')

        if LexError:
            myFile.write('<h1><span class=ERROR>Syntaxis ERROR</span></h1>')

        #Se cierra el programa
        myFile.write('</body>')
        myFile.write('</html>')
        myFile.close()
 

inputFile("inputFileOne.txt")
output()



