"""
Sistema de Alocação de Professores
================================

Este módulo implementa um sistema de gerenciamento e alocação de professores em disciplinas
usando interface gráfica Tkinter. O sistema permite cadastrar professores e disciplinas,
gerenciar suas informações e realizar alocações automáticas considerando diversos critérios.

Funcionalidades principais:
-------------------------
- Cadastro e gerenciamento de professores
- Cadastro e gerenciamento de disciplinas
- Alocação automática baseada em critérios
- Exportação de dados em JSON e CSV
- Interface gráfica intuitiva

Classes:
-------
DropdownFrame: Implementa um dropdown customizado que expande ao clicar

Funções principais:
-----------------
cadastrar_professor(): Cadastra um novo professor no sistema
cadastrar_disciplina(): Cadastra uma nova disciplina no sistema
alocar_professores(): Realiza a alocação automática de professores às disciplinas
salvar_dados(): Persiste os dados em arquivos JSON
carregar_dados(): Carrega os dados dos arquivos JSON

Autor: Seu Nome
Data: Janeiro 2024
Versão: 1.0
"""

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

# Constantes
AREAS_ATUACAO = [
    "desenvolvimento web",
    "desenvolvimento mobile",
    "desenvolvimento de jogos",
    "desenvolvimento desktop",
    "infraestrutura de redes",
    "infraestrutura cloud",
    "segurança da informação",
    "banco de dados",
    "inteligência artificial",
    "machine learning",
    "computação gráfica",
    "engenharia de software",
    "sistemas distribuídos",
    "arquitetura de software",
    "devops",
    "análise de dados",
    "big data",
    "iot",
    "blockchain",
    "realidade virtual/aumentada"
]

# Função para salvar os dados em arquivos JSON
def salvar_dados():
    with open(PROFESSORES_FILE, "w", encoding="utf-8") as f:
        json.dump(professores, f, indent=4, ensure_ascii=False)
    
    with open(DISCIPLINAS_FILE, "w", encoding="utf-8") as f:
        json.dump(disciplinas, f, indent=4, ensure_ascii=False)
    
    # Atualizar as tabelas após salvar
    atualizar_tabela_professores()
    atualizar_tabela_disciplinas()

# Função para carregar os dados ao iniciar o programa
def carregar_dados():
    global professores, disciplinas
    
    if os.path.exists(PROFESSORES_FILE):
        with open(PROFESSORES_FILE, "r", encoding="utf-8") as f:
            professores = json.load(f)

    if os.path.exists(DISCIPLINAS_FILE):
        with open(DISCIPLINAS_FILE, "r", encoding="utf-8") as f:
            disciplinas = json.load(f)
            # Atualizar disciplinas antigas que não têm a chave 'predio'
            for disciplina in disciplinas:
                if "predio" not in disciplina:
                    disciplina["predio"] = None
        # Salvar as disciplinas atualizadas
        with open(DISCIPLINAS_FILE, "w", encoding="utf-8") as f:
            json.dump(disciplinas, f, indent=4, ensure_ascii=False)

# Função para atualizar a tabela de professores
def atualizar_tabela_professores():
    # Limpar tabela atual
    for item in tree_professores.get_children():
        tree_professores.delete(item)
    
    # Carregar dados atualizados
    with open(PROFESSORES_FILE, 'r', encoding='utf-8') as file:
        professores = json.load(file)
    
    # Inserir dados na tabela
    for professor in professores:
        disponibilidade = ", ".join(professor["disponibilidade"]) if professor["disponibilidade"] else "Não definido"
        tree_professores.insert("", "end", values=(
            professor["nome"],
            professor["area_atuacao"],
            professor["modalidade"],
            disponibilidade
        ))

# Função para atualizar a tabela de disciplinas
def atualizar_tabela_disciplinas():
    # Limpar tabela atual
    for item in tree_disciplinas.get_children():
        tree_disciplinas.delete(item)
    
    # Carregar dados atualizados
    with open(DISCIPLINAS_FILE, 'r', encoding='utf-8') as file:
        disciplinas = json.load(file)
    
    # Inserir dados na tabela
    for disciplina in disciplinas:
        lab_info = f"Sim (Prédio {disciplina.get('predio', 'N/A')})" if disciplina["necessita_lab"] else "Não"
        tree_disciplinas.insert("", "end", values=(
            disciplina["nome"],
            disciplina["tipo"],
            lab_info,
            disciplina["horario"] if "horario" in disciplina else "Não definido",
            disciplina.get("professor_alocado", "Não alocado")
        ))

# Função para contar uso dos prédios
def contar_uso_predios():
    predio1 = sum(1 for d in disciplinas if d.get("predio") == "1")
    predio2 = sum(1 for d in disciplinas if d.get("predio") == "2")
    return {"1": predio1, "2": predio2}

class DropdownFrame:
    def __init__(self, parent, title, options, is_checkbutton=True):
        self.frame = tk.Frame(parent)
        self.frame.pack(side="left", padx=5)
        
        # Frame principal que contém apenas o botão
        self.main_frame = tk.Frame(self.frame)
        self.main_frame.pack(fill="x")
        
        # Botão que mostra/esconde as opções
        self.button = tk.Button(self.main_frame, text=title, command=self.toggle)
        self.button.pack(fill="x")
        
        # Criar o popup (inicialmente escondido)
        self.popup = tk.Toplevel(self.frame)
        self.popup.withdraw()  # Esconder inicialmente
        self.popup.overrideredirect(True)  # Remover decorações da janela
        
        # Frame para as opções dentro do popup
        self.content = tk.Frame(self.popup, relief="solid", borderwidth=1)
        self.content.pack(fill="both", expand=True)
        
        # Variáveis para armazenar as seleções
        if is_checkbutton:
            self.vars = {opt: tk.BooleanVar() for opt in options}
            for opt in options:
                tk.Checkbutton(self.content, text=opt, variable=self.vars[opt]).pack(anchor="w", padx=5, pady=2)
        else:
            self.var = tk.StringVar(value=options[0])
            for opt in options:
                tk.Radiobutton(self.content, text=opt.capitalize(), 
                             variable=self.var, value=opt).pack(anchor="w", padx=5, pady=2)
        
        # Adicionar botão de fechar no popup
        tk.Button(self.content, text="✓", command=self.hide_popup).pack(pady=5)
        
        self.is_visible = False
    
    def toggle(self):
        if not self.is_visible:
            self.show_popup()
        else:
            self.hide_popup()
    
    def show_popup(self):
        # Posicionar o popup abaixo do botão
        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + self.button.winfo_height()
        
        self.popup.geometry(f"+{x}+{y}")
        self.popup.deiconify()
        self.is_visible = True
        
        # Vincular evento de clique fora para fechar o popup
        self.popup.bind('<FocusOut>', lambda e: self.hide_popup())
    
    def hide_popup(self):
        self.popup.withdraw()
        self.is_visible = False
    
    def get_selected(self):
        if hasattr(self, 'vars'):  # Checkbuttons
            return [opt for opt, var in self.vars.items() if var.get()]
        else:  # Radiobuttons
            return self.var.get()
    
    def clear_selection(self):
        if hasattr(self, 'vars'):  # Checkbuttons
            for var in self.vars.values():
                var.set(False)
        else:  # Radiobuttons
            self.var.set(self.var._values[0])

# Função para cadastrar professor
def cadastrar_professor():
    nome = entry_nome_professor.get()
    area = combo_area.get()
    dias_selecionados = dias_dropdown.get_selected()
    horarios_selecionados = horarios_dropdown.get_selected()
    modalidade = modalidade_dropdown.get_selected()

    if not nome or not area or not dias_selecionados or not horarios_selecionados or not modalidade:
        messagebox.showerror("Erro", "Preencha todos os campos e selecione pelo menos um dia e um horário!")
        return

    disponibilidade = [f"{dia} - {hora}" for dia in dias_selecionados 
                      for hora in horarios_selecionados]

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
    combo_area.set("")
    dias_dropdown.clear_selection()
    horarios_dropdown.clear_selection()
    modalidade_dropdown.clear_selection()

    atualizar_tabela_professores()

# Função para cadastrar disciplina
def cadastrar_disciplina():
    nome = entry_nome_disciplina.get()
    tipo = tipo_dropdown.get_selected()
    necessita_lab = var_lab.get()
    dias_selecionados = dias_disc_dropdown.get_selected()
    horarios_selecionados = horarios_disc_dropdown.get_selected()
    
    # Alocar prédio automaticamente se necessitar de laboratório
    predio = None
    if necessita_lab:
        uso_predios = contar_uso_predios()
        predio = "1" if uso_predios["1"] <= uso_predios["2"] else "2"

    if not nome or not tipo or not dias_selecionados or not horarios_selecionados:
        messagebox.showerror("Erro", "Preencha todos os campos e selecione pelo menos um dia e um horário!")
        return

    disponibilidade_disciplina = [f"{dia} - {hora}" for dia in dias_selecionados 
                                for hora in horarios_selecionados]

    disciplina = {
        "nome": nome,
        "tipo": tipo,
        "necessita_lab": necessita_lab,
        "predio": predio,
        "horario": ", ".join(disponibilidade_disciplina),
        "professor_alocado": None
    }
    disciplinas.append(disciplina)
    salvar_dados()
    messagebox.showinfo("Sucesso", f"Disciplina {nome} cadastrada!" + 
                       (f"\nAlocada ao Prédio {predio}" if necessita_lab else ""))

    entry_nome_disciplina.delete(0, tk.END)
    var_lab.set(False)
    dias_disc_dropdown.clear_selection()
    horarios_disc_dropdown.clear_selection()
    tipo_dropdown.clear_selection()

    atualizar_tabela_disciplinas()

# Função para alocar professores corretamente
def alocar_professores():
    # Limpar alocações anteriores
    for professor in professores:
        professor["disciplinas_alocadas"] = []
    for disciplina in disciplinas:
        disciplina["professor_alocado"] = None

    # Alocar professores
    for disciplina in disciplinas:
        candidatos = [
            p for p in professores
            if p["modalidade"] == disciplina["tipo"]  # Modalidade deve ser compatível
            and all(horario in p["disponibilidade"] for horario in disciplina["horario"].split(", "))  # Todos os horários devem ser compatíveis
            and len(p["disciplinas_alocadas"]) < 4  # Máximo de 4 disciplinas por professor
        ]

        if candidatos:
            # Ordenar candidatos por número de disciplinas alocadas (menos disciplinas primeiro)
            candidatos.sort(key=lambda p: len(p["disciplinas_alocadas"]))
            professor_escolhido = candidatos[0]
            disciplina["professor_alocado"] = professor_escolhido["nome"]
            professor_escolhido["disciplinas_alocadas"].append(disciplina["nome"])
        else:
            disciplina["professor_alocado"] = "Não alocado"
    
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
                disciplina["horario"], disciplina["professor_alocado"]
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
    
    # Criar janela de edição
    janela_edicao = tk.Toplevel(root)
    janela_edicao.title("Editar Professor")
    janela_edicao.geometry("600x400")
    
    # Frame para todas as informações
    info_frame = tk.Frame(janela_edicao)
    info_frame.pack(fill="x", padx=5, pady=5)

    # Frame para nome e área (lado esquerdo)
    dados_frame = tk.Frame(info_frame)
    dados_frame.pack(side="left", fill="x")

    tk.Label(dados_frame, text="Nome:").pack(side="left", padx=5)
    entry_nome = tk.Entry(dados_frame, width=20)
    entry_nome.insert(0, valores[0])
    entry_nome.pack(side="left", padx=5)

    tk.Label(dados_frame, text="Área:").pack(side="left", padx=5)
    combo_area_edit = ttk.Combobox(dados_frame, values=AREAS_ATUACAO, width=25)
    combo_area_edit.set(valores[1])
    combo_area_edit.pack(side="left", padx=5)

    # Modalidade
    tk.Label(info_frame, text="Modalidade:").pack(pady=5)
    modalidade_var = tk.StringVar(value=valores[2])
    for mod in ["presencial", "ead", "híbrido"]:
        tk.Radiobutton(info_frame, text=mod.capitalize(), variable=modalidade_var, value=mod).pack()
    
    # Disponibilidade
    tk.Label(info_frame, text="Disponibilidade (formato: Dia - Hora, ...):").pack(pady=5)
    entry_disp = tk.Entry(info_frame, width=40)
    entry_disp.insert(0, valores[3])
    entry_disp.pack(pady=5)
    
    def salvar_edicao():
        nome_antigo = valores[0]
        novo_nome = entry_nome.get()
        nova_area = combo_area_edit.get()
        nova_modalidade = modalidade_var.get()
        nova_disponibilidade = entry_disp.get().split(", ")

        if not novo_nome or not nova_area or not nova_modalidade or not nova_disponibilidade:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        for professor in professores:
            if professor["nome"] == nome_antigo:
                professor["nome"] = novo_nome
                professor["area_atuacao"] = nova_area
                professor["modalidade"] = nova_modalidade
                professor["disponibilidade"] = nova_disponibilidade
                break
        
        salvar_dados()
        atualizar_tabela_professores()
        janela_edicao.destroy()
        messagebox.showinfo("Sucesso", "Professor atualizado com sucesso!")
    
    tk.Button(janela_edicao, text="Salvar", command=salvar_edicao).pack(pady=20)

# Editar Disciplina
def editar_disciplina():
    selecionado = tree_disciplinas.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma disciplina para editar.")
        return

    item = selecionado[0]
    valores = tree_disciplinas.item(item, "values")
    
    # Criar janela de edição
    janela_edicao = tk.Toplevel(root)
    janela_edicao.title("Editar Disciplina")
    janela_edicao.geometry("600x400")
    
    # Frame para todas as informações da disciplina
    info_disc_frame = tk.Frame(janela_edicao)
    info_disc_frame.pack(fill="x", padx=5, pady=5)

    # Frame para nome e laboratório (lado esquerdo)
    dados_disc_frame = tk.Frame(info_disc_frame)
    dados_disc_frame.pack(side="left", fill="x")

    tk.Label(dados_disc_frame, text="Nome:").pack(side="left", padx=5)
    entry_nome = tk.Entry(dados_disc_frame, width=20)
    entry_nome.insert(0, valores[0])
    entry_nome.pack(side="left", padx=5)

    # Tipo
    tk.Label(info_disc_frame, text="Tipo:").pack(pady=5)
    tipo_var = tk.StringVar(value=valores[1])
    for tipo in ["presencial", "ead", "híbrido"]:
        tk.Radiobutton(info_disc_frame, text=tipo.capitalize(), variable=tipo_var, value=tipo).pack()
    
    # Laboratório
    lab_frame = tk.Frame(info_disc_frame)
    lab_frame.pack(pady=5)
    
    lab_var = tk.BooleanVar(value="Sim" in valores[2])
    tk.Checkbutton(lab_frame, text="Necessita Laboratório", variable=lab_var).pack(side="left")
    
    # Prédio (somente informativo)
    if "Prédio" in valores[2]:
        predio_atual = valores[2].split("Prédio")[1].strip("() ")
        tk.Label(lab_frame, text=f"Prédio atual: {predio_atual}").pack(side="left", padx=5)
    
    # Horário
    tk.Label(info_disc_frame, text="Horário (formato: Dia - Hora, ...):").pack(pady=5)
    entry_horario = tk.Entry(info_disc_frame, width=40)
    entry_horario.insert(0, valores[3])
    entry_horario.pack(pady=5)
    
    def salvar_edicao():
        nome_antigo = valores[0]
        novo_nome = entry_nome.get()
        novo_tipo = tipo_var.get()
        necessita_lab_novo = lab_var.get()
        novo_horario = entry_horario.get()

        if not novo_nome or not novo_tipo or not novo_horario:
            messagebox.showerror("Erro", "Nome, tipo e horário são obrigatórios!")
            return
        
        # Se mudou para necessitar lab, alocar prédio automaticamente
        predio_novo = None
        if necessita_lab_novo:
            if "Prédio" in valores[2]:  # Manter o mesmo prédio se já tinha
                predio_novo = valores[2].split("Prédio")[1].strip("() ")
            else:  # Alocar novo prédio
                uso_predios = contar_uso_predios()
                predio_novo = "1" if uso_predios["1"] <= uso_predios["2"] else "2"
        
        for disciplina in disciplinas:
            if disciplina["nome"] == nome_antigo:
                disciplina["nome"] = novo_nome
                disciplina["tipo"] = novo_tipo
                disciplina["necessita_lab"] = necessita_lab_novo
                disciplina["predio"] = predio_novo
                disciplina["horario"] = novo_horario
                break
        
        salvar_dados()
        atualizar_tabela_disciplinas()
        janela_edicao.destroy()
        mensagem = "Disciplina atualizada com sucesso!"
        if necessita_lab_novo and predio_novo:
            mensagem += f"\nAlocada ao Prédio {predio_novo}"
        messagebox.showinfo("Sucesso", mensagem)
    
    tk.Button(janela_edicao, text="Salvar", command=salvar_edicao).pack(pady=20)

# Funções para atualizar labels de seleção
def atualizar_label_dias(label, vars_dict):
    selecionados = [dia for dia, var in vars_dict.items() if var.get()]
    texto = ", ".join(selecionados) if selecionados else "Nenhum dia selecionado"
    label.config(text=texto)

def atualizar_label_horarios(label, vars_dict):
    selecionados = [hora for hora, var in vars_dict.items() if var.get()]
    texto = ", ".join(selecionados) if selecionados else "Nenhum horário selecionado"
    label.config(text=texto)

def atualizar_label_modalidade(label, var):
    texto = var.get().capitalize() if var.get() else "Nenhuma modalidade selecionada"
    label.config(text=texto)

def atualizar_label_info_professor(label, nome, area):
    if nome and area:
        texto = f"Nome: {nome}\nÁrea: {area}"
    else:
        texto = "Nenhuma informação definida"
    label.config(text=texto)

def atualizar_label_info_disciplina(label, nome, necessita_lab):
    texto = f"Nome: {nome}\nNecessita Laboratório: {'Sim' if necessita_lab else 'Não'}"
    label.config(text=texto)

def abrir_dialogo_dias(parent, vars_dict, title="Selecionar Dias", label=None):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("200x250")
    dialog.transient(parent)
    dialog.grab_set()
    
    for dia, var in vars_dict.items():
        tk.Checkbutton(dialog, text=dia, variable=var).pack(anchor="w", padx=10, pady=5)
    
    def confirmar():
        if label:
            atualizar_label_dias(label, vars_dict)
        dialog.destroy()
    
    tk.Button(dialog, text="Confirmar", command=confirmar).pack(pady=10)

def abrir_dialogo_horarios(parent, vars_dict, title="Selecionar Horários", label=None):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("200x200")
    dialog.transient(parent)
    dialog.grab_set()
    
    for hora, var in vars_dict.items():
        tk.Checkbutton(dialog, text=hora, variable=var).pack(anchor="w", padx=10, pady=5)
    
    def confirmar():
        if label:
            atualizar_label_horarios(label, vars_dict)
        dialog.destroy()
    
    tk.Button(dialog, text="Confirmar", command=confirmar).pack(pady=10)

def abrir_dialogo_modalidade(parent, var, opcoes, title="Selecionar Modalidade", label=None):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("200x200")
    dialog.transient(parent)
    dialog.grab_set()
    
    for opcao in opcoes:
        tk.Radiobutton(dialog, text=opcao.capitalize(), variable=var, value=opcao).pack(anchor="w", padx=10, pady=5)
    
    def confirmar():
        if label:
            atualizar_label_modalidade(label, var)
        dialog.destroy()
    
    tk.Button(dialog, text="Confirmar", command=confirmar).pack(pady=10)

def abrir_dialogo_info_professor(parent, entry_nome, combo_area, label):
    dialog = tk.Toplevel(parent)
    dialog.title("Informações do Professor")
    dialog.geometry("400x200")
    dialog.transient(parent)
    dialog.grab_set()
    
    # Frame para nome
    frame_nome = tk.Frame(dialog)
    frame_nome.pack(pady=5, fill="x", padx=10)
    tk.Label(frame_nome, text="Nome:").pack(side="left", padx=5)
    entry_nome_temp = tk.Entry(frame_nome)
    entry_nome_temp.insert(0, entry_nome.get())
    entry_nome_temp.pack(side="left", expand=True, fill="x", padx=5)
    
    # Frame para área
    frame_area = tk.Frame(dialog)
    frame_area.pack(pady=5, fill="x", padx=10)
    tk.Label(frame_area, text="Área:").pack(side="left", padx=5)
    combo_area_temp = ttk.Combobox(frame_area, values=AREAS_ATUACAO)
    combo_area_temp.set(combo_area.get())
    combo_area_temp.pack(side="left", expand=True, fill="x", padx=5)
    
    def confirmar():
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, entry_nome_temp.get())
        combo_area.set(combo_area_temp.get())
        atualizar_label_info_professor(label, entry_nome_temp.get(), combo_area_temp.get())
        dialog.destroy()
    
    tk.Button(dialog, text="Confirmar", command=confirmar).pack(pady=20)

def abrir_dialogo_info_disciplina(parent, entry_nome, var_lab, label):
    dialog = tk.Toplevel(parent)
    dialog.title("Informações da Disciplina")
    dialog.geometry("400x200")
    dialog.transient(parent)
    dialog.grab_set()
    
    # Frame para nome
    frame_nome = tk.Frame(dialog)
    frame_nome.pack(pady=5, fill="x", padx=10)
    tk.Label(frame_nome, text="Nome:").pack(side="left", padx=5)
    entry_nome_temp = tk.Entry(frame_nome)
    entry_nome_temp.insert(0, entry_nome.get())
    entry_nome_temp.pack(side="left", expand=True, fill="x", padx=5)
    
    # Frame para laboratório
    frame_lab = tk.Frame(dialog)
    frame_lab.pack(pady=5, fill="x", padx=10)
    var_lab_temp = tk.BooleanVar(value=var_lab.get())
    tk.Checkbutton(frame_lab, text="Necessita Laboratório?", variable=var_lab_temp).pack(padx=5)
    
    def confirmar():
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, entry_nome_temp.get())
        var_lab.set(var_lab_temp.get())
        atualizar_label_info_disciplina(label, entry_nome_temp.get(), var_lab_temp.get())
        dialog.destroy()
    
    tk.Button(dialog, text="Confirmar", command=confirmar).pack(pady=20)

# Criar interface gráfica
root = tk.Tk()
root.title("Gerenciamento de Professores e Disciplinas")
root.geometry("1200x800")  # Aumentei o tamanho da janela

# Criar canvas e scrollbar principal
main_canvas = tk.Canvas(root, width=1180)  # Defini uma largura fixa para o canvas
scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = ttk.Frame(main_canvas, width=1160)  # Frame com largura fixa

# Garantir que o frame mantenha um tamanho mínimo
scrollable_frame.grid_propagate(False)
scrollable_frame.pack_propagate(False)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1160)  # Definir largura da janela
main_canvas.configure(yscrollcommand=scrollbar.set)

# Botões principais
frame_botoes = tk.Frame(scrollable_frame)
frame_botoes.pack(pady=10, anchor="w", fill="x", padx=10)  # Adicionei padding horizontal

tk.Button(frame_botoes, text="Alocar Professores", command=alocar_professores).pack(side="left", padx=10)
tk.Button(frame_botoes, text="Exportar para JSON", command=exportar_json).pack(side="left", padx=10)
tk.Button(frame_botoes, text="Exportar para CSV", command=exportar_csv).pack(side="left", padx=10)

# Aba de Professores
frame_professor = tk.LabelFrame(scrollable_frame, text="Cadastrar Professor")
frame_professor.pack(pady=10, fill="x", padx=5)

# Frame para todas as informações
info_frame = tk.Frame(frame_professor)
info_frame.pack(fill="x", padx=5, pady=5)

# Frame para nome e área (lado esquerdo)
dados_frame = tk.Frame(info_frame)
dados_frame.pack(side="left", fill="x")

tk.Label(dados_frame, text="Nome:").pack(side="left", padx=5)
entry_nome_professor = tk.Entry(dados_frame, width=20)
entry_nome_professor.pack(side="left", padx=5)

tk.Label(dados_frame, text="Área:").pack(side="left", padx=5)
combo_area = ttk.Combobox(dados_frame, values=AREAS_ATUACAO, width=25)
combo_area.pack(side="left", padx=5)

# Frame para os dropdowns e botão cadastrar (lado direito)
dropdowns_frame = tk.Frame(info_frame)
dropdowns_frame.pack(side="left", fill="x", padx=10)

# Criar dropdowns com tamanho fixo
dias_dropdown = DropdownFrame(dropdowns_frame, "Dias", 
                            ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"])
horarios_dropdown = DropdownFrame(dropdowns_frame, "Horários", 
                                ["18h", "19h", "20h", "21h"])
modalidade_dropdown = DropdownFrame(dropdowns_frame, "Modalidade", 
                                  ["presencial", "ead", "híbrido"], False)

# Configurar largura fixa para os botões dos dropdowns
dias_dropdown.button.configure(width=15)
horarios_dropdown.button.configure(width=15)
modalidade_dropdown.button.configure(width=15)

# Botão de Cadastrar ao lado dos dropdowns
tk.Button(dropdowns_frame, text="Cadastrar", command=cadastrar_professor).pack(side="left", padx=5)

# Tabela de Professores
frame_lista_professores = tk.LabelFrame(scrollable_frame, text="Professores Cadastrados")
frame_lista_professores.pack(pady=10, fill="x", padx=5)

# Criar PanedWindow para permitir redimensionamento
paned_window_prof = ttk.PanedWindow(frame_lista_professores, orient="vertical")
paned_window_prof.pack(fill="both", expand=True)

# Container para a tabela e scrollbar de professores
container_tabela_prof = ttk.Frame(paned_window_prof)
paned_window_prof.add(container_tabela_prof, weight=1)

tree_professores = ttk.Treeview(container_tabela_prof, columns=("Nome", "Área", "Disponibilidade", "Modalidade"), show="headings", height=10)
for col in ("Nome", "Área", "Disponibilidade", "Modalidade"):
    tree_professores.heading(col, text=col)
    tree_professores.column(col, width=150)

# Scrollbar para a tabela de professores
scrollbar_prof = ttk.Scrollbar(container_tabela_prof, orient="vertical", command=tree_professores.yview)
tree_professores.configure(yscrollcommand=scrollbar_prof.set)
scrollbar_prof.pack(side="right", fill="y")
tree_professores.pack(side="left", fill="both", expand=True)

# Frame para botões da tabela de professores
frame_botoes_prof = tk.Frame(frame_lista_professores)
frame_botoes_prof.pack(fill="x", pady=5)
tk.Button(frame_botoes_prof, text="Excluir Professor", command=excluir_professor).pack(side="left", padx=5)
tk.Button(frame_botoes_prof, text="Editar Professor", command=editar_professor).pack(side="left", padx=5)

# Grip para redimensionamento
grip_prof = ttk.Sizegrip(frame_lista_professores)
grip_prof.pack(side="bottom", anchor="se")

# Aba de Disciplinas
frame_disciplina = tk.LabelFrame(scrollable_frame, text="Cadastrar Disciplina")
frame_disciplina.pack(pady=10, fill="x", padx=5)

# Frame para todas as informações da disciplina
info_disc_frame = tk.Frame(frame_disciplina)
info_disc_frame.pack(fill="x", padx=5, pady=5)

# Frame para nome e laboratório (lado esquerdo)
dados_disc_frame = tk.Frame(info_disc_frame)
dados_disc_frame.pack(side="left", fill="x")

tk.Label(dados_disc_frame, text="Nome:").pack(side="left", padx=5)
entry_nome_disciplina = tk.Entry(dados_disc_frame, width=20)
entry_nome_disciplina.pack(side="left", padx=5)

var_lab = tk.BooleanVar()
tk.Checkbutton(dados_disc_frame, text="Necessita Lab?", 
               variable=var_lab).pack(side="left", padx=5)

# Frame para os dropdowns da disciplina e botão cadastrar (lado direito)
dropdowns_disc_frame = tk.Frame(info_disc_frame)
dropdowns_disc_frame.pack(side="left", fill="x", padx=10)

# Criar dropdowns para disciplina com tamanho fixo
dias_disc_dropdown = DropdownFrame(dropdowns_disc_frame, "Dias", 
                                 ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"])
horarios_disc_dropdown = DropdownFrame(dropdowns_disc_frame, "Horários", 
                                     ["18h", "19h", "20h", "21h"])
tipo_dropdown = DropdownFrame(dropdowns_disc_frame, "Tipo", 
                            ["presencial", "ead", "híbrido"], False)

# Configurar largura fixa para os botões dos dropdowns
dias_disc_dropdown.button.configure(width=15)
horarios_disc_dropdown.button.configure(width=15)
tipo_dropdown.button.configure(width=15)

# Botão de Cadastrar ao lado dos dropdowns
tk.Button(dropdowns_disc_frame, text="Cadastrar", command=cadastrar_disciplina).pack(side="left", padx=5)

# Tabela de Disciplinas
frame_lista_disciplinas = tk.LabelFrame(scrollable_frame, text="Disciplinas Cadastradas")
frame_lista_disciplinas.pack(pady=10, fill="x", padx=5)

# Criar PanedWindow para permitir redimensionamento
paned_window_disc = ttk.PanedWindow(frame_lista_disciplinas, orient="vertical")
paned_window_disc.pack(fill="both", expand=True)

# Container para a tabela e scrollbar de disciplinas
container_tabela_disc = ttk.Frame(paned_window_disc)
paned_window_disc.add(container_tabela_disc, weight=1)

tree_disciplinas = ttk.Treeview(container_tabela_disc, columns=("Nome", "Tipo", "Laboratório", "Horário", "Professor"), show="headings", height=10)
for col in ("Nome", "Tipo", "Laboratório", "Horário", "Professor"):
    tree_disciplinas.heading(col, text=col)
    tree_disciplinas.column(col, width=150)

# Scrollbar para a tabela de disciplinas
scrollbar_disc = ttk.Scrollbar(container_tabela_disc, orient="vertical", command=tree_disciplinas.yview)
tree_disciplinas.configure(yscrollcommand=scrollbar_disc.set)
scrollbar_disc.pack(side="right", fill="y")
tree_disciplinas.pack(side="left", fill="both", expand=True)

# Frame para botões da tabela de disciplinas
frame_botoes_disc = tk.Frame(frame_lista_disciplinas)
frame_botoes_disc.pack(fill="x", pady=5)
tk.Button(frame_botoes_disc, text="Excluir Disciplina", command=excluir_disciplina).pack(side="left", padx=5)
tk.Button(frame_botoes_disc, text="Editar Disciplina", command=editar_disciplina).pack(side="left", padx=5)

# Grip para redimensionamento
grip_disc = ttk.Sizegrip(frame_lista_disciplinas)
grip_disc.pack(side="bottom", anchor="se")

# Função para ajustar o tamanho mínimo das tabelas
def configurar_tamanho_minimo():
    # Definir altura mínima para as tabelas
    tree_professores.configure(height=10)  # Altura mínima de 5 linhas
    tree_disciplinas.configure(height=10)  # Altura mínima de 5 linhas

root.after(100, configurar_tamanho_minimo)

# Configurar o layout final com scrollbar
main_canvas.pack(side="left", fill="both", expand=True, padx=5)  # Adicionei padding
scrollbar.pack(side="right", fill="y")

# Carregar os dados ao iniciar
carregar_dados()
atualizar_tabela_professores()
atualizar_tabela_disciplinas()

# Ajustar o tamanho das colunas das tabelas
def ajustar_colunas():
    # Ajustar colunas da tabela de professores
    largura_total = tree_professores.winfo_width()
    for col in ("Nome", "Área", "Disponibilidade", "Modalidade"):
        tree_professores.column(col, width=int(largura_total/4))
    
    # Ajustar colunas da tabela de disciplinas
    largura_total = tree_disciplinas.winfo_width()
    for col in ("Nome", "Tipo", "Laboratório", "Horário", "Professor"):
        tree_disciplinas.column(col, width=int(largura_total/5))

root.after(100, ajustar_colunas)  # Chamar após a janela ser renderizada

# Configurar a rolagem com o mouse de forma mais suave
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/60)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Permitir que o frame scrollable expanda horizontalmente
scrollable_frame.pack(expand=True, fill="both")

# Rodar a aplicação
root.mainloop()