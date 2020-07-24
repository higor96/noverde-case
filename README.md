# noverde-case

### Git Clone

```bash
git clone https://github.com/higor96/noverde-case.git
```

### Instalação Docker e Docker-Compose

Na documentação do Docker é possível encontrar o passo a passo para realizar a instalação do Docker e Docker-Compose.
Ambos são necessários para execução do projeto.
https://docs.docker.com/compose/install/
https://docs.docker.com/engine/install/

### Inicialização

Dentro da pasta docker-flask-celery-redis, executar o comando:

```bash
docker-compose up --build
```

Após o Container subir, acessar a aplicação do Flask na porta 5001.
Para consultar as tasks agendadas pelo Celery, acessar o Flower na porta 5555.

Para rodar o PyTest, dentro do Container executar o comando:

```bash
docker exec -it docker-flask-celery-redis_monitor_1 pytest
```
