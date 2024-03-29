from Analizador.TablaSimbolos.instruccionAbstract import Instruccion
from Analizador.TablaSimbolos.Excepcion import Excepcion
from Analizador.TablaSimbolos.nodoASTabstract import NodoASTabstract

class Identificador(Instruccion):
    def __init__(self, fila, columna, identificador):
        self.fila = fila
        self.columna = columna
        self.identificador = identificador
        self.tipo = None #inicialmente no sabemos el tipo
        self.arreglo = False

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower()) #Buscamos la variable

        if simbolo == None:
            #no enocnotro la variable en la tabla de simbolos
            return Excepcion("La Variable " + self.identificador + " no ha sido declarada","Semantico", self.fila, self.columna)
        if simbolo.arreglo:
            self.arreglo = True
        self.tipo = simbolo.getTipo()
        
        return simbolo.getValor()

    def getArreglo(self):
        return self.arreglo

    def getNodo(self):
        nodo = NodoASTabstract("Identificador")
        nodo.agregarHijo(str(self.identificador))
        return nodo