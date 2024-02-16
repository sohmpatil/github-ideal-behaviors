# Project name
PROJECT_NAME = github-deal-behaviours

# Python requirements
REQUIREMENTS = requirements.txt

# Install dependencies
install: 
	pip install -r $(REQUIREMENTS)

# Run development server	
run:
	python -m uvicorn main:app --reload
	
# Help	
help:
	@echo "Available commands:"
	@echo "make install - Install required packages" 
	@echo "make run - Run development server"