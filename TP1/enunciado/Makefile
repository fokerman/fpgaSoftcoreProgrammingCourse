.PHONY: all clean cleanall

SOURCES := $(shell find `pwd` -name '*.tex' | grep -v alternativo)
OUTPUT := $(SOURCES:%.tex=%.pdf)
NAME := enunciado

all: $(OUTPUT)

%.pdf: %.tex
ifneq (,$(wildcard ./img/Makefile))
	make -C img
endif
	pdflatex $(NAME).tex #> /dev/null
	pdflatex $(NAME).tex #> /dev/null
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.synctex.gz

clean:
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.synctex.gz

cleanall:
	rm -f $(OUTPUT) $(NAME).pdf
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.synctex.gz
