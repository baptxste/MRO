DOCNAME=$1

pdflatex $DOCNAME.tex
bibtex $DOCNAME.aux
pdflatex $DOCNAME.tex
pdflatex $DOCNAME.tex

rm *.blg *.bbl *.aux *.log *.out *.toc
rm *.log *.aux

open $DOCNAME.pdf
