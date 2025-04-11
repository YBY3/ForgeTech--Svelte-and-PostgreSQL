# Project-55 README

## Frontend
- **Svelte** - [Svelte Official Site](https://svelte.dev/)
- **Skeleton UI + Tailwind CSS** - [Skeleton UI Official Site](https://www.skeleton.dev/)

## Backend
- **Flask** - [Flask Official Documentation](https://flask.palletsprojects.com/en/stable/)
- **PostgreSQL** - [PostgreSQL Official Site](https://www.postgresql.org/)
- **Docker** - [Docker Official Site](https://www.docker.com/)

## How Docker was Setup with Flask
  https://www.youtube.com/watch?v=MafSR4DZOhY

## Docker Backend App Commands
- **Build Docker**: 
  docker-compose build
- **Run Docker** (in detached mode):
  docker-compose up -d
- **Stop Docker**:
  docker-compose down

## Adminer Commands
- **Drop All Tables**: 
  DROP TABLE "user", "product", "order_product", "order" CASCADE; 

## Useful Docker Commands
- **List active and stopped containers**:
  docker ps -a

## Open Flask Shell While Docker is Running
1. Access the Flask app in Docker:
   docker exec -it backend-app-1 bash
2. Open Flask shell:
   flask shell
3. Create Tables:
   db.create_all()
Drop tables:
db.drop_all()
4. Exit Flask shell:
   exit()
5. Exit Flask app:
   exit

## Print from Flask App to Docker Debug Console
- **Use this Print Statement and "import sys"**
  print('message', file=sys.stderr)

## RESET DOCKER ENVIROMENT
  docker system prune -af --volumes