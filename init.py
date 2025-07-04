from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functions import forecast

# Função para validar entrada numérica (inteiros ou decimais)
def somente_numeros(valor):
    if valor == "":
        return True
    try:
        float(valor)
        return True
    except ValueError:
        return False

# Função de Realizar previsão
def realizar_previsao():
    try:
        dados = {
            'rio_itu': float(entry_nivel_ituporanga.get()) if entry_nivel_ituporanga.get() else None,
            'chuva_itu': float(entry_chuva_ituporanga.get()) if entry_chuva_ituporanga.get() else None,
            'rio_taio': float(entry_nivel_taio.get()) if entry_nivel_taio.get() else None,
            'chuva_taio': float(entry_chuva_taio.get()) if entry_chuva_taio.get() else None,
        }
        print(dados)

        resultados = forecast(dados)

        if not resultados:
            messagebox.showinfo("Sem resultados", "Não há dados suficientes para previsão.")
            return

        # Criação de nova janela para exibir os resultados
        resultado_janela = Toplevel(root)
        resultado_janela.title("Resultados da Previsão")
        resultado_janela.geometry("500x300")

        ttk.Label(resultado_janela, text="Resultados da Previsão", font=("Helvetica", 14, "bold")).pack(pady=10)

        frame_resultado = ttk.Frame(resultado_janela, padding=10)
        frame_resultado.pack(expand=True, fill=BOTH)

        for modelo, previsao in resultados:
            texto = f"{modelo}: {previsao:.2f}"
            ttk.Label(frame_resultado, text=texto, font=("Helvetica", 12)).pack(anchor=W, pady=2)

    except ValueError:
        messagebox.showerror("Erro de entrada", "Por favor, insira apenas valores numéricos válidos.")

# Janela principal
root = Tk()
root.title("RiverLevelForecastRSL")

largura_janela = 1000
altura_janela = 500
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)
root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
root.resizable(True, True)

# Registrando a função de validação
validacao = root.register(somente_numeros)

frm = ttk.Frame(root, padding=20)
frm.pack(expand=True)

# Título
ttk.Label(frm, text="RiverLevelForecastRSL", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Campos de Ituporanga
frame_ituporanga = ttk.Frame(frm)
frame_ituporanga.grid(row=1, column=0, padx=20, sticky=N)

ttk.Label(frame_ituporanga, text="Ituporanga", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

ttk.Label(frame_ituporanga, text="Nível do rio:").grid(row=1, column=0, sticky=E, pady=5)
entry_nivel_ituporanga = ttk.Entry(frame_ituporanga, width=25, validate="key", validatecommand=(validacao, "%P"))
entry_nivel_ituporanga.grid(row=1, column=1, pady=5)

ttk.Label(frame_ituporanga, text="Chuva:").grid(row=2, column=0, sticky=E, pady=5)
entry_chuva_ituporanga = ttk.Entry(frame_ituporanga, width=25, validate="key", validatecommand=(validacao, "%P"))
entry_chuva_ituporanga.grid(row=2, column=1, pady=5)

# Campos de Taió
frame_taio = ttk.Frame(frm)
frame_taio.grid(row=1, column=1, padx=20, sticky=N)

ttk.Label(frame_taio, text="Taió", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

ttk.Label(frame_taio, text="Nível do rio:").grid(row=1, column=0, sticky=E, pady=5)
entry_nivel_taio = ttk.Entry(frame_taio, width=25, validate="key", validatecommand=(validacao, "%P"))
entry_nivel_taio.grid(row=1, column=1, pady=5)

ttk.Label(frame_taio, text="Chuva:").grid(row=2, column=0, sticky=E, pady=5)
entry_chuva_taio = ttk.Entry(frame_taio, width=25, validate="key", validatecommand=(validacao, "%P"))
entry_chuva_taio.grid(row=2, column=1, pady=5)

# Botão Realizar previsão
ttk.Button(frm, text="Realizar previsão", command=realizar_previsao).grid(row=2, column=0, columnspan=2, pady=20)

# Botão Sair
# ttk.Button(frm, text="Sair", command=root.destroy).grid(row=3, column=0, columnspan=2)

root.mainloop()
