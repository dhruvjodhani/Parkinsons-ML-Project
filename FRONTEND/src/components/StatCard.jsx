import React from 'react';
import '../styles/cards.css';

const StatCard = ({ number, label }) => {
  return (
    <div className="stat-card-3d perspective-container">
      <span className="stat-number">{number}</span>
      <span className="stat-label">{label}</span>
    </div>
  );
};

export default StatCard;
