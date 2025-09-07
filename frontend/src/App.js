import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import BusinessRulesForm from "./BusinessRulesForm";
import BusinessRulesResults from "./BusinessRulesResults";
import ErrorBoundary from "./ErrorBoundary";

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Routes>
          <Route path="/" element={<BusinessRulesForm />} />
          <Route path="/results" element={<BusinessRulesResults />} />
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
