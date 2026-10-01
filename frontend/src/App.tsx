import { useEffect, useState } from 'react';
import './App.css';
import type { AnalyzerData } from './types';

function App() {
  const [data, setData] = useState<AnalyzerData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'packages' | 'node_modules' | 'home' | 'insights'>('packages');

  useEffect(() => {
    fetch('/data.json')
      .then((res) => {
        if (!res.ok) {
          throw new Error('Failed to fetch data.json');
        }
        return res.json();
      })
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container">Loading analysis data...</div>;
  if (error) return <div className="container error">Error: {error}. Please run the analyzer script first.</div>;
  if (!data) return null;

  return (
    <div className="container">
      <header>
        <h1>Linux Analyzer Report</h1>
        <p>Generated at: {new Date(data.generated_at).toLocaleString()}</p>
      </header>

      <div className="tabs">
        <button className={activeTab === 'packages' ? 'active' : ''} onClick={() => setActiveTab('packages')}>Packages</button>
        <button className={activeTab === 'node_modules' ? 'active' : ''} onClick={() => setActiveTab('node_modules')}>Node Modules</button>
        <button className={activeTab === 'home' ? 'active' : ''} onClick={() => setActiveTab('home')}>Home Dir</button>
        <button className={activeTab === 'insights' ? 'active' : ''} onClick={() => setActiveTab('insights')}>AI Insights</button>
      </div>

      <main>
        {activeTab === 'packages' && (
          <section>
            <h2>Manually Installed Packages</h2>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Size (KB)</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {data.manual_packages.map((pkg) => (
                    <tr key={pkg.name}>
                      <td>{pkg.name}</td>
                      <td>{pkg.size_kb.toLocaleString()}</td>
                      <td>{pkg.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {activeTab === 'node_modules' && (
          <section>
            <h2>Node Modules</h2>
            <p>Total Size: {(data.node_modules.reduce((acc, curr) => acc + curr.size_kb, 0) / 1024).toFixed(2)} MB</p>
            {data.pnpm_store && (
              <div className="card">
                <h3>PNPM Store</h3>
                <p>Path: {data.pnpm_store.path}</p>
                <p>Size: {(data.pnpm_store.size_kb / 1024).toFixed(2)} MB</p>
              </div>
            )}
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Path</th>
                    <th>Size (KB)</th>
                    <th>Last Modified</th>
                  </tr>
                </thead>
                <tbody>
                  {data.node_modules.map((nm) => (
                    <tr key={nm.path}>
                      <td>{nm.path}</td>
                      <td>{nm.size_kb.toLocaleString()}</td>
                      <td>{new Date(nm.last_modified).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {activeTab === 'home' && (
          <section>
            <h2>Home Directory Analysis</h2>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Directory</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {data.home_dir_analysis.map((item) => (
                    <tr key={item.name}>
                      <td>{item.name}</td>
                      <td>{item.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {activeTab === 'insights' && (
          <section>
            <h2>AI Insights</h2>
            <div className="insight-card">
              <h3>Categorization</h3>
              <div dangerouslySetInnerHTML={{ __html: formatMarkdown(data.ai_insights.categorized_packages) }} />
            </div>
            <div className="insight-card">
              <h3>Package Explanations</h3>
              <div dangerouslySetInnerHTML={{ __html: formatMarkdown(data.ai_insights.explained_packages) }} />
            </div>
            <div className="insight-card">
              <h3>Cryptic Packages</h3>
              <div dangerouslySetInnerHTML={{ __html: formatMarkdown(data.ai_insights.explained_cryptic_packages) }} />
            </div>
            <div className="insight-card">
              <h3>Recommendations</h3>
              <div dangerouslySetInnerHTML={{ __html: formatMarkdown(data.ai_insights.recommendations) }} />
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

// Simple markdown formatter (replace with a library if needed, but keeping it lightweight as requested)
function formatMarkdown(text: string) {
  if (!text) return '';
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br />');
}

export default App;
