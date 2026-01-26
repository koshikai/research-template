#!/usr/bin/env perl
# LuaLaTeX configuration
$pdf_mode = 4; # PDF via lualatex
$postscript_mode = $dvi_mode = 0;

$lualatex = 'lualatex %O -synctex=1 -interaction=nonstopmode -file-line-error %S';
$bibtex = 'upbibtex %O %B';
$out_dir = 'out';

# Cleanup
$clean_ext = 'synctex.gz synctex.gz(busy) run.xml tex.bak bbl bcf fdb_latexmk run tdo %R-blx.bib';
