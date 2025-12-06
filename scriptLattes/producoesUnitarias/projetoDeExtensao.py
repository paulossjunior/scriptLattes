#!/usr/bin/python
# encoding: utf-8


import datetime
import unicodedata
from scriptLattes.util import similaridade_entre_cadeias


class ProjetoDeExtensao:
    tipo = "Projeto de extensão"
    idMembro = None
    anoInicio = None
    anoConclusao = None
    nome = ''
    descricao = ''
    chave = None
    ano = None

    def __init__(self, idMembro, partesDoItem):
        # partesDoItem[0]: Periodo do projeto de extensão
        # partesDoItem[1]: cargo e titulo do projeto
        # partesDoItem[2]: Descricao (resto)

        self.idMembro = list([])
        self.idMembro.append(idMembro)

        anos = partesDoItem[0].partition("-")
        self.anoInicio = anos[0].strip()
        self.anoConclusao = anos[2].strip()

        # detalhe = partesDoItem[1].rpartition(":")
        #self.cargo = detalhe[0].strip()
        #self.nome = detalhe[2].strip()
        self.nome = partesDoItem[1]

        self.descricao = list([])
        if len(partesDoItem) > 2:
            self.descricao.append(partesDoItem[2])
        else:
            self.descricao.append("")

        self.chave = self.nome # chave de comparação entre os objetos

        # Conversao para int quando aplicavel
        try:
            self.anoInicio = int(self.anoInicio)
        except:
            self.anoInicio = 0

        try:
            self.anoConclusao = int(self.anoConclusao)
        except:
            if 'Atual' in self.anoConclusao:
                self.anoConclusao = datetime.datetime.now().year
            else:
                self.anoConclusao = 0

        self.ano = self.anoInicio # para comparação entre objetos

    def html(self, listaDeMembros):
        if self.anoConclusao==datetime.datetime.now().year:
            self.anoConclusao = 'Atual'

        if self.anoInicio==0 and self.anoConclusao==0:
            s = '<span class="projects"> (*) </span> '
        else:
            s = '<span class="projects">' + str(self.anoInicio) + '-' + str(self.anoConclusao) + '</span>. '
        s+= '<b>' +  self.nome  + '</b>'

        for i in range(0, len(self.idMembro)):
            s+= '<br><i><font size=-1>'+ self.descricao[i] +'</font></i>'
            m = listaDeMembros[ self.idMembro[i] ]
            
            nome_membro = m.nomeCompleto
            nome_membro = nome_membro.replace(u'\xa0', ' ')
            
            for a in m.nomeEmCitacoesBibliograficas.split(';'):
                if len(a)>0:
                    nome_membro = nome_membro.replace(a.strip(), '<a style="text-decoration: none" href="' + m.url + '">' + a.strip() + '</a>')

            s += '<br>Integrante: ' + nome_membro

        return s

    def json(self):
        def nv(x):
            return x if x not in (None, '', []) else None
        
        return {
            "nome": nv(self.nome),
            "ano_inicio": nv(str(self.anoInicio) if self.anoInicio != 0 else None),
            "ano_conclusao": nv(str(self.anoConclusao) if self.anoConclusao != 0 else None),
            "descricao": nv(self.descricao),
            "tipo": nv(self.tipo)
        }

    def compararCom(self, objeto):
        if set(self.idMembro).isdisjoint(set(objeto.idMembro)) and similaridade_entre_cadeias(self.nome, objeto.nome):
            # Os IDs dos membros são agrupados.
            # Essa parte é importante para a geracao do relorio de projetos
            self.idMembro.extend(objeto.idMembro)

            self.descricao.extend(objeto.descricao) # Apenas juntamos as descrições

            return self
        else: # nao similares
            return None

    # ------------------------------------------------------------------------ #
    def __str__(self):
        s  = "\n[PROJETO DE EXTENSÃO] \n"
        s += "+ID-MEMBRO   : " + str(self.idMembro) + "\n"
        s += "+ANO INICIO  : " + str(self.anoInicio) + "\n"
        s += "+ANO CONCLUS.: " + str(self.anoConclusao) + "\n"
        s += "+NOME        : " + self.nome + "\n"
        s += "+DESCRICAO   : " + str(self.descricao) + "\n"
        return s