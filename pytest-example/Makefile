.PHONY: clean test coverage-report

test:
	pytest test.py

coverage-report:
	pytest test.py --cov=app --cov-report=html

clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm .coverage