import React from 'react';
import { UserCheck, ShieldAlert, Activity, Cpu } from 'lucide-react';
import '../styles/cards.css';

const ICON_MAP = {
  UserCheck: UserCheck,
  ShieldAlert: ShieldAlert,
  Activity: Activity,
  Cpu: Cpu
};

const FeatureCard = ({ iconName, title, description }) => {
  const IconComponent = ICON_MAP[iconName] || Activity;

  return (
    <div className="feature-card-3d perspective-container">
      <div className="feature-card-glow"></div>
      <div className="feature-icon-wrapper">
        <IconComponent size={26} />
      </div>
      <h3 className="feature-card-title">{title}</h3>
      <p className="feature-card-text">{description}</p>
    </div>
  );
};

export default FeatureCard;
