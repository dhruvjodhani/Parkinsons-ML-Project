import React from 'react';
import { Link } from 'react-router-dom';
import BrainVisualization3D from './BrainVisualization3D';
import { ArrowRight, BookOpen, Sparkles } from 'lucide-react';
import '../styles/hero.css';

const Hero = () => {
  return (
    <section className="hero-section">
      {/* Background ambient glowing particles */}
      <div className="hero-bg-particles">
        <div className="hero-particle hero-particle-1"></div>
        <div className="hero-particle hero-particle-2"></div>
      </div>

      <div className="hero-grid">
        {/* Left Column: Content */}
        <div className="hero-content">
          <div className="hero-badge">
            <span className="badge-dot"></span>
            <span>AI-Powered Parkinson's Disease Prediction</span>
          </div>

          <h1 className="hero-title">
            Understanding Parkinson's.
            <span className="hero-title-accent">Predicting With Intelligence.</span>
          </h1>

          <p className="hero-subtitle">
            Explore an AI-assisted prediction platform designed to analyze patient health and clinical features using machine learning.
          </p>

          <div className="hero-actions">
            <Link to="/prediction" className="btn-primary">
              <span>Start Prediction</span>
              <ArrowRight size={18} />
            </Link>
            <Link to="/about" className="btn-secondary">
              <BookOpen size={18} />
              <span>Learn About Parkinson's</span>
            </Link>
          </div>
        </div>

        {/* Right Column: 3D Visualization */}
        <BrainVisualization3D />
      </div>
    </section>
  );
};

export default Hero;
