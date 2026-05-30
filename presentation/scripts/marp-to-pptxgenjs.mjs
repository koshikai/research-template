#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import matter from "gray-matter";
import PptxGenJS from "pptxgenjs";

const HELP_TEXT = `Usage:
  bun scripts/marp-to-pptxgenjs.mjs <input.md> [-o output.pptx]

Examples:
  bun scripts/marp-to-pptxgenjs.mjs demo.md
  bun scripts/marp-to-pptxgenjs.mjs demo.md --output demo-custom.pptx
`;

const DEFAULT_BACKGROUND = "FFFFFF";
const DARK_TEXT = "111827";
const LIGHT_TEXT = "F9FAFB";
const DARK_SUBTEXT = "6B7280";
const LIGHT_SUBTEXT = "D1D5DB";

function parseArgs(argv) {
  const parsed = { inputPath: "", outputPath: "", help: false };
  for (let idx = 0; idx < argv.length; idx += 1) {
    const token = argv[idx];
    if (token === "-h" || token === "--help") {
      parsed.help = true;
      return parsed;
    }
    if (token === "-o" || token === "--output") {
      const value = argv[idx + 1];
      if (!value) {
        throw new Error("Missing value for --output");
      }
      parsed.outputPath = value;
      idx += 1;
      continue;
    }
    if (!parsed.inputPath) {
      parsed.inputPath = token;
      continue;
    }
    throw new Error(`Unexpected argument: ${token}`);
  }
  return parsed;
}

function normalizeHexColor(value, fallback = DEFAULT_BACKGROUND) {
  if (typeof value !== "string") {
    return fallback;
  }
  const hex = value.trim().replace(/^#/, "").toUpperCase();
  if (/^[0-9A-F]{3}$/.test(hex)) {
    return hex
      .split("")
      .map((char) => `${char}${char}`)
      .join("");
  }
  if (/^[0-9A-F]{6}$/.test(hex)) {
    return hex;
  }
  return fallback;
}

function isDarkColor(hex) {
  const red = Number.parseInt(hex.slice(0, 2), 16);
  const green = Number.parseInt(hex.slice(2, 4), 16);
  const blue = Number.parseInt(hex.slice(4, 6), 16);
  const luminance = (0.299 * red + 0.587 * green + 0.114 * blue) / 255;
  return luminance < 0.5;
}

function stripInlineMarkdown(text) {
  return text
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[`*_~]/g, "")
    .replace(/<\/?[^>]+>/g, "")
    .replace(/\\([`*_{}\[\]()#+\-.!])/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
}

function splitSlides(content) {
  return content
    .split(/^\s*---\s*$/gm)
    .map((section) => section.trim())
    .filter((section) => section.length > 0);
}

function parseSlide(slideMarkdown) {
  const noHtmlComments = slideMarkdown.replace(/<!--[\s\S]*?-->/g, "");
  const lines = noHtmlComments.split(/\r?\n/);
  let title = "";
  const bullets = [];
  const body = [];
  let inCodeBlock = false;

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      continue;
    }
    if (line.startsWith("```")) {
      inCodeBlock = !inCodeBlock;
      continue;
    }
    if (inCodeBlock) {
      const codeLine = stripInlineMarkdown(rawLine);
      if (codeLine) {
        body.push(codeLine);
      }
      continue;
    }

    const headingMatch = line.match(/^#{1,6}\s+(.+)$/);
    if (headingMatch && !title) {
      title = stripInlineMarkdown(headingMatch[1]);
      continue;
    }

    const unorderedListMatch = line.match(/^[-*+]\s+(.+)$/);
    if (unorderedListMatch) {
      bullets.push(stripInlineMarkdown(unorderedListMatch[1]));
      continue;
    }

    const orderedListMatch = line.match(/^\d+\.\s+(.+)$/);
    if (orderedListMatch) {
      bullets.push(stripInlineMarkdown(orderedListMatch[1]));
      continue;
    }

    if (line.startsWith("![")) {
      const altText = line.match(/^!\[([^\]]*)\]/)?.[1] ?? "image";
      body.push(`[Image] ${stripInlineMarkdown(altText)}`.trim());
      continue;
    }

    const cleaned = stripInlineMarkdown(line);
    if (cleaned) {
      body.push(cleaned);
    }
  }

  if (!title && body.length > 0) {
    title = body.shift() ?? "";
  }

  return { title, bullets, body };
}

function addHeader(slide, headerText, color) {
  if (!headerText) {
    return;
  }
  slide.addText(String(headerText), {
    x: 0.45,
    y: 0.16,
    w: 12.2,
    h: 0.18,
    fontSize: 10,
    color,
    align: "left",
    valign: "mid",
  });
}

function addFooter(slide, footerText, color) {
  if (!footerText) {
    return;
  }
  slide.addText(String(footerText), {
    x: 0.45,
    y: 7.14,
    w: 10.2,
    h: 0.2,
    fontSize: 10,
    color,
    align: "left",
    valign: "mid",
  });
}

function addPagination(slide, slideIndex, totalSlides, color) {
  slide.addText(`${slideIndex + 1}/${totalSlides}`, {
    x: 11.0,
    y: 7.14,
    w: 1.85,
    h: 0.2,
    fontSize: 10,
    color,
    align: "right",
    valign: "mid",
  });
}

function addSlideFromModel(pptx, slideModel, options) {
  const slide = pptx.addSlide();
  slide.background = { color: options.backgroundColor };

  addHeader(slide, options.header, options.subTextColor);
  addFooter(slide, options.footer, options.subTextColor);
  if (options.paginate) {
    addPagination(slide, options.slideIndex, options.totalSlides, options.subTextColor);
  }

  let currentY = options.header ? 0.58 : 0.4;

  if (slideModel.title) {
    slide.addText(slideModel.title, {
      x: 0.72,
      y: currentY,
      w: 11.9,
      h: 0.95,
      fontSize: 34,
      bold: true,
      color: options.textColor,
      valign: "mid",
    });
    currentY += 1.05;
  }

  if (slideModel.bullets.length > 0) {
    const bulletText = slideModel.bullets.map((item) => `- ${item}`).join("\n");
    const bulletHeight = Math.min(4.0, 0.5 * slideModel.bullets.length + 0.5);
    slide.addText(bulletText, {
      x: 0.95,
      y: currentY,
      w: 11.35,
      h: bulletHeight,
      fontSize: 20,
      color: options.textColor,
      breakLine: true,
      valign: "top",
    });
    currentY += bulletHeight + 0.15;
  }

  if (slideModel.body.length > 0) {
    slide.addText(slideModel.body.join("\n"), {
      x: 0.95,
      y: currentY,
      w: 11.35,
      h: 7.0 - currentY,
      fontSize: 16,
      color: options.textColor,
      breakLine: true,
      valign: "top",
    });
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.inputPath) {
    console.log(HELP_TEXT);
    process.exit(args.help ? 0 : 1);
  }

  const inputPath = path.resolve(args.inputPath);
  const source = await fs.readFile(inputPath, "utf8");
  const parsed = matter(source);
  const slides = splitSlides(parsed.content).map(parseSlide);

  if (slides.length === 0) {
    throw new Error("No slides found. Use `---` separators in the markdown content.");
  }

  const outputPath =
    args.outputPath ||
    path.join(
      path.dirname(inputPath),
      `${path.basename(inputPath, path.extname(inputPath))}-pptxgenjs.pptx`,
    );
  const resolvedOutputPath = path.resolve(outputPath);
  await fs.mkdir(path.dirname(resolvedOutputPath), { recursive: true });

  const backgroundColor = normalizeHexColor(parsed.data.backgroundColor);
  const darkBackground = isDarkColor(backgroundColor);
  const textColor = darkBackground ? LIGHT_TEXT : DARK_TEXT;
  const subTextColor = darkBackground ? LIGHT_SUBTEXT : DARK_SUBTEXT;
  const paginate = Boolean(parsed.data.paginate);

  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "research-template";
  pptx.subject = "Presentation generated from Marp markdown";
  pptx.title = path.basename(inputPath);

  slides.forEach((slideModel, slideIndex) => {
    addSlideFromModel(pptx, slideModel, {
      backgroundColor,
      header: parsed.data.header,
      footer: parsed.data.footer,
      paginate,
      slideIndex,
      totalSlides: slides.length,
      textColor,
      subTextColor,
    });
  });

  await pptx.writeFile({ fileName: resolvedOutputPath });
  console.log(`Generated: ${resolvedOutputPath}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
