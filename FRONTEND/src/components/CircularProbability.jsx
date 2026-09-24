import React from 'react';
import '../styles/result.css';

const CircularProbability = ({ probability }) => {
  const percentage = Math.round(probability * 100);
  const radius = 90;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (probability * circumference);

  return (
    <div className="probability-ring-wrapper">
      <div className="ring-3d-visual">
        <svg className="probability-circle-svg" viewBox="0 0 220 220">
          <circle
            className="probability-bg-circle"
            cx="110"
            cy="110"
            r={radius}
          />
          <circle
            className="probability-fill-circle"
            cx="110"
            cy="110"
            r={radius}
            style={{
              strokeDasharray: circumference,
              strokeDashoffset: strokeDashoffset
            }}
          />
        </svg>
        <div className="probability-center-text">
          <span className="probability-value">{percentage}%</span>
          <span className="probability-label">Model Probability</span>
        </div>
      </div>

      {/* Orbiting Feature Badges */}
      <div className="orbit-node node-1">Clinical Features</div>
      <div className="orbit-node node-2">Motor Symptoms</div>
      <div className="orbit-node node-3">Medical History</div>
      <div className="orbit-node node-4">Assessment Scores</div>
    </div>
  );
};

export default CircularProbability;
