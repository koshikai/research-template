# TeX Templates

This directory contains the TeX templates for the research repository.

## Directory Structure

- `sotsuron/`: Template for Graduation Thesis (卒業論文)
- `zemi/`: Template for Seminar Papers (ゼミ資料)
- `handout/`: Template for Conference Handout (学会発表原稿)

## Usage

You can initialize a new document by copying one of these directories.

### Graduation Thesis
```bash
cp -r tex/sotsuron tex/my_thesis
cd tex/my_thesis
latexmk
```

### Seminar Paper
```bash
cp -r tex/zemi tex/my_seminar_paper
cd tex/my_seminar_paper
latexmk
```

### Handout
```bash
cp -r tex/handout tex/my_handout
cd tex/my_handout
latexmk
```
