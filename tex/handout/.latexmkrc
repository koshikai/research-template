#!/usr/bin/env perl
# LuaLaTeX configuration for handout
$pdf_mode = 4; # lualatex
$latex = 'lualatex %O -synctex=1 -interaction=nonstopmode -file-line-error %S';
$bibtex = 'upbibtex %O %B';
$out_dir = 'out';

# Cleanup
$clean_ext = 'synctex.gz synctex.gz(busy) run.xml tex.bak bbl bcf fdb_latexmk run tdo %R-blx.bib';
