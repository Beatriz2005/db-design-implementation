# Interface das Funcionalidadas 
## Projeto de Banco de Dando de um Portal da Energia e Iluminação
Matéria de Projeto e Implementação de Banco de Dados - PIBD - UFSCAR

### Funcionalidades Implementadas
- Cadastro de Usuários
Cadastra dados de novos usuários chamando o procedimento CadastrarNovoUsuarioCompleto, criado na etapa 3. Dentro deste procedimento ocorre inserção na tabela USUARIO e inserção na tabela de subtipo correspondente (USUARIOCOMUM ou ORGAOPUBLICO).

- Cadastro de Imóveis
Cadastra imóveis de propriedade de um usuário. Inserção na tabela LOCALIZACAO. Inserção na tabela IMOVEL passando como chave estrangeira  o id da localização criada anteriormente. Inserção na tabela USUARIO_IMOVEL (relacionamento), que vincula um usuário ao imóvel cadastrado. 


- Listagem do Número de Imóveis por usuário
Gera uma lista contendo todos os usuários e a quantidade de imóveis vinculados a cada um. Chamada da função ContarImoveisPorUsuario dentro de um SELECT. Essa função foi criada na etapa 3 e faz um SELECT COUNT(*) na tabela USUARIO_IMOVEL (relacionamento).
