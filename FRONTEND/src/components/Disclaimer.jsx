import React from 'react';
import { AlertTriangle } from 'lucide-react';
import '../styles/result.css';

const Disclaimer = ({ text, showWhoSource = true }) => {
  return (
    <div className="disclaimer-box">
      <AlertTriangle size={20} className="disclaimer-icon" />
      <div>
        <p>
          <strong>Educational & Research Disclaimer: </strong>
          {text || "This application provides a machine-learning prediction for educational purposes only. It is not a medical diagnosis and should not replace evaluation by a qualified healthcare professional."}
        </p>
        {showWhoSource && (
          <p style={{ marginTop: '0.4rem', fontSize: '0.82rem', opacity: 0.85 }}>
            Factual clinical reference information sourced from the{' '}
            <a
              href="https://www.who.int/news-room/fact-sheets/detail/parkinson-disease"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'var(--racing-red)', fontWeight: 600, textDecoration: 'underline' }}
            >
              World Health Organization (WHO) Parkinson's Disease Fact Sheet
            </a>.
          </p>
        )}
      </div>
    </div>
  );
};

export default Disclaimer;
