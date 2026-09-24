import React, { useState, useEffect } from 'react';
import { NavLink, Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import { Activity, Menu, X, Home, Info, Cpu } from 'lucide-react';
import '../styles/header.css';

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile drawer on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location]);

  return (
    <header className={`site-header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="header-inner">
        {/* LEFT: Brand Logo */}
        <Link to="/" className="brand-logo" aria-label="Parkinson's Disease AI Prediction Home">
          <div className="brand-icon-wrapper">
            <Activity size={22} />
          </div>
          <span className="brand-title">Parkinson's Disease</span>
        </Link>

        {/* CENTER: Navigation Links (Pill Style) */}
        <nav className="header-nav" aria-label="Main Navigation">
          <ul className="nav-pill-list">
            <li>
              <NavLink
                to="/"
                className={({ isActive }) => `nav-link-pill ${isActive ? 'active' : ''}`}
                end
              >
                <Home size={16} />
                <span>Home</span>
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/about"
                className={({ isActive }) => `nav-link-pill ${isActive ? 'active' : ''}`}
              >
                <Info size={16} />
                <span>About Us</span>
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/prediction"
                className={({ isActive }) => `nav-link-pill ${isActive ? 'active' : ''}`}
              >
                <Cpu size={16} />
                <span>Prediction</span>
              </NavLink>
            </li>
          </ul>
        </nav>

        {/* RIGHT: Actions (Theme Toggle + Mobile Drawer Toggle) */}
        <div className="header-actions">
          <ThemeToggle />
          <button
            className="mobile-toggle-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle Navigation Menu"
          >
            {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      <div className={`mobile-drawer ${mobileMenuOpen ? 'open' : ''}`}>
        <NavLink
          to="/"
          className={({ isActive }) => `nav-link-pill ${isActive ? 'active' : ''}`}
          end
        >
          <Home size={18} />
          <span>Home</span>
        </NavLink>
        <NavLink
          to="/about"
          className={({ isActive }) => `nav-link-pill ${isActive ? 'active' : ''}`}
        >
          <Info size={18} />
          <span>About Us</span>
        </NavLink>
        <NavLink
          to="/prediction"
          className={({ isActive }) => `nav-link-pill ${isActive ? 'active' : ''}`}
        >
          <Cpu size={18} />
          <span>Prediction</span>
        </NavLink>
      </div>
    </header>
  );
};

export default Header;
