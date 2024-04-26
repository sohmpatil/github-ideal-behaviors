# Project name
PROJECT_NAME = github-ideal-behaviours

# Python requirements
REQUIREMENTS = requirements.txt

# Install dependencies
install: 
	pip install -r $(REQUIREMENTS)

# Run development server	
run:
	python -m uvicorn main:app --reload

# Create executable file	
executable:
	pip install pyinstaller
	pyinstaller main.py

# Help	
help:
	@echo "Available commands:"
	@echo "make install - Install required packages" 
	@echo "make run - Run development server"

build:
	docker build -t github-ideal-behavior:latest .

container:
	docker build -t github-ideal-behavior:latest .
	docker run -p 8080:8080 github-ideal-behavior:latest
