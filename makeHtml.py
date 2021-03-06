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
def getTokenType(stringC):
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
    
    elif stringC == "(":
        return "O_PARENTHESES"
    
    elif stringC == ")":
        return "C_PARENTHESES"

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
    EXPfile.flush()
    EXPfile.close()

def getTokens(args):
    global tokenList

    for x in args:
        tokenList.append(getTokenType(x))
    tokenList.append("EOF")


def lexer(stringC):
    global tokenList,LexError,texts
    stringC+=' '

    LETTER = int(0)
    DIGIT = int(1)
    POINT = int(2)
    PLUS_SIGN = int(3)
    MULT_SIGN = int(4)
    LEFT_PAR = int(5)
    RIGHT_PAR = int(6)
    EQUAL = int(7)
    MINUS_SIGN = int(8)
    DIVIDE = int(9)
    SPACE = int(10)
    EOS = int(11)
    UNKNOWN = int(-1)


    ST_INITIAL = int(0)
    ST_ID = int(1)
    ST_DIGIT = int(2)
    ST_1ST_DIGIT = int(3)
    ST_NEXT_DIGITS = int(4)
    ST_F_ID = int(100)
    ST_F_INT = int(101)
    ST_F_FLOAT = int(102)
    ST_F_PLUS_SIGN = int(103)
    ST_F_MULT_SIGN = int(104)
    ST_F_LEFT_PAR = int(105)
    ST_F_RIGHT_PAR = int(106)
    ST_F_EQUAL = int(107)
    ST_F_MINUS_SIGN = int(108)
    ST_F_DIVIDE = int(109)
    ST_ERROR = int(-1)

    def getCharType(c):

        if c.isalpha(): 
            return LETTER
        
        elif c.isdigit() : 
            return DIGIT
        
        elif c == '.': 
            return POINT

        elif c == '+': 
            return PLUS_SIGN
        
        elif c == '=': 
            return EQUAL

        elif c == '-': 
            return MINUS_SIGN

        elif c == '*': 
            return MULT_SIGN

        elif c == '(': 
            return LEFT_PAR
            
        elif c == ')': 
            return RIGHT_PAR

        elif c == '/': 
            return DIVIDE

        elif c == '\n': 
            return EOS

        elif c == ' ': 
            return SPACE
        
        return UNKNOWN
    
    texts=[]

    transitionMatrix = [[ST_ID,ST_DIGIT,ST_ERROR,ST_F_PLUS_SIGN,ST_F_MULT_SIGN,ST_F_LEFT_PAR,ST_F_RIGHT_PAR,ST_F_EQUAL,ST_F_MINUS_SIGN,ST_F_DIVIDE,ST_INITIAL,ST_INITIAL],
                        [ST_ID,ST_ID,ST_ERROR,ST_F_ID,ST_F_ID,ST_F_ID,ST_F_ID,ST_F_ID,ST_F_ID,ST_F_ID,ST_F_ID,ST_F_ID],
                        [ST_ERROR,ST_DIGIT,ST_1ST_DIGIT,ST_F_INT,ST_F_INT,ST_F_INT,ST_F_INT,ST_F_INT,ST_F_INT,ST_F_INT,ST_F_INT,ST_F_INT],
                        [ST_ERROR,ST_NEXT_DIGITS,ST_ERROR,ST_ERROR,ST_ERROR,ST_ERROR,ST_ERROR,ST_ERROR,ST_ERROR,ST_ERROR,ST_ERROR,ST_ERROR],
                        [ST_ERROR,ST_NEXT_DIGITS,ST_ERROR,ST_F_FLOAT,ST_F_FLOAT,ST_F_FLOAT,ST_F_FLOAT,ST_F_FLOAT,ST_F_FLOAT,ST_F_FLOAT,ST_F_FLOAT,ST_F_FLOAT]]

    lexeme = ""
    currentChar = ''
    idx = 0
    shouldRead = True

    state = ST_INITIAL

    while True:
        while state != ST_ERROR and state < 100:
            if idx == len(stringC):
                return

            if shouldRead:
                currentChar = stringC[idx]
                idx+=1
                
            else:
                shouldRead = True
            
            
            charType = getCharType(currentChar)
            
            state = transitionMatrix[state][charType]

            if state < 100 and charType != SPACE and charType!=EOS:
                lexeme+=currentChar

        if state == ST_F_ID:
            if lexeme == "program":
                tokenList.append("PROGRAM")

            elif lexeme == "begin":
                tokenList.append("BEGIN")

            elif lexeme == "end":
                tokenList.append("END")
                tokenList.append("EOF")
                texts.append("end")
                return
            
            elif lexeme == "int":
                tokenList.append("INT")

            elif lexeme == "float":
                tokenList.append("FLOAT")

            else:
                tokenList.append("ID")
            
            shouldRead=False
    

        elif state == ST_F_INT:
            tokenList.append("NUM")
            shouldRead=False
        

        elif state == ST_F_FLOAT:
            tokenList.append("NUM")
            shouldRead=False
        

        elif state ==ST_F_PLUS_SIGN:
            lexeme+=currentChar
            tokenList.append("PLUS")
    

        elif state == ST_F_MULT_SIGN:
            lexeme+=currentChar
            tokenList.append("ASTER")


        elif state == ST_F_LEFT_PAR:
            lexeme+=currentChar
            tokenList.append("O_PARENTHESES")

        
        elif state == ST_F_RIGHT_PAR:
            lexeme+=currentChar
            tokenList.append("C_PARENTHESES")

        
        elif state == ST_F_EQUAL:
            lexeme+=currentChar
            tokenList.append("EQUAL")


        elif state == ST_F_MINUS_SIGN:
            lexeme+=currentChar
            tokenList.append("MINUS")
        
        elif state == ST_F_DIVIDE:
            lexeme+=currentChar
            tokenList.append("DIVIDE")

        elif state == ST_ERROR:
            lexeme+=currentChar
            tokenList.append("ERROR") 
            LexError=True
        
        #elif state == ST_F_DIVIDE:
        #    tokenList.append("DIVIDE") 
        #    shouldRead=False 
        
        if lexeme != '':
            texts.append(lexeme)

        lexeme = ''
        state = ST_INITIAL


#Parentesis abierto o no, para el parser
opened = False

#Funciones para el parser
def ParseError(tok):
    global ParsingError,counter,tokenList
    ParsingError = True
    tokenList[counter-1]="FormatERROR"
    tokenList[counter-2]="FormatERROR"
    print("Error in token:",tok,"["+str(counter-1)+"]")

def nextToken():
    global counter,tok,tokenList
    if counter < len(tokenList):
        tok = tokenList[counter]
        counter+=1

def match(tokens):
    global tok,counter
    #print(counter-1,tok,tokens)

    if tok in tokens:
        nextToken()
    else:
        ParseError(tok)

def variable():
    match(["INT","FLOAT"])
    match(["ID"])

def operand():
    global tok

    match(["PLUS","DIVIDE","MINUS","ASTER"])

    if tok == "O_PARENTHESES":
        expression()
    else:
        match(["ID","NUM"])

def expression():
    #Opened es la variable de abrir
    global tok,opened
    
    if tok == "O_PARENTHESES":
        match("O_PARENTHESES")
        opened = True
        expression()
    else:
        match(["NUM","ID"])
        
        if tok in ["PLUS","DIVIDE","MINUS","ASTER"]:
            operand()

        if tok == "C_PARENTHESES" and opened:
            match("C_PARENTHESES")
            opened = False

def assignment():
    global opened
    
    match(["ID"])
    match(["EQUAL"])
    expression()

    if opened:
        ParseError("OPENED PARENTHESES NOT CLOSED")

def exprRest():
    global ParsingError,tok
    
    if not ParsingError:

        #CODE->VAR CODE
        if tok in ["INT","FLOAT"]:
            variable()
            exprRest()

        elif tok == "ID":
            assignment()
            exprRest()

        #VAR->TYPE ID
        #TYPE-> "INT","FLOAT"

        elif tok in ["PLUS","DIVIDE","MINUS","ASTER"]:
            operand()
            exprRest()

        elif tok == "ERROR":
            match(["ERROR"])
            exprRest()
        
        elif tok == "END":
            match(["END"])
        
        else:
            ParseError("PARSE ERROR")


    else:
        print("ERROR")
    
def stmt():
    #START=>PROGRAM ID BEING CODE END
    #CODE->E
    match("PROGRAM")
    match("ID")
    match("BEGIN")
    exprRest()

#Parser que lanza error si esta mal el formato
def parse():
    global tok
    nextToken()
    stmt()

#Funcion para hacer el output a HTML
def output():
    global ParsingError,LexError, EXPfs,texts

    #Se abre el html en el que se pondra
    with open(R"output.html","w") as myFile:
        myFile.write('<html>\n')
        myFile.write('<body style="background-color:black">\n')
        myFile.write('<link rel="stylesheet" href="mystyle.css">\n')

        programBegun=False
        tokenList.pop()

        for i in range(len(tokenList)):
            
            #Se comienza el primer header con programa,id,begin
            if tokenList[i] == "PROGRAM":
                myFile.write('<h3>')

            if tokenList[i] == "END":
                myFile.write('<h3>') 
            
            if (tokenList[i] == "ID" and tokenList[i-1] in ["ID","NUM"]):
                myFile.write("<br>")
                myFile.write("<span class='INDENT'></span>\n")  

            elif tokenList[i] == "ID" and tokenList[i+1] == "EQUAL":
                myFile.write("<span class='INDENT'></span>\n")  

            #Siempre que hay int,float,begin o end se pone un endline antes (excepto en la primera)
            elif tokenList[i] in ["BEGIN","INT","FLOAT","END"]:
                if getTokenType(tokenList[i-1]) != "BEGIN":
                    myFile.write('<br>')     

            #Imprime la linea con el texto y su respectiva clase
            line="<span class='{0}'>{1} ".format(tokenList[i],texts[i])
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
lexer(EXPf)

for i in range(len(texts)):
    print(texts[i],tokenList[i])

parse()
output()



