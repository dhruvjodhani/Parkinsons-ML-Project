import React from 'react';

const SelectField = ({ field, value, onChange, error }) => {
  return (
    <div className="form-field-group">
      <label htmlFor={field.id} className="field-label">
        <span>{field.label}</span>
      </label>
      <select
        id={field.id}
        name={field.id}
        value={value !== undefined && value !== null ? value : field.options[0]?.value}
        onChange={(e) => onChange(field.id, Number(e.target.value))}
        className="field-select"
      >
        {field.options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {field.description && (
        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          {field.description}
        </span>
      )}
      {error && <span className="field-error">{error}</span>}
    </div>
  );
};

export default SelectField;
