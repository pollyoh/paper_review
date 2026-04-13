import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const reviews = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/reviews' }),
  schema: z.object({
    title: z.string(),
    originalTitle: z.string(),
    date: z.coerce.date(),
    authors: z.string(),
    institution: z.string(),
    tags: z.array(z.string()),
    description: z.string(),
  }),
});

export const collections = { reviews };
