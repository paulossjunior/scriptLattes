# scriptLattes
O CNPq realiza um enérgico trabalho na integração de bases de currículos acadêmicos de instituições públicas e privadas em uma única plataforma denominada Lattes. Os chamados ``Currículos Lattes'' são considerados um padrão nacional de avaliação representando um histórico das atividades científicas / acadêmicas / profissionais de pesquisadores cadastrados. Os currículos Lattes foram projetados para mostrar informação pública, embora, individual de cada usuário cadastrado na plataforma. Muitas vezes, realizar uma compilação ou sumarização de produções bibliográficas para um grupo de usuários cadastrados de médio ou grande porte (e.g. grupo de professores, departamento de pós-graduação) realmente requer um grande esforço mecânico que muitas vezes é suscetível a falhas.

O scriptLattes é um script GNU-GPL desenvolvido para a extração e compilação automática de: (1) produções bibliográficas, (2) produções técnicas, (3) produções artísticas, (4) orientações, (5) projetos de pesquisa, (6) prêmios e títulos, e (7) grafo de colaborações de um conjunto de pesquisadores cadastrados na plataforma Lattes. Associações de Qualis para as produções acadêmicas publicadas em Congressos e Revistas também são considerados.

O scriptLattes baixa automaticamente os currículos Lattes em formato HTML (livremente disponíveis na rede) de um grupo de pessoas de interesse, compila as listas de produções, tratando apropriadamente as produções duplicadas e similares. São geradas páginas HTML com listas de produções e orientações separadas por tipo e colocadas em ordem cronológica invertida. **Além dos relatórios HTML tradicionais, o sistema agora gera automaticamente arquivos JSON individuais para cada pesquisador, facilitando a análise de dados e integração com outras ferramentas.** Adicionalmente são criadas automaticamente vários grafos (redes) de co-autoria entre os membros do grupo de interesse e um mapa de geolocalização dos membros e alunos (de pós-doutorado, doutorado e mestrado) com orientação concluída. Os relatórios gerados permitem avaliar, analisar ou documentar a produção de grupos de pesquisa. Este projeto de software livre foi idealizado por Jesús P. Mena-Chalco e Roberto M. Cesar-Jr em 2005 (IME/USP).

O scriptLattes atualmente permite filtrar as produções científicas usando termos de pesquisa (Veja os exemplo teste-03).

## Pré-requisitos
- **Python 3**: Certifique-se de ter o Python 3 instalado no seu computador. 
  Se não tiver, você pode baixá-lo em [python.org](https://www.python.org/downloads/).
- **Google Chrome ou Chromium**: Necessário para o funcionamento do ChromeDriver.
- **jq**: Utilitário para processamento JSON (necessário para o Makefile):
  - Ubuntu/Debian: `sudo apt-get install jq`
  - CentOS/RHEL/Fedora: `sudo yum install jq` ou `sudo dnf install jq`
  - macOS: `brew install jq`
- **wget**: Para download do ChromeDriver (geralmente já instalado)

## Instalação Rápida (Recomendada)

Para uma instalação completa automatizada, use o Makefile incluído:

```bash
# Clone o repositório
git clone https://github.com/jpmenachalco/scriptLattes.git
cd scriptLattes

# Instalação completa (ambiente virtual + dependências + ChromeDriver)
make install
```

Este comando irá:
1. Criar um ambiente virtual Python
2. Instalar todas as dependências
3. Detectar automaticamente a versão do seu Chrome/Chromium
4. Baixar e configurar a versão correta do ChromeDriver

### Outros comandos úteis do Makefile:

```bash
make help                    # Mostra todos os comandos disponíveis
make status                  # Verifica o status da instalação
make test                    # Executa o exemplo de teste
make clean                   # Limpa arquivos temporários e cache
make update-chromedriver     # Atualiza o ChromeDriver
```

## Instalação Manual (Alternativa)

### 1. Clone este repositório para o seu computador
```bash
git clone https://github.com/jpmenachalco/scriptLattes.git
```

### 2. Navegue até o diretório do projeto
```bash
cd scriptLattes
```

### 3. Crie um ambiente virtual
```bash
python -m venv venv
```

#### Ative o ambiente virtual no Windows
```cmd
venv\Scripts\activate
```

#### Ative o ambiente virtual no Linux/Mac
```bash
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure o ChromeDriver manualmente
Baixe o ChromeDriver correspondente à versão do seu navegador em [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/). É importante que as versões sejam compatíveis.

## Execução do Programa

### Com Makefile (ambiente virtual gerenciado automaticamente):
```bash
make test
```

### Manual (certifique-se de que o ambiente virtual está ativado):
```bash
source venv/bin/activate  # Linux/Mac
python3 scriptLattes.py exemplo/teste-01.config
```

## Estrutura de Saída

O scriptLattes gera vários tipos de saída para análise dos dados extraídos:

### Relatórios HTML
- Páginas HTML interativas com tabelas organizadas por tipo de produção
- Gráficos de colaboração e visualizações em rede
- Mapas de geolocalização dos pesquisadores e orientandos

### **Novidade: Exportação JSON Individual**
A partir da versão atual, o scriptLattes gera automaticamente **arquivos JSON individuais para cada pesquisador** na pasta `json/` do diretório de saída.

**Estrutura do JSON por pesquisador:**
- `informacoes_pessoais`: Dados básicos do pesquisador (Nome, ID Lattes, endereço profissional, etc.)
- `formacao_academica`: Histórico de formação acadêmica
- `projetos_pesquisa`: Lista completa de projetos de pesquisa com detalhes
- `areas_atuacao`: Áreas de atuação e especialidades
- `producao_bibliografica`: Artigos, livros, capítulos, trabalhos em congressos
- `producao_tecnica`: Softwares, produtos tecnológicos, trabalhos técnicos
- `patentes_registros`: Patentes, programas de computador, desenhos industriais
- `producao_artistica`: Produções artísticas e culturais
- `orientacoes`: Orientações em andamento e concluídas (todas as modalidades)
- `eventos`: Participações e organizações de eventos
- `premios_titulos`: Prêmios e títulos recebidos
- `idiomas`: Idiomas conhecidos
- `estatisticas`: Resumo quantitativo das produções

**Exemplo de uso dos dados JSON:**
```bash
# Listar todos os projetos de pesquisa de um pesquisador
jq '.projetos_pesquisa[].nome' json/01_Daniel-Cruz-Cavalieri_*.json

# Obter estatísticas de produção
jq '.estatisticas' json/00_Paulo-Sergio-*.json

# Extrair todos os artigos publicados em periódicos
jq '.producao_bibliografica.artigos_periodicos' json/*.json
```

### Arquivos de Dados Estruturados
- **CSV/Excel**: Tabelas exportáveis para análise em planilhas
- **GDF**: Formato para análise de redes em ferramentas como Gephi
- **TXT**: Listas simples de produções

## Solução de Problemas Comuns

### Erro de incompatibilidade do ChromeDriver
Se você receber um erro como "This version of ChromeDriver only supports Chrome version X", execute:
```bash
make update-chromedriver
```

### Verificar status da instalação
```bash
make status
```

### Chrome/Chromium não encontrado
Certifique-se de ter o Google Chrome ou Chromium instalado:
- Ubuntu/Debian: `sudo apt-get install google-chrome-stable` ou `sudo apt-get install chromium-browser`
- CentOS/RHEL/Fedora: Baixe do site oficial do Google Chrome
- macOS: Baixe do site oficial do Google Chrome

### Problemas com dependências
Se houver problemas com as dependências Python:
```bash
make clean-all  # Remove tudo
make install    # Reinstala do zero
```

## Comunicação
- Temos uma área no Discord que pode ser útil para compartilhar dúvidas/sugestões [https://discord.gg/Xz8NZ3kBc3]
- Contato direto: [jesus.mena@ufabc.edu.br]

## Como referenciar este software
- J. P. Mena-Chalco e R. M. Cesar-Jr. scriptLattes: An open-source knowledge extraction system from the Lattes platform. Journal of the Brazilian Computer Society, vol. 15, n. 4, páginas 31--39, 2009. [http://dx.doi.org/10.1007/BF03194511]
- J. P. Mena-Chalco e R. M. Cesar-Jr. Prospecção de dados acadêmicos de currículos Lattes através de scriptLattes. Capítulo do livro Bibliometria e Cientometria: reflexões teóricas e interfaces São Carlos: Pedro & João, páginas 109-128, 2013. [http://dx.doi.org/10.13140/RG.2.1.5183.8561]

## Notas:
- O scriptLattes não está vinculado ao CNPq. A ferramenta é o resultado de um esforço (independente) realizado com o único intuito de auxiliar as tarefas mecânicas de compilação de informações cadastradas nos Currículos Lattes (publicamente disponíveis). Portanto, o CNPq não é responsável por nenhuma assessoria técnica sobre esta ferramenta.
- O repositorio antigo, no sourceforge não está sendo atualizado.


