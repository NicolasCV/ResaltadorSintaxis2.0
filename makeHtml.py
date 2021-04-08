#Nicolas Cardenas Valdez y Jose Pablo Cruz
import string

#Errores universales
LexError=False
ParsingError=False

#Variables globales para el parser
counter = 0
tok=""
tokenList=[]

#Regresa que tipo de chartype es
def getCharType(stringC):
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

#Se importa el file y se guarda en una variable global
def inputFile(filename):
    global EXPf,EXPfs,tokenList

    #Expression Input
    EXPfile=open(filename)
    EXPf=EXPfile.read()
    EXPfs=EXPf.split()

    for x in EXPfs:
        tokenList.append(getCharType(x))

    tokenList.append("EOF")

    EXPfile.flush()
    EXPfile.close()

#Funciones para el parser
def ParseError(tok):
    global ParsingError,counter,tokenList
    ParsingError = True
    tokenList[counter-1]="FormatERROR"
    print("Error in token:",tok,"["+str(counter)+"]")

def nextToken():
    global counter,tok,tokenList
    tok = tokenList[counter]
    counter+=1

def match(tokens):
    global tok,counter
    print(counter-1,tok)

    if tok in tokens:
        nextToken()
    else:
        ParseError(tok)

def exprRest():
    global ParsingError,tok
    #CODE->VAR CODE
    #CODE->ASSIGNMENT CODE 
    #CODE->E
    #VAR->TYPE ID
    #TYPE-> "INT","FLOAT"
    #ASSIGNMENT-> ID = EXPR
    #EXPR -> OPERAND EXPR_REST
    #EXPR_REST-> + OPERAND EXPREST | - OPERAND EXPR_REST | * OPERAND EXPR_REST | / OPERAND EXPR_REST
    if not ParsingError:

        if tok in ["INT","FLOAT"]:
            match(["INT","FLOAT"])
            match(["ID"])
            match(["INT","FLOAT","ID"])
            exprRest()
        
        elif tok == "NUM":
            match(["NUM"])
            exprRest()

        elif tok == "ID":
            match(["ID"])
            match(["EQUAL"])
            match(["NUM","ID","PARENTHESES"])
            exprRest()

        elif tok == "PARENTHESES":
            print("par")
            match(["PARENTHESES"])
            match(["PLUS","DIVIDE","MINUS","ASTER","ID","NUM"])
            exprRest()

        elif tok in ["PLUS","DIVIDE","MINUS","ASTER","ID","NUM"]:
            match(["PLUS","DIVIDE","MINUS","ASTER","ID","NUM"])
            match(["ID","NUM"])
            exprRest()

        elif tok == "ERROR":
            match("ERROR")
            exprRest()
        
        elif tok == "END":
            ""

        else:
            ParsingError=True
    else:
        print("ERROR")
    #EXPR_REST->E
    #OPERAND -> NUM | ID
    #OPERAND -> (EXPR)

def stmt():
    #START=>PROGRAM ID BEING CODE END
    match("PROGRAM")
    match("ID")
    match("BEGIN")
    exprRest()
    match("END")

#Parser que lanza error si esta mal el formato
def parse():
    global tok
    nextToken()
    stmt()
    #match("END")


#Funcion para hacer el output a HTML
def output():
    global ParsingError,LexError, EXPfs,tokenList

    #Se abre el html en el que se pondra
    with open(R"output.html","w") as myFile:
        myFile.write('<html>\n')
        myFile.write('<body style="background-color:black">\n')
        myFile.write('<link rel="stylesheet" href="mystyle.css">\n')

        programBegun=False

        for i in range(len(EXPfs)):
            
            #Se comienza el primer header con programa,id,begin
            if tokenList[i] == "PROGRAM":
                myFile.write('<h3>')

            #Siempre que hay int,float,begin o end se pone un endline antes (excepto en la primera)
            if tokenList[i] in ["BEGIN","INT","FLOAT","END"]:
                if getCharType(EXPfs[i-1]) != "BEGIN":
                    myFile.write('<br>')

            #Se abre el header para el end 
            if tokenList[i] == "END":
                myFile.write('<h3>') 

            #Si hay dos IDs seguidas,hay un endline entre ellos o un numero antes, siempre y cuando este empezado el programa
            if tokenList[i] == "ID" and getCharType(EXPfs[i-1]) in ["ID","NUM"] and programBegun==True:
                myFile.write("<br><span class='INDENT'></span>")          

            #Imprime la linea con el texto y su respectiva clase
            line="<span class='{0}'>{1} ".format(tokenList[i],EXPfs[i])
            myFile.write(line)

            #Se cierra el primer header con programa,id,begin y se comienza el codigo
            if tokenList[i] == "BEGIN":
                myFile.write('</span></h3>\n')
                programBegun=True
                continue
            
            #Se cierra el header para el end
            if tokenList[i] == "END":
                myFile.write('</h3>')
                continue
            
            #Se cierra el span
            myFile.write('</span>\n')

            if tokenList[i]=="ERROR":
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
parse()
output()



