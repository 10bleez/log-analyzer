#!/bin/bash
echo "Запуск тестов и генерация HTML-отчета..."
python3 -m pytest --cov=. --cov-report=html --cov-report=term-missing --cov-config=.coveragerc
echo "Отчет готов! Откройте файл htmlcov/index.html в браузере."
