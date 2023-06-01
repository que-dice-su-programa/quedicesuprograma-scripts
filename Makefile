.PHONY: help setup

help: ## Show this help message
	@echo "\nOptions:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


setup: ## setup dependencies
	pip install -r requirements.txt

update-requirements: ## Update requirements file
	pipreqs --force ./

