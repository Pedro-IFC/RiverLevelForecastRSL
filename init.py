from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from functions import forecast, media_ponderada_modelos, get_modelo_eq

historico_previsoes = []

def somente_numeros(valor):
    if valor == "":
        return True
    try:
        float(valor)
        return True
    except ValueError:
        return False

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
        resultado_janela.geometry(f"{1000}x{500}+{(largura_tela // 2) - (1000 // 2)}+{(altura_tela // 2) - (500 // 2)}")

        historico_previsoes.append({
            "entrada": dados.copy(),
            "resultado": resultados.copy()
        })

        ttk.Label(resultado_janela, text="Resultados da Previsão", font=("Helvetica", 14, "bold")).pack(pady=10)

        main_frame = Frame(resultado_janela)
        main_frame.pack(fill=BOTH, expand=True)

        frame_tabela = Frame(main_frame)
        frame_tabela.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        tabela = ttk.Treeview(frame_tabela, columns=("Modelo", "Previsão", "Fórmula"), show="headings")
        tabela.heading("Modelo", text="Modelo")
        tabela.heading("Previsão", text="Previsão (nível)")
        tabela.heading("Fórmula", text="Fórmula do Modelo")
        tabela.pack(fill=BOTH, expand=True)

        valores_histograma = []
        valores_para_media = {}

        formulas_modelos = get_modelo_eq()

        for modelo, previsao in resultados:
            modelo_normalizado = modelo.lower().replace(" ", "_")
            formula = formulas_modelos.get(modelo_normalizado, "Não disponível")
            tabela.insert("", "end", values=(modelo, f"{previsao:.2f}", formula))
            valores_histograma.append(previsao)
            valores_para_media[modelo_normalizado] = previsao

        tabela.insert("", "end", values=(" ", " "))
        try:
            media_ponderada = media_ponderada_modelos(valores_para_media)
            tabela.insert("", "end", values=("Média Ponderada (RMSE)", f"{media_ponderada:.2f}", "-"))
        except Exception as e:
            tabela.insert("", "end", values=("Erro ao calcular média", str(e), "-"))

        frame_grafico = Frame(main_frame)
        frame_grafico.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(5, 4))

        x = list(range(len(valores_histograma)))
        y = valores_histograma         

        ax.scatter(x, y, color='skyblue', edgecolor='black')
        ax.set_title('Dispersão das Previsões')
        ax.set_xlabel('Índice')
        ax.set_ylabel('Valor da Previsão')

        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)


    except ValueError:
        messagebox.showerror("Erro de entrada", "Por favor, insira apenas valores numéricos válidos.")

def mostrar_historico(root):
    if not historico_previsoes:
        messagebox.showinfo("Histórico vazio", "Nenhuma previsão foi realizada ainda.")
        return

    janela_hist = Toplevel(root)
    janela_hist.title("Histórico de Previsões")
    janela_hist.geometry("600x400")

    tree = ttk.Treeview(janela_hist, columns=("Entrada",), show="headings")
    tree.heading("Entrada", text="Entradas da Previsão")
    tree.pack(fill=BOTH, expand=True)

    for idx, item in enumerate(historico_previsoes):
        entrada_str = ", ".join([f"{k}={v:.2f}" for k, v in item["entrada"].items() if v is not None])
        tree.insert("", "end", iid=str(idx), values=(entrada_str,))

    def on_double_click(event):
        item_id = tree.focus()
        if item_id:
            idx = int(item_id)
            resultado = historico_previsoes[idx]["resultado"]
            entrada = historico_previsoes[idx]["entrada"]
            exibir_resultado(root, resultado, entrada)

    tree.bind("<Double-1>", on_double_click)

def exibir_resultado(root, resultados, dados):
    resultado_janela = Toplevel(root)
    resultado_janela.title("Resultados da Previsão")
    resultado_janela.geometry(f"{1000}x{500}+{(largura_tela // 2) - (1000 // 2)}+{(altura_tela // 2) - (500 // 2)}")

    ttk.Label(resultado_janela, text="Resultados da Previsão", font=("Helvetica", 14, "bold")).pack(pady=10)

    main_frame = Frame(resultado_janela)
    main_frame.pack(fill=BOTH, expand=True)

    frame_tabela = Frame(main_frame)
    frame_tabela.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    tabela = ttk.Treeview(frame_tabela, columns=("Modelo", "Previsão", "Fórmula"), show="headings")
    tabela.heading("Modelo", text="Modelo")
    tabela.heading("Previsão", text="Previsão (nível)")
    tabela.heading("Fórmula", text="Fórmula do Modelo")
    tabela.pack(fill=BOTH, expand=True)

    valores_histograma = []
    valores_para_media = {}

    formulas_modelos = get_modelo_eq()

    for modelo, previsao in resultados:
        modelo_normalizado = modelo.lower().replace(" ", "_")
        formula = formulas_modelos.get(modelo_normalizado, "Não disponível")
        tabela.insert("", "end", values=(modelo, f"{previsao:.2f}", formula))
        valores_histograma.append(previsao)
        valores_para_media[modelo_normalizado] = previsao

    tabela.insert("", "end", values=(" ", " "))
    try:
        media_ponderada = media_ponderada_modelos(valores_para_media)
        tabela.insert("", "end", values=("Média Ponderada (RMSE)", f"{media_ponderada:.2f}", "-"))
    except Exception as e:
        tabela.insert("", "end", values=("Erro ao calcular média", str(e), "-"))

    frame_grafico = Frame(main_frame)
    frame_grafico.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

    fig, ax = plt.subplots(figsize=(5, 4))
    x = list(range(len(valores_histograma)))
    y = valores_histograma

    ax.scatter(x, y, color='skyblue', edgecolor='black')
    ax.set_title('Dispersão das Previsões')
    ax.set_xlabel('Índice')
    ax.set_ylabel('Valor da Previsão')

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

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

validacao = root.register(somente_numeros)

frm = ttk.Frame(root, padding=20)
frm.pack(expand=True)

ttk.Label(frm, text="RiverLevelForecastRSL", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

frame_ituporanga = ttk.Frame(frm)
frame_ituporanga.grid(row=1, column=0, padx=20, sticky=N)

ttk.Label(frame_ituporanga, text="Ituporanga", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

ttk.Label(frame_ituporanga, text="Nível do rio:").grid(row=1, column=0, sticky=E, pady=5)
entry_nivel_ituporanga = ttk.Entry(frame_ituporanga, width=25, validate="key", validatecommand=(validacao, "%P"))
entry_nivel_ituporanga.grid(row=1, column=1, pady=5)

ttk.Label(frame_ituporanga, text="Chuva:").grid(row=2, column=0, sticky=E, pady=5)
entry_chuva_ituporanga = ttk.Entry(frame_ituporanga, width=25, validate="key", validatecommand=(validacao, "%P"))
entry_chuva_ituporanga.grid(row=2, column=1, pady=5)

frame_taio = ttk.Frame(frm)
frame_taio.grid(row=1, column=1, padx=20, sticky=N)

ttk.Label(frame_taio, text="Taió", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

ttk.Label(frame_taio, text="Nível do rio:").grid(row=1, column=0, sticky=E, pady=5)
entry_nivel_taio = ttk.Entry(frame_taio, width=25, validate="key", validatecommand=(validacao, "%P"))
entry_nivel_taio.grid(row=1, column=1, pady=5)

ttk.Label(frame_taio, text="Chuva:").grid(row=2, column=0, sticky=E, pady=5)
entry_chuva_taio = ttk.Entry(frame_taio, width=25, validate="key", validatecommand=(validacao, "%P"))
entry_chuva_taio.grid(row=2, column=1, pady=5)

ttk.Button(frm, text="Realizar previsão", command=realizar_previsao).grid(row=2, column=0, columnspan=2, pady=20)

ttk.Button(frm, text="Sair", command=root.destroy).grid(row=3, column=0, columnspan=2)

ttk.Button(frm, text="Histórico", command=lambda: mostrar_historico(root)).grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
