import { mockVerification } from './verification.js';

// Initialize routes
const initializeRoutes = (app) => {
  // Endpoint for ID verification
  app.post('/verify', (req, res) => {
    const requestData = req.body;

    // Mock verification (replace with actual verification logic)
    const verificationResult = mockVerification(requestData);

    res.status(200).json(verificationResult);
  });

  // Health check endpoint
  app.get('/health', (req, res) => {
    res.status(200).json({ status: 'OK' });
  });
};

export { initializeRoutes };