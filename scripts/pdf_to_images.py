import logging
from pathlib import Path

import fitz  # pymupdf


def main():
    # Setup simple logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("pdf_to_images")

    ref_dir = Path("references")
    if not ref_dir.exists():
        logger.error(f"Directory {ref_dir} does not exist.")
        return

    # Create images directory
    img_root_dir = ref_dir / "images"
    img_root_dir.mkdir(exist_ok=True)

    pdfs = list(ref_dir.glob("*.pdf"))
    if not pdfs:
        logger.info(f"No PDF files found in {ref_dir}.")
        return

    logger.info(f"Found {len(pdfs)} PDF files in {ref_dir}.")

    for pdf_path in pdfs:
        # Create a dedicated directory for this paper's images
        paper_name = pdf_path.stem
        paper_img_dir = img_root_dir / paper_name
        paper_img_dir.mkdir(exist_ok=True)

        logger.info(f"Processing {pdf_path.name}...")

        try:
            doc = fitz.open(pdf_path)
            for i, page in enumerate(doc):
                # Save as PNG
                # Zoom = 2 (144 dpi) for better quality
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                output_path = paper_img_dir / f"page_{i + 1:03d}.png"
                pix.save(output_path)

            logger.info(f"Saved {len(doc)} pages to {paper_img_dir}")
            doc.close()

        except Exception as e:
            logger.error(f"Failed to process {pdf_path.name}: {e}")


if __name__ == "__main__":
    main()
