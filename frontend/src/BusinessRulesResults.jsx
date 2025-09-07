import { useLocation } from "react-router-dom";
export default function BusinessRulesResults() {
  const location = useLocation();
  // Support both { results: [...] } and { results: { results: [...] } }
  const results = location.state?.results?.results || location.state?.results;

  if (!results || results.length === 0) return <p>No results found.</p>;

  function toArray(val) {
    if (Array.isArray(val)) return val;
    if (typeof val === "string" && val.trim()) return [val];
    return [];
  }

  const flagDescriptions = {
    red: "Urgent",
    yellow: "Important",
    green: "Informational"
  };

  const flagColors = {
    red: "#f44336",
    yellow: "#ffeb3b",
    green: "#4caf50"
  };

  return (
    <div style={{ maxWidth: 800, margin: "2rem auto" }}>
      <h2>Relevant Business Rules</h2>
      {results.map((rule, idx) => (
        <div
          key={idx}
          style={{
            background: "#fff",
            border: "1px solid #e0e0e0",
            borderRadius: 12,
            boxShadow: "0 2px 8px rgba(0,0,0,0.04)",
            marginBottom: 32,
            padding: 24,
            position: "relative"
          }}
        >
          {/* Flag indicator and description */}
          <div style={{ display: "flex", alignItems: "center", position: "absolute", top: 24, right: 24 }}>
            <div
              style={{
                width: 16,
                height: 16,
                borderRadius: "50%",
                background: flagColors[rule.flag] || flagColors.green,
                border: "2px solid #e0e0e0",
                marginRight: 8
              }}
              title={rule.flag}
            />
            <span style={{ fontWeight: 500, fontSize: 13 }}>
              {flagDescriptions[rule.flag] || "Informational"}
            </span>
          </div>
          <h3 style={{ marginBottom: 4 }}>{rule.title}</h3>
          <a href={rule.url} target="_blank" rel="noopener noreferrer" style={{ color: "#1976d2" }}>
            {rule.url}
          </a>
          <div style={{ fontWeight: 500, margin: "8px 0" }}>
            Jurisdiction: {rule.jurisdiction}
          </div>
          <div style={{ margin: "12px 0", fontSize: "1.1em" }}>
            {rule.summary}
          </div>
          <div>
            <strong>Key Requirements:</strong>
            <ul>
              {toArray(rule.key_requirements).map((req, i) => (
                <li key={i}>{req}</li>
              ))}
            </ul>
          </div>
          <div>
            <strong>Recommended Actions:</strong>
            <ul>
              {toArray(rule.recommended_actions).map((act, i) => (
                <li key={i}>{act}</li>
              ))}
            </ul>
          </div>
          {toArray(rule.important_deadlines).length > 0 && (
            <div>
              <strong>Important Deadlines:</strong>
              <ul>
                {toArray(rule.important_deadlines).map((dl, i) => (
                  <li key={i}>{dl}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
