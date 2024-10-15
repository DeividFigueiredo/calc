import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

# Função para calcular o total e aplicar o desconto
def calcular_total():
    try:
        em_aberto = int(entry_em_aberto.get())  # Quantidade de mensalidades em aberto
        valor_total = 0

        for entry in entry_mensalidades:  # Somar o valor das mensalidades
            valor_mensalidade = float(entry.get())
            valor_total += valor_mensalidade
        
        desconto = int(entry_desconto.get())
        desconto = 100 - desconto
        desconto_percent = desconto / 100
        valor_com_desconto = valor_total * desconto_percent

        label_resultado.config(text=f"Valor total com desconto: R$ {valor_com_desconto:.2f}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para validar as parcelas
def validar_parcelas():
    try:
        quant_parcelas = int(entry_parcelas.get())
        valor_com_desconto = float(label_resultado.cget("text").split(": R$ ")[1])

        if quant_parcelas >= 8:
            messagebox.showerror("Erro", "Quantidade inválida de parcelas (máx 7)")
        else:
            valor_parcela = valor_com_desconto / quant_parcelas
            label_parcelas_result.config(text=f"Acordo: {quant_parcelas}x de R$ {valor_parcela:.2f}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para gerar caixas de entrada para os valores das mensalidades
def gerar_campos_mensalidades():
    try:
        em_aberto = int(entry_em_aberto.get())
        for widget in frame_mensalidades.winfo_children():
            widget.destroy()  # Limpar os campos anteriores
        global entry_mensalidades
        entry_mensalidades = []

        for i in range(em_aberto):
            label_mensalidade = tk.Label(frame_mensalidades, text=f"Mensalidade {i+1} (R$):", font=label_font, bg="#f0f0f0")
            label_mensalidade.pack(pady=5)
            entry_mensalidade = tk.Entry(frame_mensalidades, font=entry_font, width=20)
            entry_mensalidade.pack(pady=5)
            entry_mensalidades.append(entry_mensalidade)
        
        button_calcular.pack(pady=15)  # Colocar o botão calcular depois das mensalidades
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira uma quantidade válida de mensalidades.")

# Função para gerar a notinha (arquivo .txt)
def gerar_nota():
    try:
        valor_com_desconto = float(label_resultado.cget("text").split(": R$ ")[1])
        quant_parcelas = int(entry_parcelas.get())
        valor_parcela = valor_com_desconto / quant_parcelas

        # Pegar valores das mensalidades
        valores_mensalidades = [float(entry.get()) for entry in entry_mensalidades]

        # Criar conteúdo da notinha
        nota = f"--- Notinha para o Cliente ---\n\n"
        nota += f"Mensalidades em aberto: {len(valores_mensalidades)}\n"
        for i, valor in enumerate(valores_mensalidades, 1):
            nota += f"  Mensalidade {i}: R$ {valor:.2f}\n"
        
        nota += f"\nDesconto aplicado: {entry_desconto.get()}%\n"
        nota += f"Valor total com desconto: R$ {valor_com_desconto:.2f}\n"
        nota += f"Acordo de pagamento: {quant_parcelas}x de R$ {valor_parcela:.2f}\n"

        # Escolher local para salvar a notinha
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(nota)
            messagebox.showinfo("Sucesso", "Notinha salva com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, finalize o cálculo antes de gerar a notinha.")

# Criação da janela
root = tk.Tk()
root.title("Cálculo de Desconto e Parcelamento")

# Ajustando o tamanho da janela
root.geometry("400x600")
root.configure(bg="#f0f0f0")  # Cor de fundo

# Estilos
label_font = ("Arial", 14)
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Adicionando o Frame com Scrollbar para as mensalidades
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Widgets
label_em_aberto = tk.Label(scrollable_frame, text="Quantidade de Mensalidades em Aberto:", font=label_font, bg="#f0f0f0")
label_em_aberto.pack(pady=10)

entry_em_aberto = tk.Entry(scrollable_frame, font=entry_font, width=20)
entry_em_aberto.pack(pady=5)

button_gerar_campos = tk.Button(scrollable_frame, text="Inserir Mensalidades", font=button_font, bg="#4CAF50", fg="white", command=gerar_campos_mensalidades)
button_gerar_campos.pack(pady=15)

# Frame para os campos das mensalidades
frame_mensalidades = tk.Frame(scrollable_frame, bg="#f0f0f0")
frame_mensalidades.pack(pady=10)

label_desconto = tk.Label(scrollable_frame, text="Desconto (%):", font=label_font, bg="#f0f0f0")
label_desconto.pack(pady=10)

entry_desconto = tk.Entry(scrollable_frame, font=entry_font, width=20)
entry_desconto.pack(pady=5)

# Colocando o botão "Calcular Desconto" logo abaixo do campo de desconto
button_calcular = tk.Button(scrollable_frame, text="Calcular Desconto", font=button_font, bg="#4CAF50", fg="white", command=calcular_total)
button_calcular.pack(pady=15)

# Label para mostrar o resultado
label_resultado = tk.Label(scrollable_frame, text="Valor total com desconto: R$ 0.00", font=label_font, bg="#f0f0f0")
label_resultado.pack(pady=10)



label_parcelas = tk.Label(scrollable_frame, text="Parcelas (máximo 7):", font=label_font, bg="#f0f0f0")
label_parcelas.pack(pady=10)

entry_parcelas = tk.Entry(scrollable_frame, font=entry_font, width=20)
entry_parcelas.pack(pady=5)

button_validar = tk.Button(scrollable_frame, text="Validar Parcelas", font=button_font, bg="#2196F3", fg="white", command=validar_parcelas)
button_validar.pack(pady=15)

label_parcelas_result = tk.Label(scrollable_frame, text="", font=label_font, bg="#f0f0f0")
label_parcelas_result.pack(pady=10)

# Botão para gerar notinha
button_gerar_nota = tk.Button(scrollable_frame, text="Gerar Notinha", font=button_font, bg="#FFC107", fg="black", command=gerar_nota)
button_gerar_nota.pack(pady=20)

# Scrollbar positioning
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Execução da interface
root.mainloop()
