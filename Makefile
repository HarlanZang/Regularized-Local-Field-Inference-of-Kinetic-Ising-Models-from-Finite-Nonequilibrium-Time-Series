# Regenerate the processed CSV data and the revised figures (Figs. 4-6).
PY ?= python3
FIGS = figures/Fig4_calibration.pdf figures/Fig5_regime.pdf figures/Fig6_robustness.pdf

all: data $(FIGS)

data: tables/*.tex scripts/tables_to_csv.py
	$(PY) scripts/tables_to_csv.py tables data

figures/Fig4_calibration.pdf: scripts/make_fig4_calibration.py scripts/style.py data/fig4_coverage.csv data/fig4_zhist.csv
	cd scripts && $(PY) make_fig4_calibration.py ../data ../$@

figures/Fig5_regime.pdf: data scripts/make_fig5_regime.py scripts/style.py
	cd scripts && $(PY) make_fig5_regime.py ../data/S_regime.csv ../$@

figures/Fig6_robustness.pdf: data scripts/make_fig6_robustness.py scripts/style.py
	cd scripts && $(PY) make_fig6_robustness.py ../data ../$@

clean:
	rm -f $(FIGS) $(FIGS:.pdf=.png)

.PHONY: all data clean
