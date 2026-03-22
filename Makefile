up:
	@echo "🚀 Lancement..."
	@docker compose up -d

	@echo "⏳ Attente Airflow..."
	@until curl -s http://localhost:8081 > /dev/null; do \
		sleep 2; \
	done

	@echo ""
	@echo "✅ Environnement prêt !"
	@echo "✅ Airflow prêt : http://localhost:8081"
	@echo "✅ FastAPI prêt : http://localhost:8000"

down:
	@docker compose down

logs:
	@docker compose logs -f