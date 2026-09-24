import React from 'react';
import { Activity, Brain, ShieldAlert, Sparkles } from 'lucide-react';
import '../styles/hero.css';

const BrainVisualization3D = () => {
  return (
    <div className="hero-visual-3d perspective-container">
      <div className="brain-3d-wrapper">
        {/* Core Neural Orb */}
        <div className="neural-orb"></div>

        {/* 3D Orbiting Dotted Rings */}
        <div className="orb-ring orb-ring-1"></div>
        <div className="orb-ring orb-ring-2"></div>
      </div>

      {/* Floating 3D Cards */}
      <div className="floating-3d-card card-pos-1">
        <Brain size={18} color="#D90429" />
        <span>Motor UPDRS: 98.4%</span>
      </div>

      <div className="floating-3d-card card-pos-2">
        <Sparkles size={18} color="#D90429" />
        <span>Cognitive MoCA: 28/30</span>
      </div>

      <div className="floating-3d-card card-pos-3">
        <Activity size={18} color="#D90429" />
        <span>Dopamine Biomarkers</span>
      </div>
    </div>
  );
};

export default BrainVisualization3D;
