import express from 'express';
import swaggerUi from 'swagger-ui-express';
import yaml from 'js-yaml';
import fs from 'fs';
import bodyParser from 'body-parser';
import { initializeRoutes } from './routes.js';

const app = express();

// Use body-parser middleware for parsing JSON requests
app.use(bodyParser.json());

// Serve Swagger UI for API documentation
const yamlFilePath = './salesforce.openapi.yaml';
const swaggerDocument = yaml.load(fs.readFileSync(yamlFilePath, 'utf8'));
const options = {
  swaggerOptions: {
      url: "/docs/swagger.json",
  },
}
app.get("/docs/swagger.json", (req, res) => res.json(swaggerDocument));
app.use('/docs', swaggerUi.serveFiles(null, options), swaggerUi.setup(null, options));

// Initialize routes
initializeRoutes(app);

// Start the server
const port = process.env.PORT || 4016;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});