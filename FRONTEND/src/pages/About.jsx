import React from 'react';
import SectionTitle from '../components/SectionTitle';
import Disclaimer from '../components/Disclaimer';
import { WHO_FACTS } from '../data/whoData';
import { ExternalLink, Brain, Activity, Zap, AlertCircle, ShieldAlert, Stethoscope, HeartPulse, Users, Globe, CheckCircle, Cpu, FileText } from 'lucide-react';
import '../styles/about.css';

const ICON_MAP = {
  Brain,
  Activity,
  Zap,
  AlertCircle,
  ShieldAlert,
  Stethoscope,
  HeartPulse,
  Users,
  Globe,
  CheckCircle,
  Cpu,
  FileText
};

const About = () => {
  return (
    <div className="section-wrapper">
      {/* Hero Title Header */}
      <div className="about-hero">
        <span className="section-tag">WHO Clinical Fact Sheet & Research</span>
        <h1 className="about-hero-title">Understanding Parkinson's Disease</h1>
        <p className="section-description">
          Detailed neurological reference guide explaining condition characteristics, motor and non-motor symptoms, risk factors, global burden, and treatment pathways.
        </p>
        <div className="about-source-badge">
          <span>Primary Factual Reference: </span>
          <a href={WHO_FACTS.sourceUrl} target="_blank" rel="noopener noreferrer">
            World Health Organization Fact Sheet <ExternalLink size={14} style={{ display: 'inline', marginLeft: 4 }} />
          </a>
        </div>
      </div>

      {/* Grid of 12 WHO Sections */}
      <div className="about-sections-grid">
        {WHO_FACTS.sections.map((sec) => {
          const IconComponent = ICON_MAP[sec.icon] || Brain;
          return (
            <div key={sec.id} className="about-card">
              <span className="about-card-num">Section {sec.id < 10 ? `0${sec.id}` : sec.id}</span>
              <h3 className="about-card-title">
                <IconComponent size={22} color="var(--racing-red)" />
                <span>{sec.title}</span>
              </h3>
              <p className="about-card-text">{sec.content}</p>
            </div>
          );
        })}
      </div>

      {/* Bottom Medical Disclaimer */}
      <div style={{ marginTop: '3.5rem' }}>
        <Disclaimer />
      </div>
    </div>
  );
};

export default About;
