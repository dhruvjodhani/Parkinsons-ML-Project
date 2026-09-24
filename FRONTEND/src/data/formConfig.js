export const FORM_SECTIONS = [
  {
    id: 'patient_info',
    title: 'Patient Information',
    subtitle: 'Demographics and baseline physical attributes',
    iconName: 'User',
    fields: [
      { id: 'Age', label: 'Age', type: 'number', min: 18, max: 100, step: 1, placeholder: 'e.g. 68', unit: 'years', description: 'Patient age in completed years' },
      { 
        id: 'Gender', 
        label: 'Gender', 
        type: 'select', 
        options: [
          { value: 0, label: 'Female' },
          { value: 1, label: 'Male' }
        ],
        description: 'Biological sex assigned at birth'
      },
      { 
        id: 'Ethnicity', 
        label: 'Ethnicity', 
        type: 'select', 
        options: [
          { value: 0, label: 'Caucasian' },
          { value: 1, label: 'African American' },
          { value: 2, label: 'Asian' },
          { value: 3, label: 'Hispanic / Other' }
        ],
        description: 'Ethnic background category'
      },
      { 
        id: 'EducationLevel', 
        label: 'Education Level', 
        type: 'select', 
        options: [
          { value: 0, label: 'None / Primary' },
          { value: 1, label: 'High School' },
          { value: 2, label: "Bachelor's Degree" },
          { value: 3, label: "Master's / Higher" }
        ],
        description: 'Highest completed level of formal education'
      },
      { id: 'BMI', label: 'Body Mass Index (BMI)', type: 'number', min: 10, max: 60, step: 0.1, placeholder: 'e.g. 24.5', unit: 'kg/m²', description: 'Ratio of mass to height squared' }
    ]
  },
  {
    id: 'lifestyle',
    title: 'Lifestyle & Habits',
    subtitle: 'Daily routine, dietary patterns, and exposure factors',
    iconName: 'Activity',
    fields: [
      { id: 'Smoking', label: 'Smoking Status', type: 'boolean', description: 'Current or long-term regular tobacco user' },
      { id: 'AlcoholConsumption', label: 'Alcohol Consumption', type: 'number', min: 0, max: 30, step: 0.1, placeholder: 'e.g. 4.5', unit: 'units/week', description: 'Average weekly alcohol units consumed' },
      { id: 'PhysicalActivity', label: 'Physical Activity', type: 'number', min: 0, max: 20, step: 0.1, placeholder: 'e.g. 2.5', unit: 'hrs/week', description: 'Weekly moderate-to-vigorous exercise hours' },
      { id: 'Diet', label: 'Diet Quality Score', type: 'number', min: 0, max: 10, step: 0.1, placeholder: 'e.g. 6.8', unit: 'scale (0-10)', description: 'Nutritional quality self/clinical rating' },
      { id: 'SleepQuality', label: 'Sleep Quality Score', type: 'number', min: 0, max: 10, step: 0.1, placeholder: 'e.g. 7.2', unit: 'scale (0-10)', description: 'Average sleep duration and restfulness score' }
    ]
  },
  {
    id: 'medical_history',
    title: 'Medical History',
    subtitle: 'Co-morbidities and hereditary clinical traits',
    iconName: 'ShieldAlert',
    fields: [
      { id: 'FamilyHistoryParkinsons', label: "Family History of Parkinson's", type: 'boolean', description: "First-degree relative diagnosed with Parkinson's" },
      { id: 'BrainInjury', label: 'Prior Traumatic Brain Injury', type: 'boolean', description: 'History of severe head injury or concussion' },
      { id: 'Hypertension', label: 'Hypertension (High BP)', type: 'boolean', description: 'Diagnosed high blood pressure condition' },
      { id: 'Diabetes', label: 'Diabetes Mellitus', type: 'boolean', description: 'Diagnosed Type 1 or Type 2 diabetes' },
      { id: 'Depression', label: 'Depression / Mood Disorder', type: 'boolean', description: 'Clinical history of major depressive episodes' },
      { id: 'Stroke', label: 'History of Stroke / TIA', type: 'boolean', description: 'Previous ischemic stroke or transient ischemic attack' }
    ]
  },
  {
    id: 'cardiovascular',
    title: 'Cardiovascular & Lab Measurements',
    subtitle: 'Vascular pressure and blood lipid biomarkers',
    iconName: 'HeartPulse',
    fields: [
      { id: 'SystolicBP', label: 'Systolic Blood Pressure', type: 'number', min: 70, max: 230, step: 1, placeholder: 'e.g. 128', unit: 'mmHg', description: 'Pressure during heartbeat contraction' },
      { id: 'DiastolicBP', label: 'Diastolic Blood Pressure', type: 'number', min: 40, max: 140, step: 1, placeholder: 'e.g. 82', unit: 'mmHg', description: 'Pressure between heartbeats' },
      { id: 'CholesterolTotal', label: 'Total Serum Cholesterol', type: 'number', min: 80, max: 500, step: 0.1, placeholder: 'e.g. 210.5', unit: 'mg/dL', description: 'Overall blood lipid concentration' },
      { id: 'CholesterolLDL', label: 'LDL Cholesterol', type: 'number', min: 30, max: 350, step: 0.1, placeholder: 'e.g. 132.4', unit: 'mg/dL', description: 'Low-density lipoprotein ("bad cholesterol")' },
      { id: 'CholesterolHDL', label: 'HDL Cholesterol', type: 'number', min: 15, max: 120, step: 0.1, placeholder: 'e.g. 48.6', unit: 'mg/dL', description: 'High-density lipoprotein ("good cholesterol")' },
      { id: 'CholesterolTriglycerides', label: 'Triglycerides', type: 'number', min: 30, max: 600, step: 0.1, placeholder: 'e.g. 185.0', unit: 'mg/dL', description: 'Blood triglyceride concentration' }
    ]
  },
  {
    id: 'neurological',
    title: 'Neurological & Clinical Scores',
    subtitle: 'Standardized motor and cognitive scale ratings',
    iconName: 'Brain',
    fields: [
      { id: 'UPDRS', label: 'UPDRS Score', type: 'number', min: 0, max: 260, step: 0.1, placeholder: 'e.g. 14.5', unit: 'scale (0-260)', description: "Unified Parkinson's Disease Rating Scale total score" },
      { id: 'MoCA', label: 'MoCA Cognitive Score', type: 'number', min: 0, max: 30, step: 0.1, placeholder: 'e.g. 27.0', unit: 'scale (0-30)', description: 'Montreal Cognitive Assessment evaluation score' },
      { id: 'FunctionalAssessment', label: 'Functional Assessment Score', type: 'number', min: 0, max: 10, step: 0.1, placeholder: 'e.g. 6.2', unit: 'scale (0-10)', description: 'Daily living functional independence rating' }
    ]
  },
  {
    id: 'symptoms',
    title: 'Clinical Symptom Evaluation',
    subtitle: 'Observed motor and non-motor clinical indicators',
    iconName: 'Stethoscope',
    fields: [
      { id: 'Tremor', label: 'Resting Tremor', type: 'boolean', description: 'Involuntary rhythmic movement at rest (hands/limbs)' },
      { id: 'Rigidity', label: 'Muscle Rigidity', type: 'boolean', description: 'Stiffness or resistance to passive limb movement' },
      { id: 'Bradykinesia', label: 'Bradykinesia (Slowness)', type: 'boolean', description: 'Slowness of physical movement and motor execution' },
      { id: 'Posture', label: 'Postural Instability', type: 'boolean', description: 'Impaired balance or stooped posture' },
      { id: 'SpeechProblems', label: 'Speech Impairment / Dysarthria', type: 'boolean', description: 'Soft, monotonous, or hesitant speech patterns' },
      { id: 'SleepDisorders', label: 'RBD / Sleep Disorders', type: 'boolean', description: 'REM sleep behavior disorder or severe insomnia' },
      { id: 'Constipation', label: 'Autonomic Constipation', type: 'boolean', description: 'Chronic gastrointestinal motility impairment' }
    ]
  }
];

export const INITIAL_FORM_STATE = {
  Age: 65,
  Gender: 1,
  Ethnicity: 0,
  EducationLevel: 2,
  BMI: 24.5,
  Smoking: 0,
  AlcoholConsumption: 2.5,
  PhysicalActivity: 3.0,
  Diet: 7.0,
  SleepQuality: 6.5,
  FamilyHistoryParkinsons: 0,
  BrainInjury: 0,
  Hypertension: 0,
  Diabetes: 0,
  Depression: 0,
  Stroke: 0,
  SystolicBP: 125,
  DiastolicBP: 80,
  CholesterolTotal: 195.0,
  CholesterolLDL: 115.0,
  CholesterolHDL: 52.0,
  CholesterolTriglycerides: 140.0,
  UPDRS: 12.0,
  MoCA: 26.5,
  FunctionalAssessment: 7.5,
  Tremor: 0,
  Rigidity: 0,
  Bradykinesia: 0,
  Posture: 0,
  SpeechProblems: 0,
  SleepDisorders: 0,
  Constipation: 0
};
