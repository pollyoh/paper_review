import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { shikiMermaidTransformer } from './src/plugins/rehype-mermaid.mjs';

export default defineConfig({
  site: 'https://pollyoh.github.io',
  base: '/paper_review',
  output: 'static',
  integrations: [react()],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
    shikiConfig: {
      transformers: [shikiMermaidTransformer()],
    },
  },
});
