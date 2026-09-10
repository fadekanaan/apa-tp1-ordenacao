.PHONY: all test benchmark clean

# Raiz do repositório, resolvida a partir da localização deste Makefile.
ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))..)

all: test

# Executa as DUAS suítes (test_suite.py e test_authorial.py) em uma única sessão.
test:
	uv run python -m unittest discover -s python -p 'test_*.py'

# Grava o gráfico na raiz do repositório, que é o caminho referenciado pelo
# relatório em relatorio/relatorio_tp1.md (../benchmark_results.png).
benchmark:
	uv run python python/benchmark.py --trials 3 --plot $(ROOT)/benchmark_results.png

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
