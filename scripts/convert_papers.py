import logging
from pathlib import Path

try:
    import pymupdf4llm
except ImportError:
    pymupdf4llm = None


def main():
    # Setup simple logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("paper_converter")

    if pymupdf4llm is None:
        logger.error("pymupdf4llm is not installed. Please run 'uv add pymupdf4llm'")
        return

    ref_dir = Path("references")
    if not ref_dir.exists():
        logger.warning(f"Directory {ref_dir} does not exist. Creating it...")
        ref_dir.mkdir(exist_ok=True)
        logger.info(
            f"Please place your PDF papers in {ref_dir} and run this command again."
        )
        return

    pdfs = list(ref_dir.glob("*.pdf"))
    if not pdfs:
        logger.info(
            f"No PDF files found in {ref_dir}. Place PDF files there to convert them."
        )
        return

    logger.info(f"Found {len(pdfs)} PDF files in {ref_dir}.")

    for pdf_path in pdfs:
        md_path = pdf_path.with_suffix(".md")

        if md_path.exists():
            logger.info(f"Skipping {pdf_path.name} (Markdown already exists)")
            continue

        logger.info(f"Converting {pdf_path.name}...")
        try:
            # Converting PDF to Markdown
            md_text = pymupdf4llm.to_markdown(str(pdf_path))

            # Save to file
            md_path.write_text(md_text, encoding="utf-8")
            logger.info(f"Successfully converted: {md_path.name}")
        except Exception as e:
            logger.error(f"Failed to convert {pdf_path.name}: {e}")


if __name__ == "__main__":
    main()
