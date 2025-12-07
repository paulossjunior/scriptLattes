#!/usr/bin/python
# encoding: utf-8

import re
from scriptLattes.util import similaridade_entre_cadeias


class AtuacaoProfissional:
    tipo = "Atuação profissional"
    item = None  # dado bruto
    idMembro = None

    instituicao = None
    vinculo = None
    periodo = None
    enquadramento = None
    regime = None
    cargo_funcao = None
    atividades = None
    disciplinas = None
    linhas_pesquisa = None
    ano_inicio = None
    ano_fim = None
    chave = None

    def __init__(self, idMembro, partesDoItem=''):
        self.idMembro = set([])
        self.idMembro.add(idMembro)

        if partesDoItem:
            print(f"DEBUG: AtuacaoProfissional partesDoItem: {partesDoItem}")
            # partesDoItem[0]: Numero (NAO USADO)
            # partesDoItem[1]: Descricao
            self.item = partesDoItem[1]
            self._parse_item(self.item)
            self.chave = f"{self.instituicao or ''}::{self.periodo or ''}::{self.cargo_funcao or ''}"
        else:
            self.item = ''
            self.instituicao = ''
            self.vinculo = ''
            self.periodo = ''
            self.enquadramento = ''
            self.regime = ''
            self.cargo_funcao = ''
            self.atividades = ''
            self.disciplinas = ''
            self.linhas_pesquisa = ''
            self.ano_inicio = ''
            self.ano_fim = ''
            self.chave = ''

    def _parse_item(self, texto):
        """Parse do texto de atuação profissional"""
        if not texto:
            return

        # Normalizar texto
        texto = " ".join(texto.split())
        
        # Extrair instituição - tenta primeiro o padrão de div, depois fallback antes de "Vínculo"
        instituicao_match = re.search(r'\u003cdiv class=\"inst_back\"\u003e\u003cb\u003e([^\u003c]+)\u003c/b\u003e\u003c/div\u003e', texto)
        if instituicao_match:
            self.instituicao = instituicao_match.group(1).strip()
        else:
            # Fallback: capturar texto antes de "Vínculo" ou "VÃ­nculo"
            fallback_match = re.search(r'^(.*?)(?=\s*V[^:]*nculo\s*:)', texto, re.DOTALL)
            if fallback_match:
                self.instituicao = fallback_match.group(1).strip()
            else:
                # Último recurso: primeira linha em negrito ou até ponto
                match = re.search(r'^([^\.]+)', texto)
                if match:
                    self.instituicao = match.group(1).strip()
        
        if not self.instituicao:
            print(f"DEBUG: Instituicao not found in text: {texto!r}")

        # Extrair período - múltiplos padrões para HTML
        periodo_patterns = [
            # Padrão HTML com tags <b> em layout-cell
            r'layout-cell-3[^>]*text-align-right[^>]*>.*?<b>([0-9/]+\s*-\s*[0-9/]+|[0-9/]+\s*-\s*Atual|[0-9/]+\s*-\s*atual|\d{4}\s*-\s*\d{4}|\d{2}/\d{4}\s*-\s*\d{2}/\d{4}|\d{2}/\d{4}\s*-\s*Atual)</b>',
            # Padrão simples com tags <b>
            r'<b>([0-9/]+\s*-\s*[0-9/]+|[0-9/]+\s*-\s*Atual|[0-9/]+\s*-\s*atual|\d{4}\s*-\s*\d{4}|\d{2}/\d{4}\s*-\s*\d{2}/\d{4}|\d{2}/\d{4}\s*-\s*Atual)</b>',
            # Padrão original (texto puro)
            r'(\d{4}\s*-\s*(?:\d{4}|Atual))',
            # Padrão MM/YYYY
            r'(\d{2}/\d{4}\s*-\s*(?:\d{2}/\d{4}|Atual))'
        ]
        
        periodo_encontrado = None
        for pattern in periodo_patterns:
            periodo_match = re.search(pattern, texto, re.IGNORECASE | re.DOTALL)
            if periodo_match:
                periodo_encontrado = periodo_match.group(1).strip()
                break
        
        if periodo_encontrado:
            self.periodo = periodo_encontrado
            # Extrair anos do período encontrado
            periodo_limpo = periodo_encontrado.replace(' ', '')
            if '-' in periodo_limpo:
                partes = periodo_limpo.split('-')
                inicio = partes[0].strip()
                fim = partes[1].strip() if len(partes) > 1 else ''
                
                # Extrair ano de início
                if '/' in inicio:  # Formato MM/YYYY
                    self.ano_inicio = inicio.split('/')[1] if '/' in inicio else inicio
                elif inicio.isdigit() and len(inicio) == 4:  # Formato YYYY
                    self.ano_inicio = inicio
                
                # Extrair ano de fim
                if fim and fim.lower() != 'atual':
                    if '/' in fim:  # Formato MM/YYYY
                        self.ano_fim = fim.split('/')[1] if '/' in fim else fim
                    elif fim.isdigit() and len(fim) == 4:  # Formato YYYY
                        self.ano_fim = fim
                else:
                    self.ano_fim = 'Atual'

        # Extrair vínculo - busca por "Vínculo:" (considerando codificação)
        vinculo_patterns = [
            r'Vínculo:\s*([^,]+)',
            r'VÃ­nculo:\s*([^,]+)'  # Versão com codificação malformada
        ]
        for pattern in vinculo_patterns:
            vinculo_match = re.search(pattern, texto)
            if vinculo_match:
                self.vinculo = vinculo_match.group(1).strip()
                break

        # Extrair enquadramento funcional
        enquadramento_patterns = [
            r'Enquadramento Funcional:\s*([^,]+)',
            r'Enquadramento Funcional:\s*([^,]+)'
        ]
        for pattern in enquadramento_patterns:
            enquadramento_match = re.search(pattern, texto)
            if enquadramento_match:
                self.enquadramento = enquadramento_match.group(1).strip()
                break

        # Extrair regime
        regime_match = re.search(r'Regime:\s*([^.]+)', texto)
        if regime_match:
            self.regime = regime_match.group(1).strip()

        # Extrair cargo ou função
        cargo_match = re.search(r'Cargo ou função[^:]*:?\s*([^.]+)', texto)
        if cargo_match:
            self.cargo_funcao = cargo_match.group(1).strip()

        # Extrair disciplinas ministradas
        disciplinas_match = re.search(r'Disciplinas ministradas[^:]*:?\s*([^.]+(?:\.[^.]*)*)', texto)
        if disciplinas_match:
            disciplinas_texto = disciplinas_match.group(1).strip()
            self.disciplinas = [d.strip() for d in re.split(r'<br[^>]*>', disciplinas_texto) if d.strip()]

        # Extrair linhas de pesquisa
        linhas_match = re.search(r'Linhas de pesquisa[^:]*:?\s*([^.]+(?:\.[^.]*)*)', texto)
        if linhas_match:
            linhas_texto = linhas_match.group(1).strip()
            self.linhas_pesquisa = [l.strip() for l in re.split(r'<br[^>]*>', linhas_texto) if l.strip()]

        # Extrair atividades (ensino, pesquisa, direção, etc.)
        atividades_patterns = [
            r'(Ensino[^.]*\.)',
            r'(Pesquisa e desenvolvimento[^.]*\.)',
            r'(Direção e administração[^.]*\.)',
            r'(Conselhos, Comissões e Consultoria[^.]*\.)'
        ]
        atividades_encontradas = []
        for pattern in atividades_patterns:
            matches = re.findall(pattern, texto)
            atividades_encontradas.extend(matches)
        
        if atividades_encontradas:
            self.atividades = atividades_encontradas

    def compararCom(self, objeto):
        if self.idMembro.isdisjoint(objeto.idMembro) and similaridade_entre_cadeias(self.item or '', objeto.item or ''):
            # Une conjuntos de membros
            self.idMembro.update(objeto.idMembro)

            # Mantém representação mais rica/longa quando houver
            if len(self.item or "") < len(objeto.item or ""):
                self.item = objeto.item
                self._parse_item(self.item)

            return self
        else:
            return None

    def json(self):
        def nv(x):
            return x if x not in (None, '', [], {}) else None

        result = {
            "instituicao": nv(self.instituicao),
            "periodo": nv(self.periodo),
            "ano_inicio": nv(self.ano_inicio),
            "ano_fim": nv(self.ano_fim),
            "vinculo": nv(self.vinculo),
            "enquadramento": nv(self.enquadramento),
            "regime": nv(self.regime),
            "cargo_funcao": nv(self.cargo_funcao),
            "tipo": self.tipo
        }

        if self.disciplinas:
            result["disciplinas"] = self.disciplinas
        if self.linhas_pesquisa:
            result["linhas_pesquisa"] = self.linhas_pesquisa
        if self.atividades:
            result["atividades"] = self.atividades

        return result

    def __str__(self):
        s = "\n[ATUACAO PROFISSIONAL] \n"
        s += "+ID-MEMBRO   : " + str(self.idMembro) + "\n"
        s += "+INSTITUICAO : " + str(self.instituicao) + "\n"
        s += "+PERIODO     : " + str(self.periodo) + "\n"
        s += "+VINCULO     : " + str(self.vinculo) + "\n"
        s += "+ENQUADRAMENT: " + str(self.enquadramento) + "\n"
        s += "+REGIME      : " + str(self.regime) + "\n"
        s += "+CARGO/FUNCAO: " + str(self.cargo_funcao) + "\n"
        return s