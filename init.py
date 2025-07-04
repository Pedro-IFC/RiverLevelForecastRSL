from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
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

        resultados = forecast(dados)

        if not resultados:
            messagebox.showinfo("Sem resultados", "Não há dados suficientes para previsão.")
            return

        resultado_janela = Toplevel(root)
        resultado_janela.title("Resultados da Previsão")
        resultado_janela.geometry("1000x500")
        resultado_janela.geometry(f"{1000}x{500}+{(largura_tela // 2) - (1000 // 2)}+{(altura_tela // 2) - (500 // 2)}")

        ttk.Label(resultado_janela, text="Resultados da Previsão", font=("Helvetica", 14, "bold")).pack(pady=10)

        main_frame = Frame(resultado_janela)
        main_frame.pack(fill=BOTH, expand=True)

        frame_tabela = Frame(main_frame)
        frame_tabela.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        tabela = ttk.Treeview(frame_tabela, columns=("Modelo", "Previsão"), show="headings")
        tabela.heading("Modelo", text="Modelo")
        tabela.heading("Previsão", text="Previsão (nível)")
        tabela.pack(fill=BOTH, expand=True)

        valores_histograma = []

        for modelo, previsao in resultados:
            tabela.insert("", "end", values=(modelo, f"{previsao:.2f}"))
            valores_histograma.append(previsao)

        frame_grafico = Frame(main_frame)
        frame_grafico.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.hist(valores_histograma, bins=5, edgecolor='black', color='skyblue')
        ax.set_title('Distribuição das Previsões')
        ax.set_xlabel('Valor da Previsão')
        ax.set_ylabel('Frequência')

        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

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
ttk.Button(frm, text="Sair", command=root.destroy).grid(row=3, column=0, columnspan=2)

root.mainloop()
