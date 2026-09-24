import React from 'react';

const InputField = ({ field, value, onChange, error }) => {
  return (
    <div className="form-field-group">
      <label htmlFor={field.id} className="field-label">
        <span>{field.label}</span>
        {field.unit && <span className="field-unit">({field.unit})</span>}
      </label>
      <input
        id={field.id}
        name={field.id}
        type={field.type || 'number'}
        min={field.min}
        max={field.max}
        step={field.step || 'any'}
        placeholder={field.placeholder}
        value={value !== undefined && value !== null ? value : ''}
        onChange={(e) => onChange(field.id, e.target.value)}
        className="field-input"
        aria-describedby={field.description ? `${field.id}-desc` : undefined}
      />
      {field.description && (
        <span id={`${field.id}-desc`} style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          {field.description}
        </span>
      )}
      {error && <span className="field-error">{error}</span>}
    </div>
  );
};

export default InputField;
