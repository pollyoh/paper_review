/**
 * Shiki transformer that prevents syntax highlighting on mermaid code blocks.
 * Instead, outputs <pre class="mermaid">raw text</pre> for mermaid.js runtime.
 */
export function shikiMermaidTransformer() {
  return {
    name: 'mermaid-passthrough',
    preprocess(code, options) {
      if (options.lang === 'mermaid') {
        this.__isMermaid = true;
      }
    },
    root(node) {
      if (this.__isMermaid) {
        return {
          type: 'root',
          children: [
            {
              type: 'element',
              tagName: 'pre',
              properties: { className: ['mermaid'] },
              children: [{ type: 'text', value: this.source }],
            },
          ],
        };
      }
    },
  };
}
