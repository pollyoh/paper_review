import { useState, useMemo, useEffect } from 'react';

export type PaperKind = 'reviews' | 'studies';

export type TabFilter = 'all' | PaperKind;

export interface ListedPaper {
  kind: PaperKind;
  slug: string;
  title: string;
  subtitle: string;
  authorsMeta: string;
  date: string;
  tags: string[];
  description: string;
}

interface Props {
  papers: ListedPaper[];
  basePath: string;
}

function formatDate(dateStr: string): string {
  const [y, m, d] = dateStr.split('-');
  return `${y}.${m}.${d}`;
}

function readTabFromUrl(): TabFilter {
  if (typeof window === 'undefined') return 'all';
  const v = new URLSearchParams(window.location.search).get('tab');
  if (v === 'reviews' || v === 'studies') return v;
  return 'all';
}

export default function PaperSearch({ papers, basePath }: Props) {
  const [query, setQuery] = useState('');
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [tab, setTab] = useState<TabFilter>('all');

  useEffect(() => {
    setTab(readTabFromUrl());
  }, []);

  const setTabAndUrl = (next: TabFilter) => {
    setTab(next);
    if (typeof window === 'undefined') return;
    const u = new URL(window.location.href);
    if (next === 'all') {
      u.searchParams.delete('tab');
    } else {
      u.searchParams.set('tab', next);
    }
    window.history.replaceState({}, '', u.pathname + u.search + u.hash);
  };

  const allTags = useMemo(
    () => [...new Set(papers.flatMap((p) => p.tags))].sort(),
    [papers],
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return papers.filter((p) => {
      if (tab !== 'all' && p.kind !== tab) return false;
      if (activeTag && !p.tags.includes(activeTag)) return false;
      if (!q) return true;
      const haystack = [
        p.title,
        p.subtitle,
        p.description,
        p.authorsMeta,
        p.kind,
        ...p.tags,
      ]
        .join(' ')
        .toLowerCase();
      return haystack.includes(q);
    });
  }, [papers, query, activeTag, tab]);

  const handleTagClick = (tag: string) => {
    setActiveTag((prev) => (prev === tag ? null : tag));
  };

  const base = basePath.replace(/\/$/, '');

  return (
    <>
      <div className="content-tabs" role="tablist" aria-label="콘텐츠 유형">
        {(
          [
            ['all', '전체'],
            ['reviews', '논문'],
            ['studies', '기술공부'],
          ] as const
        ).map(([key, label]) => (
          <button
            key={key}
            type="button"
            role="tab"
            aria-selected={tab === key}
            className={`tab-btn${tab === key ? ' active' : ''}`}
            onClick={() => setTabAndUrl(key)}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="controls">
        <input
          type="text"
          className="search-box"
          placeholder="제목, 태그, 부제로 검색..."
          aria-label="글 검색"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div className="tag-filters">
          {allTags.map((tag) => (
            <button
              key={tag}
              type="button"
              className={`tag-btn${activeTag === tag ? ' active' : ''}`}
              onClick={() => handleTagClick(tag)}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      <div className="stats">
        {filtered.length > 0 ? `${filtered.length}개의 글` : ''}
      </div>

      <div className="card-grid">
        {filtered.map((paper) => (
          <a
            key={`${paper.kind}-${paper.slug}`}
            className="paper-card"
            href={`${base}/${paper.kind === 'reviews' ? 'reviews' : 'studies'}/${paper.slug}/`}
          >
            <div className="card-header-row">
              <span className="card-date">{formatDate(paper.date)}</span>
              <span className={`kind-badge kind-${paper.kind}`}>
                {paper.kind === 'reviews' ? '논문' : '기술'}
              </span>
            </div>
            <div className="card-title">{paper.title}</div>
            {paper.subtitle ? (
              <div className="card-original-title">{paper.subtitle}</div>
            ) : null}
            {paper.authorsMeta ? (
              <div className="card-authors">{paper.authorsMeta}</div>
            ) : null}
            <div className="card-desc">{paper.description}</div>
            <div className="card-tags">
              {paper.tags.map((t) => (
                <span key={t} className="card-tag">
                  {t}
                </span>
              ))}
            </div>
          </a>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="empty-state visible">검색 결과가 없습니다.</div>
      )}
    </>
  );
}
