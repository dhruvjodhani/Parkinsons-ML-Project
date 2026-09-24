import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/footer.css';

const Footer = () => {
  return (
    <footer className="site-footer">
      <div className="footer-inner">
        {/* Left Column */}
        <div className="footer-brand">
          <span className="footer-logo">Parkinson's Disease</span>
          <p className="footer-brand-tag">
            Machine Learning Prediction & Healthcare Intelligence Platform
          </p>
        </div>

        {/* Center Column */}
        <div className="footer-nav-center">
          <ul className="footer-nav-links">
            <li>
              <Link to="/" className="footer-link">Home</Link>
            </li>
            <li>
              <Link to="/about" className="footer-link">About Us</Link>
            </li>
            <li>
              <Link to="/prediction" className="footer-link">Prediction</Link>
            </li>
          </ul>
        </div>

        {/* Right Column */}
        <div className="footer-right">
          <span className="footer-tagline">AI for Awareness & Research</span>
          <span style={{ fontSize: '0.85rem', opacity: 0.7 }}>
            Educational & Clinical Data Analysis Tool
          </span>
        </div>
      </div>

      <div className="footer-divider"></div>

      {/* Disclaimer Row */}
      <div className="footer-disclaimer-row">
        <p>
          This project is intended for educational and research purposes only and does not provide medical diagnosis or medical advice.
        </p>
        <p>
          Information source:{' '}
          <a
            href="https://www.who.int/news-room/fact-sheets/detail/parkinson-disease"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-who-link"
          >
            World Health Organization (WHO) Parkinson's Disease Fact Sheet
          </a>
        </p>
      </div>
    </footer>
  );
};

export default Footer;
