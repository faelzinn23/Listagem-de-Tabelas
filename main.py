from naturezaJuridicaDAO import *
from telaNatureza import *
from empresasDAO import *
from telaEmpresas import *
from telaPorte import *
from porteDAO import *
import tkinter as tk

empresasdao=EmpresaDAO()

natdao=NaturezaDAO()

portedao=PorteDAO()

class Aplicacao:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Alternador de Telas")

        # barra de menu
        self.barra_menu = tk.Menu(self.janela)
        self.janela.config(menu=self.barra_menu)

        
        self.menu_telas = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Tabelas", menu=self.menu_telas)

        #itens do menu para cada tela
        self.menu_telas.add_command(label="Empresas", command=self.exibir_tela1)
        self.menu_telas.add_command(label="Natureza Juridica", command=self.exibir_tela2)
        self.menu_telas.add_command(label="Porte da Empresa", command=self.exibir_tela3)

        
        self.tela_atual = None
        self.exibir_tela1()
        

    def exibir_tela1(self):
        if self.tela_atual:
            self.tela_atual.frame.forget()   
        self.tela_atual = TelaEmpresas(self.janela,empresasdao)
        #self.tela_atual.frame.pack(fill=tk.BOTH, expand=True)

    def exibir_tela2(self):
        if self.tela_atual:
            self.tela_atual.frame.forget()
            
        self.tela_atual = TelaNatureza(self.janela,natdao)
        #self.tela_atual.frame.pack(fill=tk.BOTH, expand=True)

    def exibir_tela3(self):
        if self.tela_atual:
            self.tela_atual.frame.forget()
            
        self.tela_atual = TelaPorte(self.janela,portedao)
        #self.tela_atual.frame.pack(fill=tk.BOTH, expand=True)
    

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.geometry('800x500')
    root.mainloop()
