import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchBusinessRules } from "./api";

const STATES = [
  "Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virgin Islands", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
];

const INDUSTRIES = [
  "Retail", "Food Service", "Construction", "Healthcare", "Professional Services", "Manufacturing", "Finance", "Education", "Technology", "Transportation", "Real Estate", "Other"
];

const SIZES = [
  "Self-employed", "1-10 employees", "11-50 employees", "51+ employees"
];

const STRUCTURES = [
  "LLC", "Corporation", "Partnership", "Sole Proprietor", "Nonprofit"
];

const COMPLIANCE_FOCUS = [
  "Tax", "Labor", "Licensing", "Environmental", "Other"
];

export default function BusinessRulesForm() {
  const [form, setForm] = useState({
    state: "",
    industry: "",
    size: "",
    structure: "",
    hasEmployees: false,
    hiresContractors: false,
    employsMinors: false,
    sellsGoods: false,
    providesServices: false,
    operatesOnline: false,
    operatesPhysical: false,
    complianceFocus: []
  });

  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    if (type === "checkbox") {
      setForm(f => ({ ...f, [name]: checked }));
    } else {
      setForm(f => ({ ...f, [name]: value }));
    }
  }

  function handleMultiSelect(e) {
    const options = Array.from(e.target.selectedOptions).map(o => o.value);
    setForm(f => ({ ...f, complianceFocus: options }));
  }

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await fetchBusinessRules(form);
      navigate("/results", { state: { results: data } });
    } catch (err) {
      setError("Failed to fetch business rules.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 500, margin: "2rem auto", padding: 24, border: "1px solid #ccc", borderRadius: 8 }}>
      <h2>Business Compliance Form</h2>
      <label>Location (State/Territory):<br />
        <select name="state" value={form.state} onChange={handleChange} required>
          <option value="">Select...</option>
          {STATES.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
      </label><br /><br />
      <label>Industry/Business Type:<br />
        <select name="industry" value={form.industry} onChange={handleChange} required>
          <option value="">Select...</option>
          {INDUSTRIES.map(i => <option key={i} value={i}>{i}</option>)}
        </select>
      </label><br /><br />
      <label>Business Size:<br />
        <select name="size" value={form.size} onChange={handleChange} required>
          <option value="">Select...</option>
          {SIZES.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
      </label><br /><br />
      <label>Business Structure:<br />
        <select name="structure" value={form.structure} onChange={handleChange} required>
          <option value="">Select...</option>
          {STRUCTURES.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
      </label><br /><br />
      <label><input type="checkbox" name="hasEmployees" checked={form.hasEmployees} onChange={handleChange} /> Has Employees</label><br />
      <label><input type="checkbox" name="hiresContractors" checked={form.hiresContractors} onChange={handleChange} /> Hires Contractors</label><br />
      <label><input type="checkbox" name="employsMinors" checked={form.employsMinors} onChange={handleChange} /> Employs Minors</label><br />
      <label><input type="checkbox" name="sellsGoods" checked={form.sellsGoods} onChange={handleChange} /> Sells Goods</label><br />
      <label><input type="checkbox" name="providesServices" checked={form.providesServices} onChange={handleChange} /> Provides Services</label><br />
      <label><input type="checkbox" name="operatesOnline" checked={form.operatesOnline} onChange={handleChange} /> Operates Online</label><br />
      <label><input type="checkbox" name="operatesPhysical" checked={form.operatesPhysical} onChange={handleChange} /> Operates Physical Location</label><br /><br />
      <label>Compliance Focus:<br />
        <select name="complianceFocus" multiple value={form.complianceFocus} onChange={handleMultiSelect} required>
          {COMPLIANCE_FOCUS.map(f => <option key={f} value={f}>{f}</option>)}
        </select>
      </label><br /><br />
      <button type="submit">Get My Rules</button>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}
