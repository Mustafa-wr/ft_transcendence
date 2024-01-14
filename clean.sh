rm -rf project/myapp/__pycache__
rm -rf project/myapp/migrations
rm -rf project/__pycache__
rm -rf project/project/__pycache__
docker system prune
docker volume rm ft_transcendence_pgdata