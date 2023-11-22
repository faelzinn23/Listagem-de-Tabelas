from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as mb

class TelaPorte:
    def __init__(self,janela,dao):
        self.frame=tk.Frame(janela)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.dao=dao

        self.quadro=tk.Frame(self.frame,pady=10)
        self.quadro.pack(fill=tk.BOTH,expand=tk.YES,)

        self.lblCodigo = tk.Label(self.quadro,text="Codigo:")
        self.lblCodigo.grid(row=0,column=0)
        self.enyCodigo = tk.Entry(self.quadro,)
        self.enyCodigo.grid(row=0,column=1)

        self.lblDescricao = tk.Label(self.quadro,text="Descrição:")
        self.lblDescricao.grid(row=1,column=0,pady=8)
        self.enyDescricao = tk.Entry(self.quadro)
        self.enyDescricao.grid(row=1,column=1)

        self.btnLimpar = tk.Button(self.quadro,fg='red',text='❌',command=self.acaoLimpar)
        self.btnLimpar.grid(row=0,column=2)
        #self.btnLimpar.bind("<Button-1>",self.acaoLimpar)

        self.btnAtualizar = tk.Button(self.quadro,fg='blue',text='↻',padx=4,command=self.acaoAtualizarLista)
        self.btnAtualizar.grid(row=1,column=2)
        #self.btnAtualizar.bind("<Button-1>",self.acaoAtualizarLista)

        self.btnBuscar = tk.Button(self.quadro,text="buscar",command=self.acaoBuscar)
        self.btnBuscar.grid(row=2,column=0)
        #self.btnBuscar.bind('<Button-1>',self.acaoBuscar)

        self.btnInserir = tk.Button(self.quadro,text="inserir",command=self.acaoInserir)
        self.btnInserir.grid(row=2,column=1,pady=5)
        #self.btnInserir.bind("<Button-1>",self.acaoInserir)

        self.btnDeletar = tk.Button(self.quadro,text="excluir",command=self.acaoExcluir)
        self.btnDeletar.grid(row=2,column=2)
        #self.btnDeletar.bind("<Button-1>",self.acaoExcluir)

        self.btnAlterar = tk.Button(self.quadro,text="alterar",command=self.acaoAtualizarDados)
        self.btnAlterar.grid(row=2,column=3,padx=37)
        #self.btnAlterar.bind("<Button-1>",self.acaoAtualizarDados)
        
        colunas=("codigo","descricao")
        self.tree = ttk.Treeview(self.frame,columns=colunas,show="headings")

        # Cabeçalho
        self.tree.heading('codigo', text='Código')
        self.tree.heading('descricao', text='Descrição')

        # adicionando barra de rolagem
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack( side = tk.RIGHT, fill=tk.Y )

        #vinculando o treeview ao scrollbar
        self.scrollbar.config( command = self.tree.yview )
        self.tree.config(yscrollcommand=self.scrollbar.set)

        self.tree.pack(fill=tk.BOTH, expand=tk.YES)

        #evento de clique
        self.tree.bind("<Double-1>", self.selecionarLinha)

        # 
        self.atualizarTabela(self.dao.buscar())

    def atualizarTabela(self,registros):
        self.tree.delete(*self.tree.get_children())
        for registro in registros:
            self.tree.insert('', tk.END, values=registro)

    def acaoInserir(self):
        if (self.enyCodigo.get() != ''  and self.enyDescricao.get() != ''):
            try:
                self.dao.inserir(self.enyCodigo.get(),self.enyDescricao.get())
                self.atualizarTabela(self.dao.buscar())
                mb.showinfo('informação','Valor inserido com sucesso!')
            
            except Exception as erro:
                mb.showerror('erro',f"O codigo que você inseriu ja existe!\n {erro}")

        else:
            mb.showinfo('informação','É nescessario preencher todos os campos!')

    def acaoExcluir(self):


        if self.enyCodigo.get() != '':
            
            if self.dao.buscarCodigo(self.enyCodigo.get()) != None:
                try:
                    if mb.askyesno('aviso','Tem certeza que deseja excluir a informação?'): 
                        self.dao.deletar(self.enyCodigo.get())
                        self.atualizarTabela(self.dao.buscar())
                        mb.showinfo('exclusao concluida','Exclusão concluida com sucesso!')
                except Exception as errro:
                    mb.showerror('erro',f"O codigo que você inseriu ja existe!\n {errro}")
            else:
                mb.showinfo('informação','O valor passado nao existe na tabela!')
        else:
            mb.showinfo('informação','É nescessario informar o código que deseja excluir!')
   
    def acaoBuscar(self):
        try:
            if self.enyCodigo.get().strip() !='' and self.enyDescricao.get().strip() =='':
                self.atualizarTabela(self.dao.buscarCodigo(self.enyCodigo.get()))

            elif self.enyDescricao.get().strip() !='' and self.enyCodigo.get().strip() =='':
                self.atualizarTabela(self.dao.buscarDescricao(self.enyDescricao.get()))

            elif self.enyCodigo.get().strip() !='' and self.enyDescricao.get().strip() !='':
                mb.showinfo('info','Utilize apenas um dos campos para realizar a busca!')
            else:
                self.atualizarTabela(self.dao.buscar())
        except TypeError as erro:
            mb.showwarning('warning','A sua busca não obteve resultado!')

    def selecionarLinha(self,event):
        item = self.tree.item( self.tree.selection() )
        self.enyCodigo.delete(0, tk.END)
        self.enyCodigo.insert(0, item['values'][0]) 
        self.enyDescricao.delete(0, tk.END)
        self.enyDescricao.insert(0, item['values'][1])

    def acaoAtualizarDados(self):
        
        if self.enyCodigo.get().strip() !='' and self.enyDescricao.get().strip() !='' :
            if self.dao.buscarCodigo(self.enyCodigo.get()) != None:
                self.dao.atualizar(self.enyCodigo.get(),self.enyDescricao.get())
                self.atualizarTabela(self.dao.buscar())
                mb.showinfo('info','Alteração realizada com sucesso!')
            else:
                mb.showerror('erro','Não foi possivel realizar a alteração dos parametrs passados,verifique e tente novamente!')

        elif self.enyCodigo.get().strip() =='':
            mb.showinfo('info','insira o codigo da informação que deseja alterar')
             

        elif self.enyCodigo.get().strip() !='' and self.enyDescricao.get().strip() =='':
            mb.showinfo('info','insira a nova descrição')
        

    def acaoAtualizarLista(self):
        self.atualizarTabela(self.dao.buscar())
    
    def acaoLimpar(self):
        self.enyCodigo.delete(0, tk.END)
        self.enyCodigo.insert(0,'') 
        self.enyDescricao.delete(0, tk.END)
        self.enyDescricao.insert(0,'')



        