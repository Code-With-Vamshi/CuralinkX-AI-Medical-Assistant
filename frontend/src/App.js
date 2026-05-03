import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [disease, setDisease] = useState("");
  const [location, setLocation] = useState("");
  const [whatIf, setWhatIf] = useState("");

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // =========================
  // 🔍 SINGLE ANALYZE (FIXED)
  // =========================
  const handleAnalyze = async () => {
    if (!query || !disease) {
      alert("Please enter disease and query");
      return;
    }

    setLoading(true);
    setError("");
    setData(null);

    try {
      const res = await fetch("http://127.0.0.1:5000/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          disease,
          intent: query,
          location,
          what_if: whatIf,
        }),
      });

      const result = await res.json();

      console.log("FINAL RESPONSE:", result);

      if (!res.ok) {
        throw new Error(result.error || "Something went wrong");
      }

      setData(result); // ✅ everything in one place

    } catch (err) {
      console.error(err);
      setError("⚠️ Failed to fetch AI insights");
    } finally {
      setLoading(false); // ✅ FIX loading stuck
    }
  };

  return (
    <div className="app">

      {/* LEFT PANEL */}
      <div className="sidebar">
        <h2>Curalink X</h2>
        <p className="sub">AI Medical Copilot</p>

        <input
          placeholder="Disease (e.g Diabetes)"
          value={disease}
          onChange={(e) => setDisease(e.target.value)}
        />

        <div className="stats">
          <h3>Stats</h3>
          <p>Papers <span>{data?.meta?.total_papers || 0}</span></p>
          <p>Trials <span>{data?.meta?.total_trials || 0}</span></p>
          <p>Response <span>{data?.meta?.response_time_ms || 0} ms</span></p>
        </div>
      </div>

      {/* CENTER */}
      <div className="main">
        <h1>🧠 Medical Research Assistant</h1>

        <div className="query-box">
          <textarea
            placeholder="Ask medical research question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <input
            placeholder="Location (optional)"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />

          <input
            placeholder="What-if scenario (optional)"
            value={whatIf}
            onChange={(e) => setWhatIf(e.target.value)}
          />

          <button onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>

          {loading && (
            <p className="loading">⏳ Generating AI insights...</p>
          )}

          {error && <p className="error">{error}</p>}
        </div>
      </div>

      {/* RIGHT PANEL */}
      <div className="right">

        {/* INSIGHTS */}
        <div className="card">
          <h3>Dynamic Insights</h3>
          <p style={{ whiteSpace: "pre-line" }}>
            {data?.insights || "AI insights will appear here..."}
          </p>
        </div>

        {/* PUBLICATIONS */}
        <div className="card">
          <h3>Top Research Papers</h3>

          {data?.publications?.length > 0 ? (
            data.publications.map((p, i) => (
              <div key={i} className="item">
                <h4>{p.title}</h4>
                <p className="meta">
                  {p.year} • {p.source}
                </p>
                <p className="score">Score: {p.score}</p>
                <a href={p.link} target="_blank" rel="noreferrer">
                  View Source
                </a>
              </div>
            ))
          ) : (
            <p>No publications yet</p>
          )}
        </div>

        {/* CLINICAL TRIALS */}
        <div className="card">
  <h3>Clinical Trials</h3>

  {data?.clinical_trials && data.clinical_trials.length > 0 ? (
    data.clinical_trials.map((t, i) => (
      <div key={i} className="item">
        <h4>{t.title}</h4>
        <p>Status: {t.status}</p>
        {t.info && <p>{t.info}</p>}
      </div>
    ))
  ) : (
    <p>No trials found</p>
  )}
</div>

        {/* ✅ WHAT-IF (FIXED) */}
        <div className="card">
          <h3>What-if Analysis</h3>

          {data?.what_if ? (
            <p style={{ whiteSpace: "pre-line" }}>
              {data.what_if}
            </p>
          ) : (
            <p>Enter a scenario to simulate outcomes</p>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;