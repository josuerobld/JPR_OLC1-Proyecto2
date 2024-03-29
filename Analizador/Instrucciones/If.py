from Analizador.TablaSimbolos.instruccionAbstract import Instruccion
from Analizador.TablaSimbolos.Excepcion import Excepcion
from Analizador.TablaSimbolos.tipo import TIPO
from Analizador.Instrucciones.Break import Break
from Analizador.Instrucciones.Continue import Continue
from Analizador.TablaSimbolos.tablaSimbolos import TablaSimbolos
from Analizador.Instrucciones.Return import Return
from Analizador.TablaSimbolos.nodoASTabstract import NodoASTabstract


class If(Instruccion):

    def __init__(self, fila, columna, expresionCondicion, instruccionesIf, instruccionesElse, elseIf):

        self.fila = fila
        self.columna = columna
        self.expresionCondicion = expresionCondicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.elseIf = elseIf

    def interpretar(self, tree, table):
        condicion = self.expresionCondicion.interpretar(tree, table) #interpretamos la condicion

        if isinstance(condicion, Excepcion): 
            #si hay error, lo retornamos
            return condicion

        if self.expresionCondicion.tipo == TIPO.BOOLEANO:
            #---------------------------------------IF = TRUE---------------------------------------
            if bool(condicion) == True:
                #Instrucciones por hacer si es verdadera la condicion

                TablaIF = TablaSimbolos(table)  #nueva tabla de simbolos, es decir un nuevo ambito

                for inst in self.instruccionesIf:
                    #ejecutamos todas las instrucciones dentro del if
                    result = inst.interpretar(tree, TablaIF)

                    if isinstance(result, Excepcion) :
                        tree.getExcepciones().append(result)
                        tree.updateConsole(result.toString())
                    if isinstance(result, Break) or isinstance(result, Continue) or isinstance(result, Return): 
                        #Retorna el valor de break, para que este llegue al bucle y alli haga break
                        return result

            #-------------------------------------IF = False--------------------------------------------
            else:

                if self.instruccionesElse != None:
                    #Si vienen instrucciones en el else
                    #creamos un nuevo entorno
                    TablaIfElse = TablaSimbolos(table)

                    for instruccion in self.instruccionesElse:
                        #ejecutamos cada instruccion
                        result = instruccion.interpretar(tree, TablaIfElse) 
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break) or isinstance(result, Continue) or isinstance(result, Return): 
                            #Retorna el valor de break, para que este llegue al bucle y alli haga break
                            return result
                elif self.elseIf != None:
                    #llamada recursiva al metodo interpretar nuevamente
                    result = self.elseIf.interpretar(tree, table)
                    if isinstance(result, Excepcion): 
                        return result
                    if isinstance(result, Break) or isinstance(result, Continue) or isinstance(result, Return): 
                        #Retorna el valor de break, para que este llegue al bucle y alli haga break
                        return result

        else:
            return Excepcion("La expresion ingresada como condicion tiene que ser booleana","Semantico", self.fila, self.columna)
    

    def getNodo(self):
        nodo = NodoASTabstract("If")

        instruccionesIf = NodoASTabstract("Instrucciones - If")
        for instr in self.instruccionesIf:
            instruccionesIf.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instruccionesIf)

        if self.instruccionesElse != None:
            instruccionesElse = NodoASTabstract("Instrucciones - Else")
            for instr in self.instruccionesElse:
                instruccionesElse.agregarHijoNodo(instr.getNodo())
            nodo.agregarHijoNodo(instruccionesElse) 
        elif self.elseIf != None:
            nodo.agregarHijoNodo(self.elseIf.getNodo())

        return nodo
        
    def stringToBool(self,val):
        #pasa todo a minustulas y luego mira si la palabra es true
        return val.lower() in ("true")


