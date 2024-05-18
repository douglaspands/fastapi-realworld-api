# Changelog

Todas as notas de alteração deste projeto serão documentados neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e o projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/spec/v2.0.0.html).

## [Não Lançado]

### Adicionado

- Incluido user model;
- Incluido user repository;
- Incluido função get_or_create no people repository;
- Incluido user service;
- Incluido user resource;
- Incluido user controller;
- Incluido user no context;
- Incluido gerador de token;
- Incluido validador de token;
- Incluido Depends para o validador de token em todas as people controllers;
- Incluido Depends para o validador de token em todas as user controllers (menos create user);
- Alembic: incluido script de criação da tabela user;
- Cobertura de teste de 100% do codigo; [AGUARDANDO]
- Incluido configurações do OpenAPIDocs no Settings;
- Incluido configurações do token no Settings;
- Poetry: Incluido script de `sqlmigrate`;
- Poetry: Incluido script de `makemigrations`;

### Modificado

- Remoção do `[EM DESENVOLVIMENTO]` do titulo do README.md;
- Modificado a versão para `0.2.0` do `pyproject.toml`;
- No people repository foi modificado para remover o id dos values no update;
- Melhoria na organização das pastas de recursos;
- Melhorias na configuração das migrations;
- Poetry: mudança no comando `server_production` para `production_server`;

## [0.1.0] - 2024-05-12

### Adicionado

- Incluido people controller;
- Incluido people service;
- Incluido people repository;
- Incluido people model;
- Incluido people resource;
- Incluido core api;
- Incluido core handler;
- Incluido core settings;
- Incluido core router;
- Incluido core database;
- Incluido core context;
- Incluido core exceptions;
- Incluido core openapi;
- Incluido core schema;
- Incluido core midleware;
- Cobertura de teste de 100% do codigo;
- Alembic: incluido e configurado para a autogeração dos scripts de migração;
