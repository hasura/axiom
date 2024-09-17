import { mockGetResponse, mockPostResponse } from './response.js';

const initializeRoutes = (app) => {
  app.get('/services/apexrest/SBQQ/ServiceRouter', (req, res) => {
    const requestData = req.body;
    const responseData = mockGetResponse(requestData);

    res.status(200).json(responseData);
  });

  app.post('/services/apexrest/SBQQ/ServiceRouter', (req, res) => {
    const requestData = req.body;
    const responseData = mockPostResponse(requestData);

    res.status(200).json(responseData);
  });

  app.get('/health', (req, res) => {
    res.status(200).json({ status: 'OK' });
  });
};

export { initializeRoutes };