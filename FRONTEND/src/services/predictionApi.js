const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';


export const predictParkinsons = async (formData) => {
  let response;

  try {
    response = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });
  } catch {
    throw new Error(
      'Unable to connect to prediction server. Please start the backend and try again.'
    );
  }

  let data = {};
  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(data.error || 'The prediction server returned an error.');
  }

  return {
    prediction: data.prediction,
    predictionLabel: data.predictionLabel,
    probability: data.probability,
    message: data.message
  };
};
