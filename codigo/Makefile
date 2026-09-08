.PHONY: all test benchmark clean

all: test

test:
	python3 python/test_suite.py

benchmark:
	python3 python/benchmark.py --trials 3 --plot benchmark_results.png

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f *.png

