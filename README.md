# Programa de Metas V2.0

Backend e Painel Administrativo do Programa de Metas V2.0.

## Sobre o projeto

O Programa de Metas V2.0 está sendo reconstruído com o objetivo de substituir o backend anterior por uma arquitetura mais organizada, persistente, modular e de fácil manutenção.

O backend será responsável por:

* fornecer informações ao frontend por API;
* armazenar dados de forma persistente;
* administrar usuários e acessos;
* permitir manutenção dos dados;
* receber informações para análise;
* importar dados de APIs externas;
* importar informações por Excel;
* permitir cadastramento manual;
* armazenar informações relacionadas a imagens e mapas;
* gerar dados para relatórios e impressão;
* futuramente fornecer dados para dashboards;
* manter histórico e consistência das informações.

O projeto segue princípios de:

* Clean Code;
* Clean Architecture;
* SOLID;
* Separation of Concerns;
* DRY;
* KISS;
* baixo acoplamento;
* alta coesão.

---

# Tecnologias

Atualmente o projeto utiliza:

| Tecnologia         | Responsabilidade                             |
| ------------------ | -------------------------------------------- |
| Python 3.12        | Linguagem principal                          |
| Reflex 0.9.8.post1 | Interface administrativa e aplicação         |
| FastAPI            | Backend utilizado pelo Reflex e futura API   |
| PostgreSQL 18      | Banco de dados                               |
| SQLModel           | Modelagem ORM                                |
| SQLAlchemy         | Comunicação ORM com banco                    |
| Alembic            | Migrations                                   |
| Psycopg 3          | Driver PostgreSQL                            |
| Argon2 / pwdlib    | Hash seguro de senhas                        |
| Docker             | Infraestrutura local                         |
| Docker Compose     | Orquestração dos serviços                    |
| uv                 | Dependências e ambiente Python               |
| Node.js 22.12+     | Dependências do frontend gerado pelo Reflex  |
| Bun                | Gerenciamento frontend utilizado pelo Reflex |

---

# Controle de acesso

Toda a implementação relacionada a autenticação está centralizada em:

```text
Back_end/access/
```

Essa área atualmente é responsável por:

* usuários;
* hash de senha;
* login;
* sessões;
* tokens;
* cookies;
* logout;
* proteção das páginas administrativas.

Existe documentação específica em:

```text
Back_end/access/README.md
```

---

# Banco de dados

O banco principal é PostgreSQL 18.

O PostgreSQL roda em Docker, separado da aplicação Reflex.

A aplicação utiliza:

```text
Reflex
   ↓
SQLModel
   ↓
SQLAlchemy
   ↓
Psycopg
   ↓
PostgreSQL
```

---

# Persistência

Os dados do PostgreSQL ficam em um volume Docker externo:

```text
pdm_postgres_data
```

Esse volume não pertence ao ciclo de vida do Docker Compose.

Por isso os dados permanecem mesmo após:

```powershell
docker compose down
```

e:

```powershell
docker compose down --volumes
```

O volume foi criado com:

```powershell
docker volume create pdm_postgres_data
```

O `compose.yaml` utiliza:

```yaml
volumes:
  pdm_postgres_data:
    external: true
```

## Atenção

Não executar em um ambiente com dados importantes:

```powershell
docker volume rm pdm_postgres_data
```

Esse comando remove explicitamente o armazenamento do banco.

Volume persistente também não substitui backup.

Uma estratégia de backup e restauração deverá ser implementada antes da entrada em produção.

---

# Pré-requisitos

Para desenvolvimento local é necessário:

* Git;
* Python;
* uv;
* Docker Desktop;
* Node.js 22.12 ou superior;
* NVM para Windows, recomendado;
* Reflex.

Versões utilizadas durante o desenvolvimento inicial:

```text
Python:     3.12.13
Reflex:     0.9.8.post1
Node.js:    22.12.0
PostgreSQL: 18
Psycopg:    3.3.4
SQLAlchemy: 2.0.52
SQLModel:   0.0.39
Alembic:    1.19.1
pwdlib:     0.3.1
```

---

# Configurando Node.js

No Windows com NVM:

```powershell
nvm install 22.12.0
nvm use 22.12.0
```

Confirme:

```powershell
node --version
```

Resultado esperado:

```text
v22.12.0
```

---

# Instalando dependências do projeto

Após clonar o projeto:

```powershell
uv sync
```

O `uv` utilizará:

```text
pyproject.toml
uv.lock
```

para restaurar as dependências.

Não é necessário executar novamente os comandos `uv add` usados durante a criação inicial do projeto.

---

# Variáveis de ambiente

O projeto utiliza:

```text
.env
```

para valores locais e secretos.

Existe também:

```text
.env.example
```

que documenta quais variáveis são necessárias.

Exemplo:

```env
APP_ENV=development

POSTGRES_DB=pdm_v2
POSTGRES_USER=pdm_admin
POSTGRES_PASSWORD=

REFLEX_DB_URL=
REFLEX_ASYNC_DB_URL=
```

Crie seu `.env` local com os valores reais.

## Nunca versionar

```text
.env
```

Ele deve estar no `.gitignore`.

O arquivo:

```text
.env.example
```

deve ser versionado.

---

# Banco PostgreSQL

Antes de executar o projeto, o Docker Desktop precisa estar iniciado.

## Criar o volume

Esse comando só é necessário na primeira configuração da máquina:

```powershell
docker volume create pdm_postgres_data
```

Confirme:

```powershell
docker volume ls
```

---

# Subindo o PostgreSQL

```powershell
docker compose up -d postgres
```

Verifique:

```powershell
docker compose ps
```

Resultado esperado:

```text
pdm_postgres   ...   Up ... (healthy)
```

Logs:

```powershell
docker compose logs postgres
```

---

# Acessando PostgreSQL

```powershell
docker exec -it pdm_postgres psql -U pdm_admin -d pdm_v2
```

Dentro do PostgreSQL:

```sql
\dt
```

Para sair:

```sql
\q
```

---

# Migrations

O banco utiliza Alembic.

As migrations ficam em:

```text
alembic/versions/
```

Atualmente existem migrations para:

```text
users
user_sessions
```

## Aplicando migrations existentes

Após clonar o projeto ou atualizar o código:

```powershell
uv run reflex db migrate
```

---

# Criando uma nova migration

Após alterar um model:

```powershell
uv run reflex db makemigrations --message "descricao da alteracao"
```

Exemplo:

```powershell
uv run reflex db makemigrations --message "add user role"
```

Antes de aplicar, revisar o arquivo criado em:

```text
alembic/versions/
```

Depois:

```powershell
uv run reflex db migrate
```

## Regra importante

Não apagar migrations já aplicadas para alterar o banco.

A evolução deve ser:

```text
migration 001
    ↓
migration 002
    ↓
migration 003
```

e não:

```text
alterou model
    ↓
apaga banco
```

---

# Executando o projeto

Primeiro confirme que o PostgreSQL está ativo:

```powershell
docker compose ps
```

Depois:

```powershell
uv run reflex run
```

Aplicação:

```text
http://localhost:3000/
```

Backend:

```text
http://localhost:8000/
```

---

# Rotina diária de desenvolvimento

Ao iniciar o trabalho:

```powershell
docker compose up -d postgres
```

Depois:

```powershell
uv run reflex run
```

Ao terminar o Reflex:

```text
Ctrl + C
```

Se quiser desligar o PostgreSQL também:

```powershell
docker compose down
```

Os dados continuarão armazenados no volume externo.

---

# Criando usuário

Existe um script administrativo:

```text
scripts/create_user.py
```

Execute:

```powershell
uv run python -m scripts.create_user
```

O script solicitará:

```text
Nome
E-mail
Senha
Confirmação da senha
```

A senha não é armazenada diretamente.

Ela é transformada em hash Argon2 antes de chegar ao banco.

---

# Segurança

Atualmente:

* senhas usam Argon2;
* senha original nunca é armazenada;
* tokens de sessão são gerados com `secrets`;
* banco armazena somente hash SHA-256 do token;
* sessões possuem expiração;
* sessões podem ser revogadas;
* páginas administrativas validam sessão no backend;
* `.env` não deve ser versionado.

## Produção

Antes da produção ainda será necessário revisar:

* cookies `HttpOnly`;
* `Secure=true`;
* HTTPS;
* autenticação institucional da PMSP, se disponível;
* política de duração de sessão;
* rate limiting;
* proteção contra brute force;
* auditoria;
* política de senhas;
* perfis e permissões;
* backup e restauração;
* configuração de produção do PostgreSQL.

---

# Problemas comuns

## PostgreSQL não conecta

Erro semelhante:

```text
connection timeout
localhost:5432
```

Primeiro confirme se o Docker Desktop está aberto.

Depois:

```powershell
docker compose ps
```

Se necessário:

```powershell
docker compose up -d postgres
```

---

## Problemas no frontend gerado pelo Reflex

A pasta:

```text
.web/
```

é gerada automaticamente.

Em caso de conflito de dependências frontend, ela pode ser reconstruída:

```powershell
Remove-Item -Recurse -Force .web
```

Depois:

```powershell
uv run reflex run
```

Não remover:

```text
reflex.lock/
uv.lock
pyproject.toml
rxconfig.py
Back_end/
```

---

## Node.js antigo

Caso apareça aviso indicando Node inferior a 22.12:

```powershell
nvm install 22.12.0
nvm use 22.12.0
```

---

# Regra principal do projeto

Código pode ser reconstruído.

Dados não.

A aplicação deve ser desenvolvida de forma que alterações de código, deploys, rebuilds ou reinicializações de containers não destruam os dados persistidos pelo Programa de Metas.
