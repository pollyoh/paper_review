import { useState, useMemo } from 'react';

interface Paper {
  slug: string;
  title: string;
  originalTitle: string;
  date: string;
  authors: string;
  institution: string;
  tags: string[];
  description: string;
}

interface Props {
  papers: Paper[];
  basePath: string;
}

function formatDate(dateStr: string): string {
  const [y, m, d] = dateStr.split('-');
  return `${y}.${m}.${d}`;
}

export default function PaperSearch({ papers, basePath }: Props) {
  const [query, setQuery] = useState('');
  const [activeTag, setActiveTag] = useState<string | null>(null);

  const allTags = useMemo(
    () => [...new Set(papers.flatMap((p) => p.tags))].sort(),
    [papers],
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return papers.filter((p) => {
      if (activeTag && !p.tags.includes(activeTag)) return false;
      if (!q) return true;
      const haystack = [p.title, p.originalTitle, p.description, p.authors, ...p.tags]
        .join(' ')
        .toLowerCase();
      return haystack.includes(q);
    });
  }, [papers, query, activeTag]);

  const handleTagClick = (tag: string) => {
    setActiveTag((prev) => (prev === tag ? null : tag));
  };

  const base = basePath.replace(/\/$/, '');

  return (
    <>
      <div className="controls">
        <input
          type="text"
          className="search-box"
          placeholder="제목, 태그, 저자로 검색..."
          aria-label="논문 검색"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div className="tag-filters">
          {allTags.map((tag) => (
            <button
              key={tag}
              className={`tag-btn${activeTag === tag ? ' active' : ''}`}
              onClick={() => handleTagClick(tag)}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      <div className="stats">
        {filtered.length > 0 ? `${filtered.length}개의 리뷰` : ''}
      </div>

      <div className="card-grid">
        {filtered.map((paper) => (
          <a
            key={paper.slug}
            className="paper-card"
            href={`${base}/reviews/${paper.slug}/`}
          >
            <span className="card-date">{formatDate(paper.date)}</span>
            <div className="card-title">{paper.title}</div>
            <div className="card-original-title">{paper.originalTitle}</div>
            <div className="card-authors">
              {paper.authors}
              {paper.institution ? ` \u00B7 ${paper.institution}` : ''}
            </div>
            <div className="card-desc">{paper.description}</div>
            <div className="card-tags">
              {paper.tags.map((t) => (
                <span key={t} className="card-tag">{t}</span>
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
