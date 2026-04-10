import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';

mermaid.initialize({
	startOnLoad: true,
	theme: 'base',
	securityLevel: 'loose',
	themeVariables: {
		primaryColor: '#eef4fb',
		primaryBorderColor: '#8faecc',
		primaryTextColor: '#1f2d3d',
		secondaryColor: '#f8fbfe',
		tertiaryColor: '#ffffff',
		lineColor: '#6f8faf',
		fontFamily: 'Pretendard, Noto Sans KR, Apple SD Gothic Neo, Segoe UI, sans-serif'
	}
});

const noteBlocks = Array.from(document.querySelectorAll('blockquote')).filter((block) => {
	const label = block.querySelector('p strong');
	return label && label.textContent.trim().startsWith('[주석]');
});

for (const block of noteBlocks) {
	const paragraphs = Array.from(block.querySelectorAll(':scope > p'));
	const firstStrong = paragraphs[0]?.querySelector('strong');
	const summaryText = firstStrong ? firstStrong.textContent.trim() : '주석';

	if (paragraphs[0] && firstStrong) {
		firstStrong.remove();
		paragraphs[0].innerHTML = paragraphs[0].innerHTML.replace(/^:\s*/, '').trim();
		if (!paragraphs[0].textContent.trim()) {
			paragraphs[0].remove();
		}
	}

	const details = document.createElement('details');
	details.className = 'commentary-toggle';

	const summary = document.createElement('summary');
	summary.textContent = summaryText.replace(/^\[주석\]\s*/, '');

	const body = document.createElement('div');
	body.className = 'commentary-body';

	while (block.firstChild) {
		body.appendChild(block.firstChild);
	}

	details.append(summary, body);
	block.replaceWith(details);
}

const contentRoot = document.querySelector('.content-wrapper');
const tocHeading = contentRoot.querySelector('h2[id="%EB%AA%A9%EC%B0%A8"]');
const legacyTocList = tocHeading?.nextElementSibling;
const legacyTocDivider = legacyTocList?.nextElementSibling?.tagName === 'HR' ? legacyTocList.nextElementSibling : null;

legacyTocDivider?.remove();
legacyTocList?.remove();
tocHeading?.remove();

const remainingBlockquotes = Array.from(contentRoot.querySelectorAll('blockquote'));
remainingBlockquotes.forEach((block, index) => {
	const text = block.textContent.trim();
	if (text.includes('면책 조항')) {
		block.classList.add('disclaimer-callout');
		return;
	}

	if (index === 0) {
		block.classList.add('meta-card');
		return;
	}

	block.classList.add('summary-callout');
});

const sentenceSegmenter = typeof Intl !== 'undefined' && Intl.Segmenter
	? new Intl.Segmenter('ko', { granularity: 'sentence' })
	: null;

const sentenceRanges = (text) => {
	if (sentenceSegmenter) {
		const parts = Array.from(sentenceSegmenter.segment(text)).filter((part) => part.segment.trim());
		return parts.map((part, index) => ({
			start: part.index,
			end: index + 1 < parts.length ? parts[index + 1].index : text.length
		}));
	}

	const matches = [...text.matchAll(/[^.!?]+(?:[.!?]+|$)\s*/g)];
	return matches
		.map((match) => ({ start: match.index ?? 0, end: (match.index ?? 0) + match[0].length }))
		.filter((range) => text.slice(range.start, range.end).trim());
};

const locateTextPosition = (root, targetOffset) => {
	const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
	let traversed = 0;
	let lastNode = null;

	while (walker.nextNode()) {
		const node = walker.currentNode;
		const length = node.nodeValue.length;
		lastNode = node;

		if (targetOffset <= traversed + length) {
			return { node, offset: Math.max(0, targetOffset - traversed) };
		}

		traversed += length;
	}

	if (!lastNode) {
		return null;
	}

	return { node: lastNode, offset: lastNode.nodeValue.length };
};

const splitLongParagraph = (paragraph) => {
	const text = paragraph.textContent;
	if (text.trim().length < 340) {
		return;
	}

	const sentences = sentenceRanges(text);
	if (sentences.length <= 5) {
		return;
	}

	const chunkSizes = [];
	let remaining = sentences.length;

	while (remaining > 5) {
		const size = remaining === 6 ? 3 : 4;
		chunkSizes.push(size);
		remaining -= size;
	}

	chunkSizes.push(remaining);

	if (chunkSizes.length <= 1) {
		return;
	}

	const boundaries = [];
	let count = 0;
	for (let index = 0; index < chunkSizes.length - 1; index += 1) {
		count += chunkSizes[index];
		boundaries.push(sentences[count].start);
	}

	const insertBeforeNode = paragraph.nextSibling;

	for (let index = boundaries.length - 1; index >= 0; index -= 1) {
		const splitPoint = locateTextPosition(paragraph, boundaries[index]);
		if (!splitPoint) {
			continue;
		}

		const range = document.createRange();
		range.setStart(splitPoint.node, splitPoint.offset);
		range.setEnd(paragraph, paragraph.childNodes.length);

		const newParagraph = paragraph.cloneNode(false);
		newParagraph.appendChild(range.extractContents());

		if (newParagraph.textContent.trim()) {
			paragraph.parentNode.insertBefore(newParagraph, insertBeforeNode);
		}
	}
};

const paragraphsToSplit = Array.from(contentRoot.querySelectorAll('p')).filter((paragraph) => {
	return !paragraph.closest('blockquote, details, li, td, th, figcaption, .visual-card, .visual-flow, pre')
		&& !paragraph.querySelector('.katex-display, .katex');
});

paragraphsToSplit.forEach(splitLongParagraph);

const tocHeadings = Array.from(contentRoot.querySelectorAll('h2, h3')).filter(
	(heading) => heading.textContent.trim() !== '목차'
);

const slugCounts = new Map();

const makeSlug = (text, fallback) => {
	const slug = text
		.normalize('NFKD')
		.replace(/[\u0300-\u036f]/g, '')
		.toLowerCase()
		.replace(/[^a-z0-9\uac00-\ud7a3]+/g, '-')
		.replace(/^-+|-+$/g, '');

	return slug || fallback;
};

tocHeadings.forEach((heading, index) => {
	const baseSlug = makeSlug(heading.textContent.trim(), `section-${index + 1}`);
	const seenCount = slugCounts.get(baseSlug) || 0;
	const nextCount = seenCount + 1;
	slugCounts.set(baseSlug, nextCount);
	heading.id = seenCount === 0 ? baseSlug : `${baseSlug}-${nextCount}`;
});

if (tocHeadings.length > 0) {
	const aside = document.createElement('aside');
	aside.className = 'toc-sidebar';

	const title = document.createElement('h2');
	title.textContent = '목차';

	const list = document.createElement('ol');

	tocHeadings.forEach((heading) => {
		const item = document.createElement('li');
		item.className = `toc-level-${heading.tagName.toLowerCase().replace('h', '')}`;

		const link = document.createElement('a');
		link.href = `#${heading.id}`;
		link.textContent = heading.textContent.trim();

		link.addEventListener('click', (event) => {
			event.preventDefault();
			heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
			history.replaceState(null, '', `#${heading.id}`);
			setActiveLink(heading.id);
		});

		item.appendChild(link);
		list.appendChild(item);
	});

	aside.append(title, list);
	document.body.appendChild(aside);
	document.body.classList.add('has-sidebar');

	const tocLinks = new Map(
		Array.from(aside.querySelectorAll('a')).map((link) => [decodeURIComponent(link.getAttribute('href').slice(1)), link])
	);

	function setActiveLink(id) {
		tocLinks.forEach((link) => link.classList.remove('is-active'));
		const activeLink = tocLinks.get(id);
		if (activeLink) {
			activeLink.classList.add('is-active');
		}
	}

	function updateActiveHeading() {
		let activeHeading = tocHeadings[0];
		for (const heading of tocHeadings) {
			if (heading.getBoundingClientRect().top <= 140) {
				activeHeading = heading;
			} else {
				break;
			}
		}

		if (activeHeading) {
			setActiveLink(activeHeading.id);
		}
	}

	window.addEventListener('scroll', updateActiveHeading, { passive: true });
	window.addEventListener('resize', updateActiveHeading);
	updateActiveHeading();
}

if (window.location.hash) {
	const hashId = decodeURIComponent(window.location.hash.slice(1));
	const target = document.getElementById(hashId);
	if (target) {
		setTimeout(() => {
			target.scrollIntoView({ behavior: 'auto', block: 'start' });
		}, 0);
	}
}
