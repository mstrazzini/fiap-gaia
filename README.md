# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Projeto GAIA - Irrigação Inteligente

## Responsável
- <a href="https://www.linkedin.com/in/mstrazzini">Marcos Trazzini (RM559926)</a>


## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Tutor</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Coordenador</a>


## 📜 Descrição

A solução desenvolvida tem como objetivo implementar um sistema de automação de controle de irrigação agrícola, voltado para o monitoramento e gerenciamento eficiente de áreas de plantação. O projeto foi criado para atender à necessidade de registrar e monitorar processos de irrigação em áreas específicas, além de capturar e exibir leituras de sensores de solo. A solução é construída como uma aplicação CLI (Command Line Interface) em Python, integrando-se com um banco de dados Oracle para gerenciar os dados de irrigação e leituras de sensores de forma persistente.

Essa solução oferece uma abordagem prática para o controle de irrigação em áreas agrícolas, permitindo:

* Gerenciamento eficiente do uso de água;
* Monitoramento em tempo real das condições do solo através de sensores;
* Registro e consulta de históricos de irrigação e leituras de sensores, o que facilita a tomada de decisões informadas para otimizar a produtividade das plantações.

A solução proposta é escalável e pode ser expandida para incluir novos sensores, áreas de plantio e funcionalidades adicionais, como relatórios avançados e integração com sistemas de previsão climática.

## :game_die: Estrutura de dados da Solução

A aplicação foi desenvolvida com base em uma arquitetura de banco de dados relacional no Oracle, utilizando as seguintes tabelas principais:
1. **AREAS**: Armazena as informações de cada área de plantação, como o nome, o tamanho (em hectares) e o tipo de cultura plantada.
2. **IRRIGACOES**: Registra os processos de irrigação, incluindo a área irrigada, a data/hora de início e fim da irrigação e a quantidade de água utilizada.
3. **SENSORES**: Contém informações sobre os sensores instalados nas áreas, que monitoram a umidade do solo, o pH e os níveis de nutrientes (nitrogênio, fósforo e potássio).
4. **LEITURAS_SENSORES**: Armazena as leituras dos sensores para cada área, incluindo a data/hora da leitura, o tipo de sensor e o valor coletado.
5. **FATORES_IRRIGACAO**: Mantém os fatores de irrigação específicos para cada tipo de cultura, que são aplicados no cálculo da quantidade de água necessária para irrigação.

## Funcionalidades Implementadas

### Registro de Irrigação

Uma das principais funcionalidades da solução é a possibilidade de registrar novos processos de irrigação para áreas específicas. O usuário insere a data e hora de início e fim da irrigação, e o sistema calcula automaticamente a quantidade de água necessária com base em:

* O tamanho da área (em hectares);
* O tempo total de irrigação;
* O fator de irrigação específico da cultura plantada naquela área (armazenado na tabela FATORES_IRRIGACAO).

O cálculo da quantidade de água considera que cada hectare de plantação requer 100 litros de água por hora, ajustado pelo fator de irrigação da cultura.

### Consulta de Processos de Irrigação

A aplicação permite consultar os processos de irrigação registrados para uma determinada área, exibindo a data de início, data de fim e a quantidade de água utilizada em cada irrigação. Isso facilita o acompanhamento histórico das atividades de irrigação e a eficiência do uso de recursos hídricos.

### Monitoramento de Sensores

Os sensores instalados nas áreas de plantação são responsáveis por capturar leituras regulares de umidade, pH do solo e níveis de nutrientes. A aplicação permite consultar as últimas 10 leituras de cada sensor (umidade, pH, nitrogênio, fósforo e potássio) para uma área específica. Essas informações são essenciais para que o agricultor possa ajustar o processo de irrigação e o manejo das áreas com base nas condições do solo. Com base nos dados coletados, futuramente será possível implementar mecanismos de análise mais robustos, com estatísticas, gráficos e previsões utilizando modelos de Machine Learning.

### Carga de Dados de Sensores

Um script adicional foi implementado para carregar automaticamente leituras de sensores a partir de um arquivo CSV para o banco de dados Oracle. O script verifica se a leitura já existe (com base na área, sensor e data/hora) e, caso exista, atualiza o valor. Se a leitura for nova, ela é inserida no banco de dados.


## Preparando o ambiente

### Requisitos do Sistema

Antes de iniciar a preparação e execução da aplicação de controle de irrigação, é importante garantir que todos os requisitos de software e infraestrutura estão atendidos.

* __Sistema Operacional__: Linux, macOS ou Windows.
* __Python__: Versão 3.10 ou superior.
    * É recomendado o uso de um ambiente virtual (venv) para gerenciar as dependências da aplicação.
* __Banco de Dados__: Oracle Database 12c ou superior (Foi utilizado o Oracle 23c Free durante o desenvolvimento). Pode ser instalado localmente, em um host/vm separado ou na nuvem. Basta alterar as variáveis de conexão (mais especificamente, a variável `GAIA_DB_DSN`) conforme necessário. Certifique-se de possuir permissões adequadas para manipulação de tabelas no banco.
* __Pacotes Python__: (basta instalar com`pip install pacote`)
    * `oracledb`: Para conexão e manipulação do banco de dados Oracle.
    * `csv` (módulo nativo do Python): Para leitura de arquivos CSV contendo os dados dos sensores.

### Estrutura de Diretórios do Projeto
* scripts/: Contém scripts para preparação e carga de dados.

    * `estrutura_banco.sql`: Script SQL para criar as tabelas necessárias.
    * `gera_dados_sensores.py`: Gera dados simulados dos sensores.
    * `carrega_dados_sensores.py`: Faz a carga dos dados simulados no banco de dados Oracle.

* src/: Contém a aplicação principal.

    * `main.py`: Script principal da aplicação CLI para registrar e consultar processos de irrigação e leituras de sensores.

### Variáveis de Ambiente
As seguintes variáveis de ambiente devem ser configuradas para garantir a conexão com o banco de dados Oracle:

* `GAIA_DB_USER`: Usuário do banco de dados Oracle.
* `GAIA_DB_PASSWORD`: Senha do banco de dados Oracle.
* `GAIA_DB_DSN`: Data Source Name (DSN), composto pelo host, porta e nome do serviço Oracle.

### Preparação do Banco de Dados Oracle
Antes de executar a aplicação, você precisa configurar o banco de dados Oracle utilizando o script SQL que cria a estrutura das tabelas necessárias.

Passo-a-passo:

1. Conecte-se ao banco de dados Oracle utilizando uma ferramenta como __SQL*Plus__ ou qualquer cliente de banco de dados compatível (como SQL Developer).
2. Navegue até o diretório onde o arquivo `scripts/estrutura_banco.sql` está localizado.
3. Execute o seguinte comando para preparar o banco de dados:
    ```
    @/caminho_para_o_arquivo/scripts/estrutura_banco.sql
    ```

### Geração dos dados dos sensores
Como a aplicação necessita de dados de sensoriamento já previamente carregados no banco de dados, e no momento não temos essa funcionalidade ainda implementada, podemos utilizar o procedimento a seguir para carregar o banco de dados com uma amostragem de leituras aleatórias dos sensores:
`
Passo-a-passo:

1. Navegue até o diretório `scripts/`
2. Execute o script Python que gera os dados dos sensores:
    ```
    python ./gera_dados_sensores.py
    ```
3. O script não dá nenhuma saída no terminal (o que é bom sinal!), mas deve gerar um arquivo `dados_sensores.csv`, que será uilizado na próxima etapa.

### Carregando dados de sensoriamento no banco
Após gerar os dados dos sensores, você pode carregar esses dados no banco de dados Oracle utilizando o script `carrega_dados_sensores.py`.

Passo-a-passo:

1. Navegue até o diretório `scripts/`
2. Execute o seguinte comando para carregar os dados dos sensores:
    ```
    python ./carrega_dados_sensores.py dados_sensores.csv
    ```
3. Caso a carga tenha sido bem sucedida, o script retornará a mensagem `Dados carregados com sucesso!` 

## 🔧 Como executar o código

Com o ambiente devidamente preparado, basta executar o script src/main.py para rodar a aplicação principal:
```
python src/main.py
```

A aplicação exibe um menu com as seguintes opções:
```
1. Registrar irrigação
2. Consultar processos de irrigação
3. Consultar leituras de sensores
4. Sair
```

* __Registrar irrigação__: Insira o ID da área e as datas de início e fim da irrigação. A aplicação calculará a quantidade de água necessária e registrará o processo.
* __Consultar processos de irrigação__: Exibe os processos de irrigação registrados para uma área específica.
* __Consultar leituras de sensores__: Exibe as últimas 10 leituras de sensores (umidade, pH e nutrientes) de uma área.


## 🗃 Histórico de lançamentos

* 0.1.0 - 15/10/2024
    * Versão inicial, CLI, com recursos básicos de sensoriamento simulado e carga de dados no banco oracle.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


