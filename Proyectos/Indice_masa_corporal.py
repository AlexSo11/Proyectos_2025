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
from tkinter import messagebox

def calcular_imc():
    try:
        peso = float(entry_peso.get())
        altura = float(entry_altura.get())

        if peso <= 0 or altura <= 0:
            raise ValueError

        imc = peso / (altura ** 2)
        resultado = f"Tu IMC es: {imc:.2f}\n"

        if imc < 18.5:
            resultado += "Clasificación: Bajo peso"
        elif 18.5 <= imc < 24.9:
            resultado += "Clasificación: Normal"
        elif 25 <= imc < 29.9:
            resultado += "Clasificación: Sobrepeso"
        else:
            resultado += "Clasificación: Obesidad"

        messagebox.showinfo("Resultado IMC", resultado)
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores válidos.")

root = tk.Tk()
root.title("Calculadora IMC")
root.geometry("300x200")

tk.Label(root, text="Peso (kg):", font=("Arial", 12)).pack(pady=5)
entry_peso = tk.Entry(root, font=("Arial", 12))
entry_peso.pack(pady=5)

tk.Label(root, text="Altura (m):", font=("Arial", 12)).pack(pady=5)
entry_altura = tk.Entry(root, font=("Arial", 12))
entry_altura.pack(pady=5)

btn_calcular = tk.Button(root, text="Calcular IMC", font=("Arial", 12), command=calcular_imc)
btn_calcular.pack(pady=20)

root.mainloop()
