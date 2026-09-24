import React from 'react';
import InputField from './InputField';
import SelectField from './SelectField';
import BooleanToggle from './BooleanToggle';
import { User, Activity, ShieldAlert, HeartPulse, Brain, Stethoscope } from 'lucide-react';

const ICON_MAP = {
  User,
  Activity,
  ShieldAlert,
  HeartPulse,
  Brain,
  Stethoscope
};

const FormSection = ({ section, formData, onChange, errors }) => {
  const IconComponent = ICON_MAP[section.iconName] || Activity;

  return (
    <div className="form-section-card">
      <div className="form-section-header">
        <div className="form-section-icon">
          <IconComponent size={24} />
        </div>
        <div>
          <h3 className="form-section-title-text">{section.title}</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{section.subtitle}</p>
        </div>
      </div>

      <div className="form-fields-grid">
        {section.fields.map((field) => {
          if (field.type === 'select') {
            return (
              <SelectField
                key={field.id}
                field={field}
                value={formData[field.id]}
                onChange={onChange}
                error={errors[field.id]}
              />
            );
          }
          if (field.type === 'boolean') {
            return (
              <BooleanToggle
                key={field.id}
                field={field}
                value={formData[field.id]}
                onChange={onChange}
              />
            );
          }
          return (
            <InputField
              key={field.id}
              field={field}
              value={formData[field.id]}
              onChange={onChange}
              error={errors[field.id]}
            />
          );
        })}
      </div>
    </div>
  );
};

export default FormSection;
