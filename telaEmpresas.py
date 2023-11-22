from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as mb

class TelaEmpresas:
    def __init__(self,janela,dao):
        self.frame = tk.Frame(janela)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.dao=dao
        self.codigoOperacao=1
        self.page_size = 25  # Número de itens por página
        self.current_page = 1  # Página atual

        self.quadro=tk.Frame(self.frame,pady=10)
        self.quadro.pack(fill=tk.BOTH,expand=tk.YES,)

        self.quadro1=tk.Frame(self.frame,bg='white')
        self.quadro1.pack(fill=tk.X,expand=tk.YES,side='bottom')

        self.lblCnpj = tk.Label(self.quadro,text="CNPJ:")
        self.lblCnpj.grid(row=0,column=0)
        self.enyCnpj = tk.Entry(self.quadro,)
        self.enyCnpj.grid(row=0,column=1,)

        self.lblRazao = tk.Label(self.quadro,text="Razão Social:")
        self.lblRazao.grid(row=1,column=0,)
        self.enyRazao = tk.Entry(self.quadro)
        self.enyRazao.grid(row=1,column=1)

        self.lblNatureza = tk.Label(self.quadro,text="Natureza Juridica:")
        self.lblNatureza.grid(row=2,column=0,pady=4)
        self.enyNatureza = tk.Entry(self.quadro)
        self.enyNatureza.grid(row=2,column=1)

        self.lblQualificacao = tk.Label(self.quadro,text="Qualificação Responsavel:")
        self.lblQualificacao.grid(row=3,column=0,)
        self.enyQualificacao = tk.Entry(self.quadro)
        self.enyQualificacao.grid(row=3,column=1)

        self.lblCapital = tk.Label(self.quadro,text="Capital Social:")
        self.lblCapital.grid(row=4,column=0,pady=5)
        self.enyCapital = tk.Entry(self.quadro)
        self.enyCapital.grid(row=4,column=1)

        self.lblPorte = tk.Label(self.quadro,text="Porte Empresa:")
        self.lblPorte.grid(row=5,column=0,)
        self.enyPorte = tk.Entry(self.quadro)
        self.enyPorte.grid(row=5,column=1)

        self.lblEnte = tk.Label(self.quadro,text="Ente Federativo:")
        self.lblEnte.grid(row=6,column=0,pady=5)
        self.enyEnte = tk.Entry(self.quadro)
        self.enyEnte.grid(row=6,column=1)

        self.btnLimpar = tk.Button(self.quadro,fg='red',text='❌',command=self.acaoLimpar,)
        self.btnLimpar.grid(row=0,column=2)
        #self.btnLimpar.bind("<Button-1>",self.acaoLimpar)

        self.btnAtualizar = tk.Button(self.quadro,fg='blue',text='↻',padx=4,command=self.acaoAtualizarLista)
        self.btnAtualizar.grid(row=1,column=2)
        #self.btnAtualizar.bind("<Button-1>",self.acaoAtualizarLista)

        self.btnBuscar = tk.Button(self.quadro,text="buscar",command=self.acaoBuscar)
        self.btnBuscar.grid(row=7,column=0)
        #self.btnBuscar.bind('<Button-1>',self.acaoBuscar)

        self.btnInserir = tk.Button(self.quadro,text="inserir",command=self.acaoInserir)
        self.btnInserir.grid(row=7,column=1,pady=5)
        #self.btnInserir.bind("<Button-1>",self.acaoInserir)

        self.btnDeletar = tk.Button(self.quadro,text="excluir",command=self.acaoExcluir)
        self.btnDeletar.grid(row=7,column=2,padx=25)
        #self.btnDeletar.bind("<Button-1>",self.acaoExcluir)

        self.btnAlterar = tk.Button(self.quadro,text="alterar",command=self.acaoAtualizarDados)
        self.btnAlterar.grid(row=7,column=3,padx=37)
        #self.btnAlterar.bind("<Button-1>",self.acaoAtualizarDados)

        self.btnPaginaAnterior = tk.Button(self.quadro1, text="Página Anterior", command=self.pagina_anterior)
        self.btnPaginaAnterior.grid(row=0,column=0,padx=100)

        self.btnProximaPagina = tk.Button(self.quadro1, text="Próxima Página", command=self.proxima_pagina)
        self.btnProximaPagina.grid(row=0,column=1,)

        
        colunas=("cnpj", "razao social", "natureza", "qualificacao responsavel", "Capital social", "porte empresa", "Ente Federativo")
        self.tree = ttk.Treeview(self.frame,columns=colunas,show="headings")

        # Cabeçalho
        self.tree.heading("#1", text="CNPJ",)
        self.tree.heading("#2", text="Razão Social")
        self.tree.heading("#3", text="Natureza Juridica")
        self.tree.heading("#4", text="Qualificação Responsável")
        self.tree.heading("#5", text="Capital Social")
        self.tree.heading("#6", text="Porte Empresa")
        self.tree.heading("#7", text="Ente Federativo")

        self.tree.column("#1",width=5)
        self.tree.column("#2",width=200)
        self.tree.column("#3",width=20)
        self.tree.column("#4",width=20)
        self.tree.column("#5",width=10)
        self.tree.column("#6",width=10)
        self.tree.column("#7",width=10)

        # adicionando barra de rolagem
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack( side = tk.RIGHT, fill=tk.Y )

        #vinculando o treeview ao scrollbar
        self.scrollbar.config( command = self.tree.yview )
        self.tree.config(yscrollcommand=self.scrollbar.set)

        self.tree.pack(fill=tk.BOTH, expand=tk.YES)

        #evento de clique
        self.tree.bind("<Double-1>", self.selecionarLinha)

        self.atualizarTabela(self.dao.buscar())

    def atualizarTabela(self,registros):
        self.tree.delete(*self.tree.get_children())
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size

        # Exiba apenas os itens da página atual
        for registro in registros[start:end]:
            self.tree.insert('', tk.END, values=registro)

        # for registro in registros:
        #     self.tree.insert('', tk.END, values=registro)
    
    def acaoInserir(self):
        if (self.enyCnpj.get() != ''  and self.enyRazao.get() != '' and self.enyNatureza.get() != '' and self.enyPorte.get() != ''):
            try:
                self.dao.inserir(self.enyCnpj.get(),self.enyRazao.get(),self.enyNatureza.get(),self.enyQualificacao.get(),self.enyCapital.get(),self.enyPorte.get(),self.enyEnte.get())
                self.atualizarTabela(self.dao.buscar())
                mb.showinfo('informação','Valor inserido com sucesso!')
            
            except Exception as erro:
                mb.showerror('erro',f"O codigo que você inseriu ja existe!\n {erro}")

        else:
            mb.showinfo('informação','É nescessario preencher o cnpj, razao social, natureza juridica e porte da empresa!')
                
    def acaoExcluir(self):

        if self.enyCnpj.get() != '':           
            if self.dao.buscarCodigo(self.enyCnpj.get().strip()) != []:
                try:
                    if mb.askyesno('aviso','Tem certeza que deseja excluir a informação?'): 
                        self.dao.deletar(self.enyCnpj.get())
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
            if self.dao.buscarCodigo(self.enyCnpj.get().strip(),self.enyRazao.get().strip(),self.enyNatureza.get().strip(),self.enyQualificacao.get().strip(),self.enyCapital.get().strip(),self.enyPorte.get().strip(),self.enyEnte.get().strip()) != []:

                self.atualizarTabela(self.dao.buscarCodigo(self.enyCnpj.get().strip(),self.enyRazao.get().strip(),self.enyNatureza.get().strip(),self.enyQualificacao.get().strip(),self.enyCapital.get().strip(),self.enyPorte.get().strip(),self.enyEnte.get().strip()))
                self.codigoOperacao=2
            else:
                mb.showwarning('warning','A sua busca não obteve resultado!')
        except TypeError as erro:
            mb.showwarning('warning',erro)

    def acaoAtualizarDados(self):
        try:
            if (self.enyCnpj.get() != ''  and self.enyRazao.get() != '' and self.enyNatureza.get() != '' and self.enyPorte.get() != ''):
                if self.dao.buscarCodigo(self.enyCnpj.get().strip()) != []:
                    self.dao.atualizar(self.enyCnpj.get(),self.enyRazao.get(),self.enyNatureza.get(),self.enyQualificacao.get(),self.enyCapital.get(),self.enyPorte.get(),self.enyEnte.get())
                    self.atualizarTabela(self.dao.buscar())
                    mb.showinfo('info','Alteração realizada com sucesso!')
                else:
                    mb.showerror('erro','Não foi possivel realizar a alteração dos parametrs passados,verifique e tente novamente!')

            elif self.enyCnpj.get().strip() =='':
                mb.showinfo('info','insira o cnpj da informação que deseja alterar')
            elif self.enyRazao.get().strip() =='':
                mb.showinfo('info','insira a razao social da informação que deseja alterar')
            elif self.enyNatureza.get().strip() =='':
                mb.showinfo('info','insira a natureza juridica da informação que deseja alterar')
            elif self.enyPorte.get().strip() =='':
                mb.showinfo('info','insira o porte da empresa da informação que deseja alterar')
                

        except Exception as erro:
            mb.showerror('erro',erro)

    def selecionarLinha(self,event):
        item = self.tree.item( self.tree.selection() )
        self.enyCnpj.delete(0, tk.END)
        self.enyCnpj.insert(0,item['values'][0]) 
        self.enyRazao.delete(0, tk.END)
        self.enyRazao.insert(0,item['values'][1])
        self.enyNatureza.delete(0, tk.END)
        self.enyNatureza.insert(0,item['values'][2]) 
        self.enyQualificacao.delete(0, tk.END)
        self.enyQualificacao.insert(0,item['values'][3])
        self.enyCapital.delete(0, tk.END)
        self.enyCapital.insert(0,item['values'][4]) 
        self.enyPorte.delete(0, tk.END)
        self.enyPorte.insert(0,item['values'][5])
        self.enyEnte.delete(0, tk.END)
        self.enyEnte.insert(0,item['values'][6])

    def acaoAtualizarLista(self):
        self.current_page = 1
        self.atualizarTabela(self.dao.buscar())
        self.codigoOperacao=1
        
    def acaoLimpar(self):
        self.enyCnpj.delete(0, tk.END)
        self.enyCnpj.insert(0,'') 

        self.enyRazao.delete(0, tk.END)
        self.enyRazao.insert(0,'')

        self.enyNatureza.delete(0, tk.END)
        self.enyNatureza.insert(0,'') 

        self.enyQualificacao.delete(0, tk.END)
        self.enyQualificacao.insert(0,'')

        self.enyCapital.delete(0, tk.END)
        self.enyCapital.insert(0,'') 

        self.enyPorte.delete(0, tk.END)
        self.enyPorte.insert(0,'')

        self.enyEnte.delete(0, tk.END)
        self.enyEnte.insert(0,'')
    


    def pagina_anterior(self):
        if self.current_page > 1:
            self.current_page -= 1
            if self.codigoOperacao == 1:
                self.atualizarTabela(self.dao.buscar())
            elif self.codigoOperacao ==2:
                self.atualizarTabela(self.dao.buscarCodigo(self.enyCnpj.get().strip(),self.enyRazao.get().strip(),self.enyNatureza.get().strip(),self.enyQualificacao.get().strip(),self.enyCapital.get().strip(),self.enyPorte.get().strip(),self.enyEnte.get().strip()))

    def proxima_pagina(self):
        if self.current_page < len(self.dao.buscar()) / self.page_size:
            self.current_page += 1
            if self.codigoOperacao == 1:
                self.atualizarTabela(self.dao.buscar())
            elif self.codigoOperacao ==2:
                self.atualizarTabela(self.dao.buscarCodigo(self.enyCnpj.get().strip(),self.enyRazao.get().strip(),self.enyNatureza.get().strip(),self.enyQualificacao.get().strip(),self.enyCapital.get().strip(),self.enyPorte.get().strip(),self.enyEnte.get().strip()))