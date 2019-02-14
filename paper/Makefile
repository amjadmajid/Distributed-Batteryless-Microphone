PAPER :=paper
all:
	pdflatex $(PAPER)
	bibtex	 $(PAPER) 
	pdflatex $(PAPER)
	pdflatex $(PAPER)

view: all
	open -a Preview $(PAPER).pdf
fig:
	make -C figures

figclean:
	make -C figures clean

clean:
	-rm *.out *.pdf *.aux *.log *.bbl *blg
