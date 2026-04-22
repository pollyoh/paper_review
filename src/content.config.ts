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
    topic: z.string().optional(),
  }),
});

const studies = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/studies' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string(),
    tags: z.array(z.string()),
    topic: z.string(),
    sources: z
      .array(
        z.object({
          title: z.string(),
          url: z.string().url(),
        }),
      )
      .optional(),
    originalTitle: z.string().optional(),
    authors: z.string().optional(),
    institution: z.string().optional(),
  }),
});

export const collections = { reviews, studies };
