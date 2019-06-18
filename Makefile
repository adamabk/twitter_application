.PHONY: help run test shell stop

default: help

help: ## Show this help
	@echo "fetcher Service"
	@echo "======================"
	@echo
	@echo "CLI Tool to fetch Twitter Tweets into PostgreSQL"
	@echo
	@fgrep -h " ## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -Ee 's/([a-z.]*):[^#]*##(.*)/\1##\2/' | column -t -s "##"

build: ## Build fetcher service
	@docker-compose up --build fetcher

run: build ## Run Shell inside the fetcher container
	@docker-compose run fetcher /bin/sh

stop: ## Stop running applications
	@docker-compose down

db: ## Start DB container
	@docker-compose up --build db
