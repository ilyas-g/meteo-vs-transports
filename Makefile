up:
	@echo "🚀 Lancement de l'environnement Docker..."
	@docker compose up -d

	@echo "⏳ Vérification des services..."
	@sleep 5

	@docker compose ps

	@echo ""
	@echo "✅ Environnement prêt !"
	@echo "➡ Airflow : http://localhost:8081"
	@echo "➡ FastAPI : http://localhost:8000"

down:
	docker compose down

logs:
	docker compose logs -f