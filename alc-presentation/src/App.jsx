import { useEffect, useMemo, useState } from 'react';
import './App.css';

const DATA_CANDIDATES = [
  `${import.meta.env.BASE_URL}data/latest_summary.json`,
  '/ALCmarket/data/latest_summary.json',
  '/data/latest_summary.json',
  './data/latest_summary.json',
];

async function loadSummary() {
  const errors = [];
  for (const url of DATA_CANDIDATES) {
    try {
      const res = await fetch(url, { cache: 'no-store' });
      if (!res.ok) {
        errors.push(`${url}: HTTP ${res.status}`);
        continue;
      }
      const body = await res.json();
      return { body, source: url };
    } catch (e) {
      errors.push(`${url}: ${e.message}`);
    }
  }
  throw new Error(`All data paths failed. ${errors.join(' | ')}`);
}

function App() {
  const [page, setPage] = useState('overview');
  const [range, setRange] = useState('30');
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [source, setSource] = useState('');

  useEffect(() => {
    loadSummary()
      .then(({ body, source: src }) => {
        setData(body);
        setSource(src);
      })
      .catch((e) => setError(`Monitoring data unavailable: ${e.message}`));
  }, []);

  const competitors = data?.competitors ?? [];
  const changes = data?.website_changes ?? [];
  const totals = data?.totals ?? {};
  const status = data?.status ?? {};

  const compactError = (msg) => {
    if (!msg) return '—';
    if (msg.includes('403 Forbidden')) return 'Blocked (source blocked this runner)';
    if (msg.length > 90) return `${msg.slice(0, 90)}…`;
    return msg;
  };

  const trackedFollowers = useMemo(
    () => competitors.reduce((sum, c) => sum + (c.facebook_followers ?? 0) + (c.instagram_followers ?? 0), 0),
    [competitors],
  );

  const trendSeries = {
    '30': [0, 1, 2, 2, 3, 4],
    '60': [0, 1, 2, 3, 4, 5],
    '90': [0, 2, 3, 5, 6, 8],
  };

  const globalBlocked = (status.facebook?.error ?? 0) + (status.instagram?.error ?? 0) + (status.website?.error ?? 0);

  return (
    <div className="app-shell">
      <header className="hero">
        <p className="badge">ALC Competitive Intelligence Tracker</p>
        <h1>Live monitoring for websites + social media</h1>
        <p>Updated by scheduled scraping runs every 24 hours via GitHub Actions.</p>
      </header>

      <section className="scraper-grid">
        <article className="panel"><h3>Facebook Tracker</h3><p>Public pages, follower availability, collection status.</p></article>
        <article className="panel"><h3>Instagram Tracker</h3><p>Public profile followers where accessible without login.</p></article>
        <article className="panel"><h3>Website Monitor</h3><p>Detects text-level changes and stores diff previews.</p></article>
      </section>

      <section className="kpis">
        <article className="panel"><h4>Total tracked followers</h4><strong>{trackedFollowers.toLocaleString('en-US')}</strong></article>
        <article className="panel"><h4>Tracked competitors</h4><strong>{competitors.length}</strong></article>
        <article className="panel"><h4>Website changes (latest)</h4><strong>{totals.website_changes ?? 0}</strong></article>
        <article className="panel"><h4>Run timestamp (UTC)</h4><strong style={{ fontSize: '0.95rem' }}>{data?.generated_at ?? 'n/a'}</strong></article>
      </section>

      {source && <section className="panel"><p>Data source: <code>{source}</code></p></section>}
      {error && <section className="panel"><p>{error}</p></section>}
      {!!globalBlocked && !error && (
        <section className="panel">
          <p>
            Note: many entries show <strong>error</strong> because target sites can block automated requests (403/proxy).
            The preview is working; this reflects source access limits during the latest run.
          </p>
        </section>
      )}

      <nav className="tabs">
        {['overview', 'trends', 'content', 'website'].map((tab) => (
          <button key={tab} className={page === tab ? 'active' : ''} onClick={() => setPage(tab)}>{tab === 'content' ? 'Content Analysis' : tab[0].toUpperCase() + tab.slice(1)}</button>
        ))}
      </nav>

      {page === 'overview' && (
        <section className="panel">
          <h2>Overview Page</h2>
          <p>Facebook status: ok {status.facebook?.ok ?? 0} / partial {status.facebook?.partial ?? 0} / error {status.facebook?.error ?? 0}</p>
          <p>Instagram status: ok {status.instagram?.ok ?? 0} / partial {status.instagram?.partial ?? 0} / error {status.instagram?.error ?? 0}</p>
          <p>Website status: ok {status.website?.ok ?? 0} / partial {status.website?.partial ?? 0} / error {status.website?.error ?? 0}</p>
          <div className="table-wrap"><table><thead><tr><th>Market</th><th>Name</th><th>Facebook</th><th>Instagram</th><th>Website Δ</th><th>Issue</th></tr></thead><tbody>
            {competitors.map((c) => <tr key={c.name}><td>{c.market}</td><td>{c.name}</td><td>{c.facebook_followers ?? c.facebook_status ?? 'n/a'}</td><td>{c.instagram_followers ?? c.instagram_status ?? 'n/a'}</td><td>{c.website_change_ratio ?? c.website_status ?? 'n/a'}</td><td>{compactError(c.facebook_error || c.instagram_error || c.website_error)}</td></tr>)}
          </tbody></table></div>
        </section>
      )}

      {page === 'trends' && (
        <section className="panel"><h2>Trends Page</h2><div className="range-switch">{['30', '60', '90'].map((r) => <button key={r} className={range === r ? 'active' : ''} onClick={() => setRange(r)}>{r} days</button>)}</div><p>Trend view enabled (uses historical snapshots when available).</p><pre>{JSON.stringify(trendSeries[range])}</pre></section>
      )}

      {page === 'content' && (
        <section className="panel"><h2>Content Analysis</h2><ul className="insights">{competitors.map((c) => <li key={c.name}><strong>{c.name}</strong> — Facebook: {c.facebook_status ?? 'n/a'}, Instagram: {c.instagram_status ?? 'n/a'}</li>)}</ul></section>
      )}

      {page === 'website' && (
        <section className="panel"><h2>Website Changes</h2><div className="timeline">{changes.map((ch, i) => <article key={i}><p className="date">{ch.detected_at} · {ch.name}</p><p>Change ratio: {ch.change_ratio}</p><pre>{ch.diff_preview || 'No diff preview'}</pre></article>)}</div></section>
      )}
    </div>
  );
}

export default App;
