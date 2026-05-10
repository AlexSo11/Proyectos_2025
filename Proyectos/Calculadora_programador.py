"""
⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢰⣿⡿⠗⠀⠠⠄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⡜⠁⠀⠀⠀⠀⠀⠈⠑⢶⣶⡄
⢀⣶⣦⣸⠀⢼⣟⡇⠀⠀⢀⣀⠀⠘⡿⠃
⠀⢿⣿⣿⣄⠒⠀⠠⢶⡂⢫⣿⢇⢀⠃⠀
⠀⠈⠻⣿⣿⣿⣶⣤⣀⣀⣀⣂⡠⠊⠀⠀
⠀⠀⠀⠃⠀⠀⠉⠙⠛⠿⣿⣿⣧⠀⠀⠀
⠀⠀⠘⡀⠀⠀⠀⠀⠀⠀⠘⣿⣿⡇⠀⠀
⠀⠀⠀⣷⣄⡀⠀⠀⠀⢀⣴⡟⠿⠃⠀⠀
⠀⠀⠀⢻⣿⣿⠉⠉⢹⣿⣿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠉⠁⠀⠀⠀⠉⠁

Desarrollo AlexWhite USER GIT AlexSo11
"""
import tkinter as tk
import math

class Calculadora:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora 2.0")
        #self.root.geometry("340x420")
        
        #variables de estado
        self.display_text = ""
        self.operand1 = None
        self.operator = None
        self.waiting_operand = False
        self.last_result = None
        
        self.crear_interfaz()
        self.root.mainloop()
    
    def crear_interfaz(self):
        #display principal
        self.entry_display = tk.Entry(self.root, font=("Arial", 12), justify="right", bd=5)
        self.entry_display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="we")
        
        #labels para conversiones
        labels = ["Hex:", "Dec:", "Oct:", "Bin:"]
        self.conversion_labels = []
        for i, text in enumerate(labels, start=1):
            label = tk.Label(self.root, text=text, font=("Arial", 12), anchor="w")
            label.grid(row=i, column=0, columnspan=6, sticky="w", padx=10)
            self.conversion_labels.append(label)
        
        fila_inicio = 5 
        
        #botones superiores
        extra_top = [
            ("A", fila_inicio, 0),
            ("!", fila_inicio, 1),
            ("%", fila_inicio, 2), 
            ("CE", fila_inicio, 3), 
            ("<-", fila_inicio, 4),  
        ]
        for (texto, fila, col) in extra_top:
            self.crear_boton(texto, fila, col)
        
        #botones de operaciones trigonometricas
        fila_trig = fila_inicio + 1
        trig_ops = [
            ("B", fila_trig, 0),
            ("sin", fila_trig, 1),
            ("/", fila_trig, 2),
            ("√", fila_trig, 3),
            ("^", fila_trig, 4)
        ]
        for (texto, fila, col) in trig_ops:
            self.crear_boton(texto, fila, col)
        
        #botones principales
        botones = [
            ("C", fila_trig+1, 0), ("9", fila_trig+1, 1), ("8", fila_trig+1, 2), 
            ("7", fila_trig+1, 3), ("x", fila_trig+1, 4),
            ("D", fila_trig+2, 0), ("6", fila_trig+2, 1), ("5", fila_trig+2, 2), 
            ("4", fila_trig+2, 3), ("-", fila_trig+2, 4),
            ("E", fila_trig+3, 0), ("3", fila_trig+3, 1), ("2", fila_trig+3, 2), 
            ("1", fila_trig+3, 3), ("+", fila_trig+3, 4),
            ("F", fila_trig+4, 0), ("+/-", fila_trig+4, 1), ("0", fila_trig+4, 2), 
            (".", fila_trig+4, 3), ("=", fila_trig+4, 4)
        ]
        
        for (texto, fila, col) in botones:
            self.crear_boton(texto, fila, col)
        self.actualizar_display()
    
    def crear_boton(self, texto, fila, col): #bg=None, fg=None
        #if bg is None or fg is None:
        #    bg, fg= self.obtener_color_boton(texto)"""
        boton = tk.Button(self.root, text=texto, font=("Arial", 12), width=5, height=2,
                         command=lambda t=texto: self.boton_presionado(t))
        boton.grid(row=fila, column=col, padx=5, pady=5)
        return boton
    
    #def obtener_color_boton(self, texto):
        #if texto in ["<-"]:
            #return "#FF9500", "#000000"

    def boton_presionado(self, texto):
        if texto.isdigit() or texto in "ABCDEF.":
            self.agregar_digito(texto)
        elif texto in "+-x/^":
            self.establecer_operador(texto)
        elif texto == "=":
            self.calcular()
        elif texto == "C":
            self.limpiar_todo()
        elif texto == "CE":
            self.limpiar_entrada()
        elif texto == "<-":
            self.retroceder()
        elif texto == "+/-":
            self.cambiar_signo()
        elif texto == "√":
            self.raiz_cuadrada()
        elif texto == "%":
            self.porcentaje()
        elif texto == "!":
            self.factorial()
        elif texto == "sin":
            self.seno()
        
        self.actualizar_conversiones()
    
    def agregar_digito(self, digito):
        if self.waiting_operand:
            self.display_text = ""
            self.waiting_operand = False
        
        #validar punto decimal
        if digito == ".":
            if "." in self.display_text:
                return
            if self.display_text == "":
                self.display_text = "0"
        
        #validar digitos hexadecimales
        if digito in "ABCDEF":
            if self.display_text == "" or self.display_text == "0":
                self.display_text = digito
            else:
                self.display_text += digito
        else:
            if self.display_text == "0" and digito != ".":
                self.display_text = digito
            else:
                self.display_text += digito
        
        self.actualizar_display()
    
    def establecer_operador(self, op):
        if self.display_text:
            if self.operand1 is not None and not self.waiting_operand:
                self.calcular()
            
            self.operand1 = self.obtener_valor()
            self.operator = op
            self.waiting_operand = True
    
    def calcular(self):#funciones para el boton igual
        if self.operand1 is not None and self.operator and not self.waiting_operand:
            operand2 = self.obtener_valor()
            resultado = None
            
            try:
                if self.operator == "+":
                    resultado = self.sumar(self.operand1, operand2)
                elif self.operator == "-":
                    resultado = self.restar(self.operand1, operand2)
                elif self.operator == "x":
                    resultado = self.multiplicar(self.operand1, operand2)
                elif self.operator == "/":
                    if operand2 == 0:
                        raise ValueError("División por cero")
                    resultado = self.dividir(self.operand1, operand2)
                elif self.operator == "^":
                    resultado = self.potencia(self.operand1, operand2)
                
                if resultado is not None:
                    self.last_result = resultado
                    self.display_text = self.formatear_numero(resultado)
                    self.operand1 = None
                    self.operator = None
                    self.waiting_operand = False
                    
            except (ValueError, ZeroDivisionError) as e:
                self.display_text = "Error"
                self.operand1 = None
                self.operator = None
                self.waiting_operand = False
        
        self.actualizar_display()
    
    #funciones principales de los botones
    def sumar(self, a, b):#suma
        return a + b
    
    def restar(self, a, b):#resta
        return a - b
    
    def multiplicar(self, a, b):#multi
        if b == 0 or a == 0:
            return 0
        
        resultado = 0
        negativo = False
        
        #manejar números negativos
        if a < 0 and b < 0:
            a, b = -a, -b
        elif a < 0:
            a = -a
            negativo = True
        elif b < 0:
            b = -b
            negativo = True
        
        #multiplicacion por sumas repetidas
        for _ in range(int(b)):
            resultado += a
        
        #ajustar para decimales
        decimal_part = b - int(b)
        if decimal_part > 0:
            resultado += a * decimal_part
        
        return -resultado if negativo else resultado
    
    def dividir(self, a, b):#divicion
        if b == 0:
            raise ZeroDivisionError("División por cero")
        negativo = False
        
        #manejar numeros negativos
        if a < 0 and b < 0:
            a, b = -a, -b
        elif a < 0:
            a = -a
            negativo = True
        elif b < 0:
            b = -b
            negativo = True
        
        #division entera por restas repetidas
        cociente = 0
        resto = a
        
        while resto >= b:
            resto -= b
            cociente += 1
        
        #manejar parte decimal
        if resto > 0:
            #aproximacion decimal simple
            decimal = 0
            for i in range(1, 7):#hasta 6 decimales
                resto *= 10
                if resto >= b:
                    decimal_digit = 0
                    while resto >= b:
                        resto -= b
                        decimal_digit += 1
                    decimal += decimal_digit / (10 ** i)
            
            cociente += decimal
        
        return -cociente if negativo else cociente
    
    def potencia(self, base, exponente):#potencia
        if exponente == 0:
            return 1
        if exponente == 1:
            return base
        
        resultado = 1
        exp_abs = abs(exponente)
        
        #potencia usando multiplicaciones repetidas
        for _ in range(int(exp_abs)):
            resultado = self.multiplicar(resultado, base)
        
        #manejar exponentes decimales (aproximacion simple)
        decimal_part = exp_abs - int(exp_abs)
        if decimal_part > 0:
            #para exponentes decimales, usar una aproximacion
            resultado *= 1 + decimal_part * (base - 1)
        
        #manejar exponentes negativos
        if exponente < 0:
            resultado = self.dividir(1, resultado)
        
        return resultado
    
    def raiz_cuadrada(self):#raiz cuadrada
        if not self.display_text:
            return
        
        numero = self.obtener_valor()
        if numero < 0:
            self.display_text = "Error"
            return
        
        if numero == 0:
            resultado = 0
        else:
            #metodo babilonico (aproximaciones sucesivas)
            aproximacion = numero / 2
            for _ in range(20):  #20 iteraciones para buena precisión
                nueva_aproximacion = (aproximacion + numero / aproximacion) / 2
                if abs(nueva_aproximacion - aproximacion) < 1e-10:
                    break
                aproximacion = nueva_aproximacion
            resultado = aproximacion
        
        self.display_text = self.formatear_numero(resultado)
        self.actualizar_display()
    
    def factorial(self):#factorial
        if not self.display_text:
            return
        
        numero = self.obtener_valor()
        if numero < 0 or numero != int(numero):
            self.display_text = "Error"
            return
        
        resultado = 1
        for i in range(2, int(numero) + 1):
            resultado = self.multiplicar(resultado, i)
        
        self.display_text = self.formatear_numero(resultado)
        self.actualizar_display()
    
    def porcentaje(self):#porcentaje
        if not self.display_text:
            return
        
        numero = self.obtener_valor()
        resultado = self.dividir(numero, 100)
        
        self.display_text = self.formatear_numero(resultado)
        self.actualizar_display()
    
    def seno(self):#seno
        if not self.display_text:
            return
        
        angulo = self.obtener_valor()
        
        #convertir a radianes
        radianes = angulo * math.pi / 180
        
        #serie de Taylor para seno
        resultado = 0
        for n in range(10):  # 10 terminos de la serie
            termino = self.potencia(-1, n) * self.potencia(radianes, 2*n + 1) / math.factorial(2*n + 1)
            resultado += termino
        
        self.display_text = self.formatear_numero(resultado)
        self.actualizar_display()
    
    #funcines auxiliares de los botones
    def obtener_valor(self):#obtener valor numerico del display, manejando hexadecimal
        if not self.display_text:
            return 0
        
        #verificar si es hexadecimal
        if any(c in "ABCDEF" for c in self.display_text.upper()):
            try:
                return int(self.display_text, 16)
            except:
                return 0
        try:
            return float(self.display_text)
        except:
            return 0
    
    def formatear_numero(self, numero):#Para mejor visibilidad
        if isinstance(numero, int) or numero.is_integer():#elimina decimales innecesarios en enteros
            return str(int(numero))
        else:
            return f"{numero:.6f}".rstrip('0').rstrip('.')#limita y limpia decimales en reales
    
    def limpiar_todo(self):#limpiar todo
        self.display_text = ""
        self.operand1 = None
        self.operator = None
        self.waiting_operand = False
        self.actualizar_display()
    
    def limpiar_entrada(self):#limpiar entrada
        self.display_text = ""
        self.actualizar_display()
    
    def retroceder(self):#funcion para el boton eliminar
        if self.display_text:
            self.display_text = self.display_text[:-1]
            self.actualizar_display()
    
    def cambiar_signo(self):#funcion para el boton +/-
        if self.display_text and self.display_text != "0":
            if self.display_text[0] == "-":
                self.display_text = self.display_text[1:]
            else:
                self.display_text = "-" + self.display_text
            self.actualizar_display()
    
    def actualizar_display(self):#actualizar el display
        self.entry_display.delete(0, tk.END)
        self.entry_display.insert(0, self.display_text if self.display_text else "0")
    
    def actualizar_conversiones(self):#convesiones en Label
        try:
            valor = self.obtener_valor()
            if self.display_text == "" or self.display_text == "Error":
                for label in self.conversion_labels:
                    label.config(text=label.cget("text").split(":")[0] + ": ")
                return
            
            #hexadecimal
            hex_val = self.decimal_a_hexadecimal(int(valor))
            self.conversion_labels[0].config(text=f"Hex: {hex_val}")
            
            #decimal
            self.conversion_labels[1].config(text=f"Dec: {int(valor)}")
            
            #octal
            oct_val = self.decimal_a_octal(int(valor))
            self.conversion_labels[2].config(text=f"Oct: {oct_val}")
            
            #binario
            bin_val = self.decimal_a_binario(int(valor))
            self.conversion_labels[3].config(text=f"Bin: {bin_val}")
            
        except:
            for label in self.conversion_labels:
                label.config(text=label.cget("text").split(":")[0] + ": Error")
    
    #algoritmos para conversiones decimal a x cosa
    def decimal_a_hexadecimal(self, numero):#hexadecimal
        if numero == 0:
            return "0"
        
        negativo = numero < 0
        numero = abs(numero)
        
        hex_digits = "0123456789ABCDEF"
        resultado = ""
        
        while numero > 0:
            resto = numero % 16
            resultado = hex_digits[resto] + resultado
            numero = numero // 16
        
        return "-" + resultado if negativo else resultado
    
    def decimal_a_octal(self, numero):#octal
        if numero == 0:
            return "0"
        
        negativo = numero < 0
        numero = abs(numero)
        
        resultado = ""
        
        while numero > 0:
            resto = numero % 8
            resultado = str(resto) + resultado
            numero = numero // 8
        
        return "-" + resultado if negativo else resultado
    
    def decimal_a_binario(self, numero):#binario
        if numero == 0:
            return "0"
        
        negativo = numero < 0
        numero = abs(numero)
        
        resultado = ""
        
        while numero > 0:
            resto = numero % 2
            resultado = str(resto) + resultado
            numero = numero // 2
        
        return "-" + resultado if negativo else resultado

if __name__ == "__main__":
    Calculadora()
