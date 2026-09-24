import React from 'react';

const SectionTitle = ({ tag, title, description }) => {
  return (
    <div className="section-header">
      {tag && <span className="section-tag">{tag}</span>}
      <h2 className="section-heading">{title}</h2>
      {description && <p className="section-description">{description}</p>}
    </div>
  );
};

export default SectionTitle;
