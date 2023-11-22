import sqlite3 

class NaturezaDAO:
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
            
            self.cursor.execute("select * from Desc_NaturezaJuridica")
            resultado=self.cursor.fetchall()
            self.fecharConexao()
            return resultado
        else:
            return None
        
    def buscarCodigo(self,codigo):
        if(self.abrirConexao()):
            self.cursor.execute("select * from Desc_NaturezaJuridica where id_natureza = ?",(str(codigo),))
            resultado=self.cursor.fetchone()
            self.fecharConexao()
            return resultado
        else:
            return None
    
    def buscarDescricao(self,descricao):
        if(self.abrirConexao()):
            self.cursor.execute("select * from Desc_NaturezaJuridica where UPPER(descricao_natureza) LIKE UPPER(?)",('%'+descricao+'%',))
            resultado=self.cursor.fetchall() 
            
            self.fecharConexao()
            return resultado
            
        else:
            return None

    def inserir(self,codigo,descricao):
        if(self.abrirConexao()):
                self.cursor.execute("insert into Desc_NaturezaJuridica (id_natureza,descricao_natureza) values (?,?)",(codigo,descricao))
                self.conexao.commit()
                self.fecharConexao()
            
    def deletar(self,codigo):
        if(self.abrirConexao()):
            #try:
                self.cursor.execute("delete from Desc_NaturezaJuridica where id_natureza = ?",(codigo,))
                self.conexao.commit()
                self.fecharConexao()
           # except sqlite3.DatabaseError as erro:
                #print(erro)
 
    def atualizar(self,codigo,atualizacao):
        if(self.abrirConexao()):
            try:
                self.cursor.execute("update Desc_NaturezaJuridica  set descricao_natureza = (?) where id_natureza = ?",(atualizacao,codigo))
                self.conexao.commit()
                self.fecharConexao()
            except sqlite3.DatabaseError as erro:
                print(erro)

    def buscarTodosCodigos(self):
        if(self.abrirConexao()):
            
            self.cursor.execute("select id_natureza from Desc_NaturezaJuridica")
            resultado=self.cursor.fetchall()
            self.fecharConexao()
            lista=[]
            for indice,codigo in enumerate(resultado):
                lista.insert(indice,str(codigo[0]).strip())
            return lista
        else:
            return None