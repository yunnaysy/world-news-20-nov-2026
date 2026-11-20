// Friday, 20 November 2026 world-news front page.
// Copy the finished, locally rendered editorial image; no network or third-party packages are used.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const sourcePath = fileURLToPath(new URL('./entry.png', import.meta.url));
const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const outputPath = join(outputDirectory, 'entry.png');

mkdirSync(dirname(outputPath), { recursive: true });
copyFileSync(sourcePath, outputPath);
