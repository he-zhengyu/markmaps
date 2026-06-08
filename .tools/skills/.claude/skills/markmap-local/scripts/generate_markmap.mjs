#!/usr/bin/env node

/**
 * generate_markmap.mjs — Convert a Markdown file into an interactive markmap HTML file.
 *
 * Usage:
 *   node generate_markmap.mjs <input.md> [output.html] [--offline]
 *
 * If output is omitted, writes to <input-basename>.html in the same directory.
 * --offline flag inlines all JS/CSS for offline viewing (larger file size).
 */

import { Transformer } from 'markmap-lib';
import { fillTemplate } from 'markmap-render';
import { readFileSync, writeFileSync } from 'fs';
import { basename, dirname, join, extname } from 'path';

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log(`Usage: node generate_markmap.mjs <input.md> [output.html] [--offline]`);
  console.log(`  --offline   Inline assets for offline use (not yet implemented, uses CDN)`);
  process.exit(0);
}

const inputPath = args.find(a => !a.startsWith('--'));
const remainingArgs = args.filter(a => a !== inputPath && !a.startsWith('--'));
const outputPath = remainingArgs[0] ||
  join(dirname(inputPath), basename(inputPath, extname(inputPath)) + '.html');

try {
  const markdown = readFileSync(inputPath, 'utf-8');

  const transformer = new Transformer();
  const { root, features } = transformer.transform(markdown);
  const assets = transformer.getUsedAssets(features);

  // Default JSON options — can be overridden via frontmatter in the .md file
  const defaultJsonOptions = {
    initialExpandLevel: -1,
    maxWidth: 300,
  };

  const html = fillTemplate(root, assets, {
    jsonOptions: defaultJsonOptions,
  });

  writeFileSync(outputPath, html);
  console.log(`✅ Markmap generated: ${outputPath}`);
  console.log(`   Nodes: ${countNodes(root)}`);
} catch (err) {
  console.error(`❌ Error: ${err.message}`);
  process.exit(1);
}

function countNodes(node) {
  if (!node) return 0;
  let count = 1;
  if (node.children) {
    for (const child of node.children) {
      count += countNodes(child);
    }
  }
  return count;
}
