import random
import json
import csv
import os
import tkinter as tk
from tkinter import messagebox, ttk

# Arquivos de armazenamento
PROFESSORES_FILE = "professores.json"
DISCIPLINAS_FILE = "disciplinas.json"

# Estruturas de dados
professores = []
disciplinas = []

# Função para salvar os dados em arquivos JSON
def salvar_dados():
    with open(PROFESSORES_FILE, "w", encoding="utf-8") as f:
        json.dump(professores, f, indent=4, ensure_ascii=False)
    
    with open(DISCIPLINAS_FILE, "w", encoding="utf-8") as f:
        json.dump(disciplinas, f, indent=4, ensure_ascii=False)

# Função para carregar os dados ao iniciar o programa
def carregar_dados():
    global professores, disciplinas
    
    if os.path.exists(PROFESSORES_FILE):
        with open(PROFESSORES_FILE, "r", encoding="utf-8") as f:
            professores = json.load(f)

    if os.path.exists(DISCIPLINAS_FILE):
        with open(DISCIPLINAS_FILE, "r", encoding="utf-8") as f:
            disciplinas = json.load(f)

# Função para atualizar a tabela de professores
def atualizar_tabela_professores():
    for row in tree_professores.get_children():
        tree_professores.delete(row)

    for professor in professores:
        tree_professores.insert("", tk.END, values=(
            professor["nome"], professor["area_atuacao"], ", ".join(professor["disponibilidade"]), professor["modalidade"]
        ))

# Função para atualizar a tabela de disciplinas
def atualizar_tabela_disciplinas():
    for row in tree_disciplinas.get_children():
        tree_disciplinas.delete(row)

    for disciplina in disciplinas:
        tree_disciplinas.insert("", tk.END, values=(
            disciplina["nome"], disciplina["tipo"], "Sim" if disciplina["necessita_lab"] else "Não", disciplina["horario"], disciplina["professor"] or "Não alocado"
        ))

# Função para cadastrar professor
def cadastrar_professor():
    nome = entry_nome_professor.get()
    area = combo_area.get()
    modalidade = modalidade_professor.get()  # Pega o valor do botão de rádio selecionado


    # Capturar dias e horários selecionados
    dias_selecionados = [dia for dia, var in dias_vars.items() if var.get()]
    horarios_selecionados = [hora for hora, var in horarios_vars.items() if var.get()]

    if not nome or not area or not dias_selecionados or not horarios_selecionados or not modalidade:
        messagebox.showerror("Erro", "Preencha todos os campos e selecione pelo menos um dia e um horário!")
        return

    disponibilidade = [f"{dia} - {hora}" for dia in dias_selecionados for hora in horarios_selecionados]

    professor = {
        "nome": nome,
        "area_atuacao": area,
        "disponibilidade": disponibilidade,
        "modalidade": modalidade,
        "disciplinas_alocadas": []
    }
    professores.append(professor)
    salvar_dados()
    messagebox.showinfo("Sucesso", f"Professor {nome} cadastrado!")

    entry_nome_professor.delete(0, tk.END)

    # Resetar checkboxes de disponibilidade
    for var in dias_vars.values():
        var.set(False)
    for var in horarios_vars.values():
        var.set(False)

    atualizar_tabela_professores()


# Função para cadastrar disciplina
def cadastrar_disciplina():
    nome = entry_nome_disciplina.get()
    tipo = tipo_disciplina.get()  # Agora pegamos o valor do Radiobutton
    necessita_lab = var_lab.get()

    # Capturar dias e horários selecionados
    dias_selecionados = [dia for dia, var in dias_disc_vars.items() if var.get()]
    horarios_selecionados = [hora for hora, var in horarios_disc_vars.items() if var.get()]

    if not nome or not tipo or not dias_selecionados or not horarios_selecionados:
        messagebox.showerror("Erro", "Preencha todos os campos e selecione pelo menos um dia e um horário!")
        return

    disponibilidade_disciplina = [f"{dia} - {hora}" for dia in dias_selecionados for hora in horarios_selecionados]

    disciplina = {
        "nome": nome,
        "tipo": tipo,
        "necessita_lab": necessita_lab,
        "horario": ", ".join(disponibilidade_disciplina),  # Salva os horários como string separada por vírgula
        "professor": None
    }
    disciplinas.append(disciplina)
    salvar_dados()
    messagebox.showinfo("Sucesso", f"Disciplina {nome} cadastrada!")

    entry_nome_disciplina.delete(0, tk.END)

    # Resetar checkboxes de dias e horários
    for var in dias_disc_vars.values():
        var.set(False)
    for var in horarios_disc_vars.values():
        var.set(False)

    atualizar_tabela_disciplinas()


# Função para alocar professores corretamente
def alocar_professores():
    for disciplina in disciplinas:
        candidatos = [
            p for p in professores
            if disciplina["tipo"] in p["modalidade"]
            and disciplina["horario"] in p["disponibilidade"]
            and disciplina["nome"] not in p["disciplinas_alocadas"]
        ]

        if candidatos:
            professor_escolhido = random.choice(candidatos)
            disciplina["professor"] = professor_escolhido["nome"]
            professor_escolhido["disciplinas_alocadas"].append(disciplina["nome"])
        else:
            disciplina["professor"] = "Não alocado"
    
    salvar_dados()
    messagebox.showinfo("Alocação", "Professores alocados!")
    atualizar_tabela_disciplinas()
    
# Exportar para JSON
def exportar_json():
    with open("grade.json", "w", encoding="utf-8") as f:
        json.dump(disciplinas, f, indent=4, ensure_ascii=False)
    messagebox.showinfo("Exportação", "Grade exportada para 'grade.json'.")
    
# Exportar para CSV
def exportar_csv():
    with open("grade.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Disciplina", "Tipo", "Laboratório", "Horário", "Professor"])
        for disciplina in disciplinas:
            writer.writerow([
                disciplina["nome"], disciplina["tipo"], "Sim" if disciplina["necessita_lab"] else "Não",
                disciplina["horario"], disciplina["professor"]
            ])
    messagebox.showinfo("Exportação", "Grade exportada para 'grade.csv'.")

# Excluir Professor
def excluir_professor():
    selecionado = tree_professores.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um professor para excluir.")
        return

    for item in selecionado:
        nome_professor = tree_professores.item(item, "values")[0]
        professores[:] = [p for p in professores if p["nome"] != nome_professor]

    salvar_dados()
    atualizar_tabela_professores()

# Excluir Disciplina
def excluir_disciplina():
    selecionado = tree_disciplinas.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma disciplina para excluir.")
        return

    for item in selecionado:
        nome_disciplina = tree_disciplinas.item(item, "values")[0]
        disciplinas[:] = [d for d in disciplinas if d["nome"] != nome_disciplina]

    salvar_dados()
    atualizar_tabela_disciplinas()

# Editar Professor
def editar_professor():
    selecionado = tree_professores.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um professor para editar.")
        return

    item = selecionado[0]
    valores = tree_professores.item(item, "values")

    nome_antigo = valores[0]
    novo_nome = entry_nome_professor.get()
    nova_area = combo_area.get()
    nova_disponibilidade = entry_disponibilidade.get().split(", ")
    nova_modalidade = combo_modalidade.get()

    if not novo_nome or not nova_area or not nova_disponibilidade or not nova_modalidade:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    for professor in professores:
        if professor["nome"] == nome_antigo:
            professor["nome"] = novo_nome
            professor["area_atuacao"] = nova_area
            professor["disponibilidade"] = nova_disponibilidade
            professor["modalidade"] = nova_modalidade
            break

    salvar_dados()
    atualizar_tabela_professores()
    messagebox.showinfo("Sucesso", "Professor atualizado!")

# Editar Disciplina
def editar_disciplina():
    selecionado = tree_disciplinas.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma disciplina para editar.")
        return

    item = selecionado[0]
    valores = tree_disciplinas.item(item, "values")

    nome_antigo = valores[0]
    novo_nome = entry_nome_disciplina.get()
    novo_tipo = combo_tipo.get()
    novo_lab = var_lab.get()
    novo_horario = entry_horario.get()

    if not novo_nome or not novo_tipo or not novo_horario:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    for disciplina in disciplinas:
        if disciplina["nome"] == nome_antigo:
            disciplina["nome"] = novo_nome
            disciplina["tipo"] = novo_tipo
            disciplina["necessita_lab"] = novo_lab
            disciplina["horario"] = novo_horario
            break

    salvar_dados()
    atualizar_tabela_disciplinas()
    messagebox.showinfo("Sucesso", "Disciplina atualizada!")





# Criar interface gráfica
root = tk.Tk()
root.title("Gerenciamento de Professores e Disciplinas")
root.geometry("900x600")




# Botões principais ( Botões "Alocar Professores", "Exportar para JSON" e "Exportar para CSV" )
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10, anchor="w", fill="x")  # Alinha à esquerda

tk.Button(frame_botoes, text="Alocar Professores", command=alocar_professores).pack(side="left", padx=10)
tk.Button(frame_botoes, text="Exportar para JSON", command=exportar_json).pack(side="left", padx=10)
tk.Button(frame_botoes, text="Exportar para CSV", command=exportar_csv).pack(side="left", padx=10)




# Aba de Professores ( CADASTRAR PROFESSOR (NOME, AREA, DISPONIBILIDADE, MODALIDADE))
frame_professor = tk.LabelFrame(root, text="Cadastrar Professor")
frame_professor.pack(pady=10, fill="x")

# Frame para nome e área
frame_info_basica = tk.Frame(frame_professor)
frame_info_basica.pack(fill="x", padx=5, pady=5)

tk.Label(frame_info_basica, text="Nome:").pack(side="left", padx=5)
entry_nome_professor = tk.Entry(frame_info_basica)
entry_nome_professor.pack(side="left", padx=5)

tk.Label(frame_info_basica, text="Área:").pack(side="left", padx=5)
combo_area = ttk.Combobox(frame_info_basica, values=["desenvolvimento", "infra", "ambos"])
combo_area.pack(side="left", padx=5)

# Frame para dias
frame_dias = tk.Frame(frame_professor)
frame_dias.pack(fill="x", padx=5, pady=5)

tk.Label(frame_dias, text="Dias:").pack(anchor="w", padx=5)
dias_container = tk.Frame(frame_dias)
dias_container.pack(fill="x")

dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
dias_vars = {dia: tk.BooleanVar() for dia in dias_semana}

for dia in dias_semana:
    tk.Checkbutton(dias_container, text=dia, variable=dias_vars[dia]).pack(side="left")

# Frame para horários e modalidade (lado a lado)
frame_horarios_modalidade = tk.Frame(frame_professor)
frame_horarios_modalidade.pack(fill="x", padx=5, pady=5)

# Frame para horários (lado esquerdo)
frame_horarios = tk.Frame(frame_horarios_modalidade)
frame_horarios.pack(side="left", fill="x", expand=True)

tk.Label(frame_horarios, text="Horários:").pack(anchor="w", padx=5)
horarios_container = tk.Frame(frame_horarios)
horarios_container.pack(fill="x")

horarios_disponiveis = ["18h", "19h", "20h", "21h"]
horarios_vars = {hora: tk.BooleanVar() for hora in horarios_disponiveis}

for hora in horarios_disponiveis:
    tk.Checkbutton(horarios_container, text=hora, variable=horarios_vars[hora]).pack(side="left")

# Frame para modalidade (lado direito)
frame_modalidade = tk.Frame(frame_horarios_modalidade)
frame_modalidade.pack(side="left", fill="x", expand=True)

tk.Label(frame_modalidade, text="Modalidade:").pack(anchor="w", padx=5)
modalidades_container = tk.Frame(frame_modalidade)
modalidades_container.pack(fill="x")

modalidade_professor = tk.StringVar(value="presencial")
modalidades = ["presencial", "ead", "híbrido"]

for mod in modalidades:
    tk.Radiobutton(modalidades_container, text=mod.capitalize(), variable=modalidade_professor, value=mod).pack(side="left", padx=5)

# Frame para botão de cadastro
frame_botao = tk.Frame(frame_professor)
frame_botao.pack(fill="x", padx=5, pady=5)
tk.Button(frame_botao, text="Cadastrar", command=cadastrar_professor).pack(side="left", padx=5)



# Tabela de Professores (PROFESSORES CADASTRADOS)
frame_lista_professores = tk.LabelFrame(root, text="Professores Cadastrados")
frame_lista_professores.pack(pady=10, fill="both", expand=True)

tree_professores = ttk.Treeview(frame_lista_professores, columns=("Nome", "Área", "Disponibilidade", "Modalidade"), show="headings")
for col in ("Nome", "Área", "Disponibilidade", "Modalidade"):
    tree_professores.heading(col, text=col)
tree_professores.pack(fill="both", expand=True)
tk.Button(frame_lista_professores, text="Excluir Professor", command=excluir_professor).pack(side="left", padx=5)
tk.Button(frame_lista_professores, text="Editar Professor", command=editar_professor).pack(side="left", padx=5)





# Aba de Disciplinas (CADASTRAR DISCIPLINA (NOME, TIPO, LAB, HORARIO))
frame_disciplina = tk.LabelFrame(root, text="Cadastrar Disciplina")
frame_disciplina.pack(pady=10, fill="x")

# Frame para informações básicas
frame_info_disc = tk.Frame(frame_disciplina)
frame_info_disc.pack(fill="x", padx=5, pady=5)

tk.Label(frame_info_disc, text="Nome:").pack(side="left", padx=5)
entry_nome_disciplina = tk.Entry(frame_info_disc)
entry_nome_disciplina.pack(side="left", padx=5)

var_lab = tk.BooleanVar()
tk.Checkbutton(frame_info_disc, text="Necessita Lab?", variable=var_lab).pack(side="left", padx=5)

# Frame para dias
frame_dias_disc = tk.Frame(frame_disciplina)
frame_dias_disc.pack(fill="x", padx=5, pady=5)

tk.Label(frame_dias_disc, text="Dias:").pack(anchor="w", padx=5)
dias_disc_container = tk.Frame(frame_dias_disc)
dias_disc_container.pack(fill="x")

dias_semana_disciplina = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
dias_disc_vars = {dia: tk.BooleanVar() for dia in dias_semana_disciplina}

for dia in dias_semana_disciplina:
    tk.Checkbutton(dias_disc_container, text=dia, variable=dias_disc_vars[dia]).pack(side="left")

# Frame para horários e tipo (lado a lado)
frame_horarios_tipo = tk.Frame(frame_disciplina)
frame_horarios_tipo.pack(fill="x", padx=5, pady=5)

# Frame para horários (lado esquerdo)
frame_horarios_disc = tk.Frame(frame_horarios_tipo)
frame_horarios_disc.pack(side="left", fill="x", expand=True)

tk.Label(frame_horarios_disc, text="Horários:").pack(anchor="w", padx=5)
horarios_disc_container = tk.Frame(frame_horarios_disc)
horarios_disc_container.pack(fill="x")

horarios_disciplinas = ["18h", "19h", "20h", "21h"]
horarios_disc_vars = {hora: tk.BooleanVar() for hora in horarios_disciplinas}

for hora in horarios_disciplinas:
    tk.Checkbutton(horarios_disc_container, text=hora, variable=horarios_disc_vars[hora]).pack(side="left")

# Frame para tipo de disciplina (lado direito)
frame_tipo_disc = tk.Frame(frame_horarios_tipo)
frame_tipo_disc.pack(side="left", fill="x", expand=True)

tk.Label(frame_tipo_disc, text="Tipo:").pack(anchor="w", padx=5)
tipos_container = tk.Frame(frame_tipo_disc)
tipos_container.pack(fill="x")

tipo_disciplina = tk.StringVar(value="presencial")
tipos_opcoes = ["presencial", "ead", "híbrido"]

for tipo in tipos_opcoes:
    tk.Radiobutton(tipos_container, text=tipo.capitalize(), variable=tipo_disciplina, value=tipo).pack(side="left", padx=5)

# Frame para botão de cadastro
frame_botao_disc = tk.Frame(frame_disciplina)
frame_botao_disc.pack(fill="x", padx=5, pady=5)
tk.Button(frame_botao_disc, text="Cadastrar", command=cadastrar_disciplina).pack(side="left", padx=5)






# Tabela de Disciplinas (DISCIPLINAS CADASTRADAS)
frame_lista_disciplinas = tk.LabelFrame(root, text="Disciplinas Cadastradas")
frame_lista_disciplinas.pack(pady=10, fill="both", expand=True)

tree_disciplinas = ttk.Treeview(frame_lista_disciplinas, columns=("Nome", "Tipo", "Laboratório", "Horário", "Professor"), show="headings")
for col in ("Nome", "Tipo", "Laboratório", "Horário", "Professor"):
    tree_disciplinas.heading(col, text=col)
tree_disciplinas.pack(fill="both", expand=True)
tk.Button(frame_lista_disciplinas, text="Excluir Disciplina", command=excluir_disciplina).pack(side="left", padx=5)
tk.Button(frame_lista_disciplinas, text="Editar Disciplina", command=editar_disciplina).pack(side="left", padx=5)




# Carregar os dados ao iniciar
carregar_dados()
atualizar_tabela_professores()
atualizar_tabela_disciplinas()



# Rodar a aplicação
root.mainloop()