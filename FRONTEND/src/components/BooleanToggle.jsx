import React from 'react';

const BooleanToggle = ({ field, value, onChange }) => {
  const isYes = Number(value) === 1;

  return (
    <div className="form-field-group">
      <label className="field-label">
        <span>{field.label}</span>
      </label>
      <div className="segmented-control">
        <button
          type="button"
          className={`segment-btn ${!isYes ? 'active-no' : ''}`}
          onClick={() => onChange(field.id, 0)}
          aria-pressed={!isYes}
        >
          NO
        </button>
        <button
          type="button"
          className={`segment-btn ${isYes ? 'active-yes' : ''}`}
          onClick={() => onChange(field.id, 1)}
          aria-pressed={isYes}
        >
          YES
        </button>
      </div>
      {field.description && (
        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          {field.description}
        </span>
      )}
    </div>
  );
};

export default BooleanToggle;
