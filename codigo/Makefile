.PHONY: all test benchmark clean

all: test

test:
	uv run python python/test_suite.py

benchmark:
	uv run python python/benchmark.py --trials 3 --plot ../images/benchmark_results.png

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f *.png

