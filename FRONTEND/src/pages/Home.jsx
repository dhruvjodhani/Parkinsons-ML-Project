import React from 'react';
import Hero from '../components/Hero';
import SectionTitle from '../components/SectionTitle';
import FeatureCard from '../components/FeatureCard';
import StatCard from '../components/StatCard';
import Disclaimer from '../components/Disclaimer';
import { WHO_FACTS } from '../data/whoData';
import '../styles/cards.css';

const Home = () => {
  const features = [
    {
      iconName: 'UserCheck',
      title: 'Patient Analysis',
      description: 'Comprehensive demographic, anthropometric (BMI), and personal health feature evaluation.'
    },
    {
      iconName: 'ShieldAlert',
      title: 'Clinical Risk Factors',
      description: 'Assessment of cardiovascular conditions, vascular history, and genetic predisposition markers.'
    },
    {
      iconName: 'Activity',
      title: 'Symptom Assessment',
      description: 'Evaluation of motor tremors, rigidity, bradykinesia, and non-motor autonomic dysfunction.'
    },
    {
      iconName: 'Cpu',
      title: 'ML-Based Prediction',
      description: 'Multi-parametric machine learning model generating statistical risk probability scores.'
    }
  ];

  return (
    <div>
      {/* Hero Banner */}
      <Hero />

      {/* Feature Cards Section */}
      <section className="section-wrapper">
        <SectionTitle
          tag="Core Platform Capabilities"
          title="Intelligent Parkinson's Feature Analysis"
          description="Combining multi-dimensional clinical measurements and neurological scale assessments into a unified prediction pipeline."
        />

        <div className="features-grid">
          {features.map((item, idx) => (
            <FeatureCard
              key={idx}
              iconName={item.iconName}
              title={item.title}
              description={item.description}
            />
          ))}
        </div>
      </section>

      {/* WHO Statistics Section */}
      <section className="stats-section">
        <div className="section-wrapper" style={{ padding: 0 }}>
          <SectionTitle
            tag="Global Impact Overview"
            title="World Health Organization Key Insights"
            description="Statistical data from global healthcare evaluations on Parkinson's disease prevalence and burden."
          />

          <div className="stats-grid">
            {WHO_FACTS.stats.map((stat, idx) => (
              <StatCard key={idx} number={stat.number} label={stat.label} />
            ))}
          </div>

          <div className="stat-source-wrapper">
            <span>Source: World Health Organization (WHO) Parkinson's Disease Fact Sheet (2019 Estimates)</span>
          </div>
        </div>
      </section>

      {/* Educational Disclaimer Banner */}
      <section className="section-wrapper" style={{ paddingTop: 0 }}>
        <Disclaimer />
      </section>
    </div>
  );
};

export default Home;
