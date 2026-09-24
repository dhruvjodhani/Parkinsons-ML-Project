import React, { useState } from 'react';
import FormSection from '../components/FormSection';
import PredictionResult from '../components/PredictionResult';
import Disclaimer from '../components/Disclaimer';
import { FORM_SECTIONS, INITIAL_FORM_STATE } from '../data/formConfig';
import { SAMPLE_PATIENTS } from '../data/sampleData';
import { predictParkinsons } from '../services/predictionApi';
import { ArrowLeft, ArrowRight, RotateCcw, Sparkles, Loader2, Cpu } from 'lucide-react';
import '../styles/prediction.css';

const Prediction = () => {
  const [formData, setFormData] = useState(INITIAL_FORM_STATE);
  const [errors, setErrors] = useState({});
  const [activeSectionIndex, setActiveSectionIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [predictionResult, setPredictionResult] = useState(null);
  const [submitError, setSubmitError] = useState(null);
  const [sampleIndex, setSampleIndex] = useState(0);

  const currentSection = FORM_SECTIONS[activeSectionIndex];

  // Field change handler
  const handleChange = (fieldId, value) => {
    setFormData((prev) => ({
      ...prev,
      [fieldId]: value
    }));
    // Clear error for field
    if (errors[fieldId]) {
      setErrors((prev) => ({ ...prev, [fieldId]: null }));
    }
  };

  // Load sample data trigger
  const handleLoadSample = () => {
    const sample = SAMPLE_PATIENTS[sampleIndex % SAMPLE_PATIENTS.length];
    setFormData({ ...sample.data });
    setErrors({});
    setSampleIndex((prev) => prev + 1);
  };

  // Clear form trigger
  const handleClearForm = () => {
    setFormData({
    
      Age: 50,
      Gender: 0,
      Ethnicity: 0,
      EducationLevel: 0,
      BMI: 20.0,
      Smoking: 0,
      AlcoholConsumption: 0,
      PhysicalActivity: 0,
      Diet: 5.0,
      SleepQuality: 5.0,
      FamilyHistoryParkinsons: 0,
      BrainInjury: 0,
      Hypertension: 0,
      Diabetes: 0,
      Depression: 0,
      Stroke: 0,
      SystolicBP: 120,
      DiastolicBP: 80,
      CholesterolTotal: 180,
      CholesterolLDL: 100,
      CholesterolHDL: 50,
      CholesterolTriglycerides: 150,
      UPDRS: 0,
      MoCA: 30,
      FunctionalAssessment: 10,
      Tremor: 0,
      Rigidity: 0,
      Bradykinesia: 0,
      Posture: 0,
      SpeechProblems: 0,
      SleepDisorders: 0,
      Constipation: 0
    });
    setErrors({});
    setPredictionResult(null);
    setSubmitError(null);
    setActiveSectionIndex(0);
  };

  // Validate active section numeric inputs
  const validateCurrentSection = () => {
    const newErrors = {};
    let isValid = true;

    currentSection.fields.forEach((field) => {
      if (field.type === 'number') {
        const val = Number(formData[field.id]);
        if (isNaN(val) || formData[field.id] === '' || formData[field.id] === null) {
          newErrors[field.id] = 'Value is required';
          isValid = false;
        } else if (field.min !== undefined && val < field.min) {
          newErrors[field.id] = `Min value is ${field.min}`;
          isValid = false;
        } else if (field.max !== undefined && val > field.max) {
          newErrors[field.id] = `Max value is ${field.max}`;
          isValid = false;
        }
      }
    });

    setErrors(newErrors);
    return isValid;
  };

  // Step Navigation
  const handleNext = () => {
    if (validateCurrentSection()) {
      if (activeSectionIndex < FORM_SECTIONS.length - 1) {
        setActiveSectionIndex((prev) => prev + 1);
        window.scrollTo({ top: 150, behavior: 'smooth' });
      }
    }
  };

  const handlePrev = () => {
    if (activeSectionIndex > 0) {
      setActiveSectionIndex((prev) => prev - 1);
      window.scrollTo({ top: 150, behavior: 'smooth' });
    }
  };

  // Form Submission Trigger
  const handleSubmit = async (e) => {
    if (e) e.preventDefault();

    if (!validateCurrentSection()) return;

    setIsLoading(true);
    setPredictionResult(null);
    setSubmitError(null);

    try {
      const res = await predictParkinsons(formData);
      setPredictionResult(res);
      window.scrollTo({ top: 200, behavior: 'smooth' });
    } catch (err) {
      setSubmitError(
        err.message ||
          'Unable to connect to prediction server. Please start the backend and try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="section-wrapper">
      {/* Title & Subtitle Header */}
      <div className="prediction-header">
        <span className="section-tag">Machine Learning Prediction Pipeline</span>
        <h1 className="prediction-title">Parkinson's Disease Prediction</h1>
        <p className="prediction-subtitle">
          Enter patient and clinical information to generate an ML-based prediction.
        </p>
      </div>

      {/* Action Toolbar */}
      <div className="form-toolbar">
        <button type="button" onClick={handleLoadSample} className="btn-sample">
          <Sparkles size={16} />
          <span>Load Sample Data ({SAMPLE_PATIENTS[sampleIndex % SAMPLE_PATIENTS.length].name.split(' ')[2]})</span>
        </button>
        <button type="button" onClick={handleClearForm} className="btn-clear">
          <RotateCcw size={16} />
          <span>Clear Form</span>
        </button>
      </div>

      {/* Step Progress Tracker Indicator */}
      <div className="progress-stepper">
        <div className="progress-track">
          <div
            className="progress-fill"
            style={{
              width: `${(activeSectionIndex / (FORM_SECTIONS.length - 1)) * 100}%`
            }}
          ></div>
        </div>
        {FORM_SECTIONS.map((sec, idx) => (
          <div
            key={sec.id}
            className={`step-item ${idx === activeSectionIndex ? 'active' : ''} ${
              idx < activeSectionIndex ? 'completed' : ''
            }`}
            onClick={() => {
              if (idx < activeSectionIndex || validateCurrentSection()) {
                setActiveSectionIndex(idx);
              }
            }}
          >
            <div className="step-node">{idx + 1}</div>
            <span className="step-label">{sec.title.split(' ')[0]}</span>
          </div>
        ))}
      </div>

      {/* Main Form Content or Result Card */}
      {predictionResult ? (
        <PredictionResult
          result={predictionResult}
          formData={formData}
          onReset={() => {
            setPredictionResult(null);
            setSubmitError(null);
            setActiveSectionIndex(0);
          }}
        />
      ) : (
        <form onSubmit={handleSubmit}>
          {/* Active Section Component */}
          <FormSection
            section={currentSection}
            formData={formData}
            onChange={handleChange}
            errors={errors}
          />

          {submitError && (
            <div className="prediction-error" role="alert">
              {submitError}
            </div>
          )}

          {/* Form Actions Row */}
          <div className="form-actions-row">
            <button
              type="button"
              onClick={handlePrev}
              disabled={activeSectionIndex === 0}
              className="btn-secondary"
              style={{ opacity: activeSectionIndex === 0 ? 0.5 : 1, cursor: activeSectionIndex === 0 ? 'not-allowed' : 'pointer' }}
            >
              <ArrowLeft size={18} />
              <span>Previous Section</span>
            </button>

            {activeSectionIndex < FORM_SECTIONS.length - 1 ? (
              <button type="button" onClick={handleNext} className="btn-primary">
                <span>Next: {FORM_SECTIONS[activeSectionIndex + 1].title}</span>
                <ArrowRight size={18} />
              </button>
            ) : (
              <button type="submit" disabled={isLoading} className="btn-primary">
                {isLoading ? (
                  <>
                    <Loader2 size={18} className="animate-spin" />
                    <span>Analyzing Patient Data...</span>
                  </>
                ) : (
                  <>
                    <Cpu size={18} />
                    <span>Generate ML Prediction</span>
                  </>
                )}
              </button>
            )}
          </div>
        </form>
      )}

      {/* Bottom Medical Disclaimer */}
      <div style={{ marginTop: '4rem' }}>
        <Disclaimer />
      </div>
    </div>
  );
};

export default Prediction;
