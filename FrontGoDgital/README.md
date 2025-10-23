# goDigital Code! - Sistema de Gestão Full-Stack para Padarias

![Java](https://img.shields.io/badge/Java-17-blue) ![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.x-green) ![React](https://img.shields.io/badge/React-18-blue) ![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

Sistema de gestão completo e robusto para micro e pequenas empresas, focado em otimizar operações, fornecer inteligência de negócio e garantir conformidade legal.

## 🎯 Conceito do Projeto

O goDigital Code! foi projetado para resolver os desafios centrais de gestão de pequenos negócios, como padarias, que frequentemente dependem de processos manuais. A solução centraliza o controle de vendas, estoque, clientes e finanças em uma plataforma única, intuitiva e segura, transformando dados operacionais em insights estratégicos.

## ✨ Funcionalidades Implementadas

O sistema é dividido em três pilares de valor:

###  Gestão Operacional
- **Ponto de Venda (PDV):** Registro rápido de vendas com busca de produtos e clientes.
- **Gestão de Produtos e Categorias:** CRUD completo para o catálogo.
- **Controle de Estoque:** Ajustes de entrada/saída e alertas automáticos de estoque baixo.
- **Gestão de Clientes:** Cadastro e gerenciamento da base de clientes.
- **Programa de Fidelidade:** Sistema de pontos integrado ao PDV.
- **Impressão de Cupons:** Geração de recibos de venda.

### 📈 Gestão Financeira e Estratégica
- **Dashboard Principal:** KPIs diários (faturamento, nº de vendas, produto mais vendido).
- **Dashboard Financeiro:** Análise de Receitas, Despesas e Lucro com filtros por período.
- **Evolução de Faturamento:** Gráfico dinâmico para análise de performance.
- **Gestão de Despesas:** CRUD completo para lançamentos de saídas (custos, salários, etc.).
- **Metas Financeiras:** Criação e acompanhamento de metas de faturamento.
- **Alertas Proativos:** Notificações de aniversariantes do dia para ações de marketing.

### 🛡️ Governança e Segurança
- **Autenticação e Autorização:** Login seguro com Tokens JWT e controle de acesso baseado em perfis (Administrador, Gerente, Operador) via Spring Security.
- **Conformidade com LGPD:**
  - Coleta de consentimento explícito.
  - Funcionalidades para anonimização (direito ao esquecimento) e portabilidade de dados.
  - Página de Política de Privacidade.
- **Backup e Restauração:** Sistema completo para criar backups (download de JSON) e restaurar o estado do sistema.
- **Auditoria:** Log persistente de ações críticas (edição, anonimização, etc.) para rastreabilidade.

## 🛠️ Arquitetura e Tecnologias

A aplicação segue uma arquitetura moderna e desacoplada, com um backend robusto servindo uma API RESTful para um frontend dinâmico.

| Camada | Tecnologia/Framework | Justificativa |
| :--- | :--- | :--- |
| **Backend** | **Java 17 + Spring Boot 3** | Ecossistema maduro, seguro e performático, ideal para aplicações de negócio críticas. |
| | **Spring Security + JWT** | Padrão de mercado para autenticação e autorização, garantindo segurança robusta. |
| | **Spring Data JPA / Hibernate** | Alta produtividade e abstração para a persistência de dados. |
| **Frontend** | **React 18 + React Router** | Criação de interfaces de usuário reativas e dinâmicas, com excelente experiência do dev. |
| | **Styled Components** | Estilização componentizada e organizada, mantendo o escopo do CSS. |
| | **Axios** | Cliente HTTP robusto e padronizado para a comunicação com a API. |
| | **Recharts** | Biblioteca declarativa para a criação de gráficos interativos e visualmente agradáveis. |
| **Banco de Dados** | **MySQL 8.0** | Banco de dados relacional confiável, performático e amplamente utilizado no mercado. |

## 🚀 Como Executar o Projeto

### Pré-requisitos
-   Java JDK 17+
-   Apache Maven 3.8+
-   Node.js 18+
-   MySQL Server 8.0

### 1. Configuração do Backend
```bash
# Clone o repositório
git clone [URL_DO_SEU_REPOSITORIO]

# Navegue até a pasta do backend
cd ./synvia-core

# Configure o application.properties
# Abra src/main/resources/application.properties e ajuste as credenciais do seu banco de dados MySQL:
# spring.datasource.url=jdbc:mysql://localhost:3306/sua_database
# spring.datasource.username=seu_usuario
# spring.datasource.password=sua_senha
# E a pasta para os backups:
# backup.storage.location=C:/caminho/para/backups

# Compile e execute a aplicação
mvn spring-boot:run
```
O backend estará rodando em `http://localhost:8080`.

### 2. Configuração do Frontend
```bash
# Em um novo terminal, navegue até a pasta do frontend
cd ../FrontGoDgital # (Ajuste o nome da pasta se necessário)

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm start
```
A aplicação estará acessível em `http://localhost:3000`.

### 🔐 Credenciais de Teste
-   **Email:** `admin@synvia.io`
-   **Senha:** `admin123` 

## 🔮 Próximos Passos (Roadmap Futuro)
-   [ ] Implementar agendamento de backups (Scheduler).
-   [ ] Desenvolver um módulo de gestão de fornecedores.
-   [ ] Criar painel de KPIs de performance de funcionários.
-   [ ] Expandir o módulo de IA para previsão de demanda de produtos.
