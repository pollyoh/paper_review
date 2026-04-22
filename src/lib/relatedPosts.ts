import type { CollectionEntry } from 'astro:content';

export type AnyPost = CollectionEntry<'reviews'> | CollectionEntry<'studies'>;

function tagOverlap(a: string[], b: string[]): number {
  const sb = new Set(b);
  return a.filter((t) => sb.has(t)).length;
}

export function getRelated(
  current: AnyPost,
  reviews: CollectionEntry<'reviews'>[],
  studies: CollectionEntry<'studies'>[],
  limit = 3,
): { href: string; title: string; collection: 'reviews' | 'studies' }[] {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const scored = [...reviews, ...studies]
    .filter((e) => !(e.id === current.id && e.collection === current.collection))
    .map((e) => {
      let score = 0;
      const ct = current.data.topic;
      const et = e.data.topic;
      if (ct && et && ct === et) score += 100;
      score += 10 * tagOverlap(current.data.tags, e.data.tags);
      score += e.data.date.getTime() / 1e12;
      const href =
        e.collection === 'reviews'
          ? `${base}/reviews/${e.id}/`
          : `${base}/studies/${e.id}/`;
      return { href, title: e.data.title, collection: e.collection, score };
    });
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, limit).map(({ href, title, collection }) => ({
    href,
    title,
    collection,
  }));
}
