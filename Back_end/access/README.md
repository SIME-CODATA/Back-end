# Access

Módulo responsável pelo controle de acesso ao Painel Administrativo do Programa de Metas V2.0.

Todo código relacionado diretamente a:

* usuários;
* senhas;
* autenticação;
* login;
* logout;
* sessões;
* tokens;
* cookies;
* validação de sessão;

deve ficar centralizado neste módulo.

---

# Estrutura

```text
access/
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── session.py
│
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   └── session_service.py
│
├── pages/
│   ├── __init__.py
│   ├── login.py
│   └── logout.py
│
├── __init__.py
├── security.py
├── state.py
└── README.md
```

A organização segue:

```text
Models
   ↓
estrutura dos dados

Services
   ↓
regras e operações

State
   ↓
integração entre Reflex e serviços

Pages
   ↓
interface

Security
   ↓
funções criptográficas
```

---

# models/user.py

Responsável pelo modelo de usuário.

Tabela:

```text
users
```

Estrutura atual:

```text
users
├── id
├── name
├── email
├── password_hash
└── is_active
```

## id

Identificador único do usuário.

É a chave primária da tabela.

---

## name

Nome do usuário.

Exemplo:

```text
João Banana
```

---

## email

E-mail utilizado para autenticação.

Possui:

```text
UNIQUE
INDEX
```

para impedir usuários duplicados e facilitar consultas.

O serviço normaliza o e-mail para letras minúsculas.

---

## password_hash

Hash da senha.

Nunca contém a senha original.

Exemplo:

```text
$argon2id$...
```

A senha é processada utilizando Argon2.

---

## is_active

Define se o usuário pode autenticar.

```text
true
```

Usuário ativo.

```text
false
```

Usuário desativado.

Mesmo que a senha esteja correta, um usuário desativado não deve conseguir entrar.

---

# models/session.py

Responsável pelas sessões autenticadas.

Tabela:

```text
user_sessions
```

Estrutura:

```text
user_sessions
├── id
├── user_id
├── token_hash
├── created_at
├── expires_at
└── revoked_at
```

---

## user_id

Foreign key:

```text
user_sessions.user_id
        ↓
users.id
```

Identifica quem é o dono da sessão.

---

## token_hash

O token original nunca é armazenado no banco.

O navegador recebe o token.

O PostgreSQL recebe:

```text
SHA-256(token)
```

---

## created_at

Momento em que a sessão foi criada.

Utiliza UTC.

---

## expires_at

Momento em que a sessão deixa automaticamente de ser válida.

A duração atual da sessão é:

```text
8 horas
```

---

## revoked_at

Momento em que a sessão foi explicitamente revogada.

Exemplo:

```text
logout
    ↓
revoked_at = agora
```

Uma sessão com `revoked_at` preenchido não pode ser reutilizada.

---

# security.py

Responsável pelas funções relacionadas à segurança das senhas.

Utiliza:

```text
pwdlib
Argon2
```

Possui atualmente:

```python
hash_password()
verify_password()
```

---

## hash_password()

Recebe:

```text
senha original
```

e retorna:

```text
hash Argon2
```

Fluxo:

```text
Senha
   ↓
hash_password()
   ↓
Argon2
   ↓
password_hash
   ↓
PostgreSQL
```

A senha original não é salva.

---

## verify_password()

Recebe:

```text
senha digitada
+
hash armazenado
```

e retorna:

```text
True
```

ou:

```text
False
```

Fluxo:

```text
Senha informada
       ↓
verify_password()
       ↑
password_hash
       ↓
True / False
```

---

# services/user_service.py

Responsável pelas regras relacionadas aos usuários.

A página de login não deve consultar diretamente o PostgreSQL.

Ela deve conversar com o serviço.

Atualmente possui:

```python
create_user()
authenticate_user()
```

---

## create_user()

Responsável por criar um usuário.

Fluxo:

```text
nome
email
senha
   ↓
normalização
   ↓
validação
   ↓
verificação de duplicidade
   ↓
hash da senha
   ↓
User
   ↓
PostgreSQL
```

Também impede a criação de outro usuário com o mesmo e-mail.

---

## authenticate_user()

Responsável por validar credenciais.

Fluxo:

```text
email + senha
      ↓
normalização
      ↓
busca User
      ↓
usuário existe?
      ↓
está ativo?
      ↓
verify_password()
      ↓
User ou None
```

Para evitar enumeração de usuários, a interface exibe a mesma mensagem para:

```text
e-mail inexistente
```

e:

```text
senha incorreta
```

Mensagem atual:

```text
E-mail ou senha inválidos.
```

---

# services/session_service.py

Responsável pelas sessões autenticadas.

Atualmente possui:

```python
create_session()
validate_session()
revoke_session()
```

Além de funções auxiliares relacionadas ao token.

---

## create_session()

Recebe:

```text
user_id
```

Gera um token criptograficamente seguro com:

```python
secrets.token_urlsafe()
```

Fluxo:

```text
user_id
   ↓
token aleatório
   ↓
SHA-256
   ↓
UserSession
   ↓
PostgreSQL
```

O token original é retornado para a camada de autenticação.

O banco recebe apenas o hash.

---

## validate_session()

Recebe o token enviado pelo navegador.

Fluxo:

```text
token
   ↓
SHA-256
   ↓
procura token_hash
   ↓
sessão existe?
   ↓
revoked_at é NULL?
   ↓
expires_at ainda é válido?
   ↓
user_id
```

Retorna:

```text
user_id
```

quando válido.

Retorna:

```text
None
```

quando inválido.

---

## revoke_session()

Utilizado principalmente no logout.

Fluxo:

```text
token
   ↓
token_hash
   ↓
busca sessão
   ↓
revoked_at = agora
```

Mesmo que o token antigo ainda exista no navegador ou em algum outro local, ele não será aceito novamente.

---

# state.py

Contém:

```python
AuthState
```

O `AuthState` é a ponte entre a interface Reflex e os serviços de autenticação.

Ele não deve concentrar regras de negócio que pertencem aos services.

Responsabilidades atuais:

* receber formulário de login;
* chamar `authenticate_user()`;
* criar sessão;
* armazenar token no cookie;
* validar acesso às páginas protegidas;
* executar logout;
* redirecionar páginas;
* manter informações internas de autenticação.

---

# Cookie de sessão

O token do navegador utiliza:

```text
pdm_session
```

O cookie possui atualmente configuração adequada ao desenvolvimento local.

Entre as configurações estão:

```text
path=/
max_age=8 horas
same_site=strict
```

Durante desenvolvimento local:

```text
secure=False
```

Antes da produção essa configuração deve ser revista.

---

# Variável backend-only

O ID do usuário autenticado é mantido como variável backend-only.

Exemplo:

```python
_authenticated_user_id
```

Por começar com `_`, essa variável não deve ser tratada como estado público da interface.

Informações sensíveis devem permanecer no servidor sempre que possível.

---

# pages/login.py

Página:

```text
/login
```

Responsável pela interface de autenticação.

Possui atualmente:

* título;
* identificação do Painel Administrativo;
* campo de e-mail;
* campo de senha;
* botão Entrar;
* mensagem de erro.

O formulário envia os dados para:

```python
AuthState.login
```

A página não acessa diretamente:

```text
PostgreSQL
SQLModel
Argon2
UserSession
```

Essas responsabilidades pertencem aos services.

---

# Fluxo completo de login

```text
/login
   ↓
Usuário informa e-mail e senha
   ↓
AuthState.login
   ↓
authenticate_user()
   ↓
PostgreSQL
   ↓
verify_password()
   ↓
credenciais válidas
   ↓
create_session()
   ↓
token
   ↓
cookie pdm_session
   ↓
redirect
   ↓
/admin
```

---

# Login inválido

Quando as credenciais não forem válidas:

```text
authenticate_user()
   ↓
None
   ↓
AuthState
   ↓
"E-mail ou senha inválidos."
```

O sistema não informa se:

* o e-mail não existe;
* a senha está incorreta;
* a conta está inativa.

---

# Proteção do Admin

A página:

```text
/admin
```

utiliza:

```python
AuthState.require_auth
```

ao carregar.

Fluxo:

```text
/admin
   ↓
require_auth()
   ↓
cookie
   ↓
validate_session()
   ↓
sessão válida?
```

Se válida:

```text
permanece /admin
```

Se inválida:

```text
/login
```

---

# pages/logout.py

Página:

```text
/logout
```

Responsável pelo encerramento da sessão.

Ao carregar:

```python
AuthState.logout
```

é executado.

---

# Fluxo de logout

```text
/admin
   ↓
Sair
   ↓
/logout
   ↓
AuthState.logout
   ↓
revoke_session()
   ↓
revoked_at
   ↓
remove cookie
   ↓
/login
```

A sessão deixa de ser válida no servidor.

---

# Criando usuário

O cadastro inicial de usuários pode ser feito através do script:

```text
scripts/create_user.py
```

Execute na raiz do projeto:

```powershell
uv run python -m scripts.create_user
```

Será solicitado:

```text
Nome:
E-mail:
Senha:
Confirme a senha:
```

A senha é digitada usando `getpass`, portanto não aparece no terminal.

O script deve utilizar:

```text
Back_end.access.services.user_service
```

para criar o usuário.

Nunca deve duplicar a lógica de criação.

---

# Consultando usuários

Entre no PostgreSQL:

```powershell
docker exec -it pdm_postgres psql -U pdm_admin -d pdm_v2
```

Consulta:

```sql
SELECT
    id,
    name,
    email,
    is_active
FROM users;
```

---

# Consultando sessões

```sql
SELECT
    id,
    user_id,
    created_at,
    expires_at,
    revoked_at
FROM user_sessions
ORDER BY id DESC;
```

Para verificar somente parte do hash:

```sql
SELECT
    id,
    user_id,
    LEFT(token_hash, 12) AS token_hash,
    created_at,
    expires_at,
    revoked_at
FROM user_sessions;
```

Não é necessário visualizar o token real, pois ele não é armazenado.

---

# Testando o serviço de sessão manualmente

Abra o Python:

```powershell
uv run python
```

Importe:

```python
from Back_end.access.services.session_service import (
    create_session,
    validate_session,
    revoke_session,
)
```

Crie uma sessão:

```python
token = create_session(2)
```

Valide:

```python
print(validate_session(token))
```

Resultado esperado:

```text
2
```

Token inválido:

```python
print(validate_session("token-falso"))
```

Resultado:

```text
None
```

Revogue:

```python
print(revoke_session(token))
```

Resultado:

```text
True
```

Valide novamente:

```python
print(validate_session(token))
```

Resultado:

```text
None
```

---

# Foreign Key entre sessões e usuários

`UserSession` depende de `User`.

Portanto o model da sessão precisa garantir que o model do usuário esteja registrado na metadata do SQLModel.

A relação é:

```text
User
  ↑
  │ users.id
  │
UserSession.user_id
```

Essa dependência não deve ser removida sem alterar também o modelo e a migration correspondente.

---

# Migrations relacionadas ao Access

Atualmente:

```text
77e010501735
create users table
        ↓
547355594417
create user sessions table
```

A revision atual do Alembic pode ser consultada no PostgreSQL:

```sql
SELECT * FROM alembic_version;
```

---

# Alterando models

Depois de alterar:

```text
models/user.py
```

ou:

```text
models/session.py
```

gere uma nova migration:

```powershell
uv run reflex db makemigrations --message "descricao"
```

Revise o arquivo criado.

Depois:

```powershell
uv run reflex db migrate
```

Nunca apagar migrations já aplicadas em produção para recriar tabelas do zero.

---

# Dependências entre camadas

O fluxo desejado é:

```text
Pages
   ↓
State
   ↓
Services
   ↓
Models / Security
   ↓
Database
```

Evitar:

```text
Page
   ↓
SQL direto
```

ou:

```text
State
   ↓
hash implementado novamente
```

ou:

```text
Script
   ↓
INSERT manual duplicando regra
```

A regra deve existir em um único lugar.

---

# Componentes

Atualmente as páginas de acesso utilizam componentes Reflex diretamente.

Ainda não existem componentes próprios suficientes para justificar:

```text
access/components/
```

Caso elementos reutilizáveis apareçam, essa pasta poderá ser criada.

Exemplos futuros:

```text
access/
└── components/
    ├── login_form.py
    ├── password_input.py
    └── access_card.py
```

A pasta deve ser criada somente quando houver reutilização ou complexidade real.

---

# Responsabilidades que não pertencem ao Access

O módulo `access` não deve receber regras relacionadas a:

* Metas;
* Eixos;
* Notícias;
* SMAE;
* Excel;
* Relatórios;
* Mapas;
* Dashboard.

Essas funcionalidades terão módulos próprios.

A responsabilidade de `access` termina na identidade, autenticação e autorização do usuário.

---

# Segurança antes da produção

Itens ainda pendentes para produção:

* [ ] Cookie HttpOnly
* [ ] Cookie Secure
* [ ] HTTPS
* [ ] política de senha
* [ ] proteção contra brute force
* [ ] rate limiting
* [ ] perfis
* [ ] permissões
* [ ] auditoria de login
* [ ] controle de tentativas
* [ ] limpeza de sessões expiradas
* [ ] revogação de todas as sessões
* [ ] integração institucional, caso disponível

---

# Estado atual

* [x] User
* [x] senha com Argon2
* [x] criação de usuário
* [x] autenticação por e-mail e senha
* [x] UserSession
* [x] token criptograficamente seguro
* [x] hash do token
* [x] cookie
* [x] proteção do `/admin`
* [x] sessão persistente
* [x] logout
* [x] revogação da sessão