import sqlite3 

class EmpresaDAO:
    def abrirConexao(self):
        try:
            self.conexao = sqlite3.connect('Empresas0.db')
            self.cursor = self.conexao.cursor()
            return True
        except sqlite3.DataBaseError as erro:
            print('erro na conexao',erro)
            return False
        
    def fecharConexao(self):
        if(self.conexao):
            self.cursor.close()
            self.conexao.close()
            
        
    def buscar(self):
        if(self.abrirConexao()):
            
            self.cursor.execute("select * from Empresas")
            resultado=self.cursor.fetchall()
            self.fecharConexao()
            return resultado
        else:
            return None
        
    def buscarCodigo(self,cnpj='%' ,razao='%' ,natureza='%',qualificacao='%',capital='%' ,porte='%' ,ente='%'):
        if cnpj == '':
            cnpj='%'
        if natureza == '':
            natureza='%'
        if qualificacao == '':
            qualificacao='%'
        if capital == '':
            capital='%'
        if porte == '':
            porte='%'
        if ente == '':
            ente='%'
        if(self.abrirConexao()):
            comando='''select * from Empresas
                        where UPPER(cnpj like UPPER(?)) 
                        and UPPER(razao_social like UPPER(?))
                        and UPPER(natureza_juridica like UPPER(?))
                        and UPPER(qualificacao_resp like UPPER(?))
                        and UPPER(capital_social like UPPER(?))
                        and UPPER(porte_empresa like UPPER(?))
                        and UPPER(ente_federativo like UPPER(?))'''
            
            self.cursor.execute(comando,(cnpj,'%' + razao + '%',natureza , qualificacao,capital,porte,ente ))
            resultado=self.cursor.fetchall()
            self.fecharConexao()
            return resultado
        else:
            return None
    
    # def buscarDescricao(self,descricao):
    #     if(self.abrirConexao()):
    #         self.cursor.execute("select * from Desc_NaturezaJuridica where UPPER(descricao_natureza) LIKE UPPER(?)",('%'+descricao+'%',))
    #         resultado=self.cursor.fetchall() 
            
    #         self.fecharConexao()
    #         return resultado
            
    #     else:
    #         return None

    def inserir(self,cnpj,razao,natureza,qualificacao,capital,porte,ente):
        if(self.abrirConexao()):
                self.cursor.execute('''insert into Empresas (cnpj,razao_social,natureza_juridica,qualificacao_resp,capital_social,porte_empresa,ente_federativo) 
                                    values (?,?,?,?,?,?,?)''',(cnpj,razao,natureza,qualificacao,capital,porte,ente))
                self.conexao.commit()
                self.fecharConexao()
            
    def deletar(self,codigo):
        if(self.abrirConexao()):
            #try:
                self.cursor.execute("delete from Empresas where cnpj = ?",(codigo,))
                self.conexao.commit()
                self.fecharConexao()
           # except sqlite3.DatabaseError as erro:
                #print(erro)
 
    def atualizar(self,cnpj,razao,natureza,qualificacao,capital,porte,ente):
        if(self.abrirConexao()):
            try:
                self.cursor.execute('''update Empresas  set razao_social = (?),
                                    natureza_juridica = (?),
                                    qualificacao_resp = (?),
                                    capital_social = (?),
                                    porte_empresa = (?),
                                    ente_federativo = (?) where cnpj = ?''',(razao,natureza,qualificacao,capital,porte,ente,cnpj))
                self.conexao.commit()
                self.fecharConexao()
            except sqlite3.DatabaseError as erro:
                print(erro)

    # def buscarTodosCodigos(self):
    #     if(self.abrirConexao()):
            
    #         self.cursor.execute("select cnpj from empresas")
    #         resultado=self.cursor.fetchall()
    #         self.fecharConexao()
    #         lista=[]
    #         for indice,codigo in enumerate(resultado):
    #             lista.insert(indice,str(codigo[0]).strip())
    #         return lista
    #     else:
    #         return None