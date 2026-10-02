import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import routes from './routes/index.js';
import { errorHandler } from './middleware/errorHandler.js';

const app = express();
app.use(cors({ origin: process.env.CORS_ORIGIN || 'http://localhost:5173' }));
app.use(express.json({ limit: '10kb' }));
app.get('/health', (_req, res) => res.json({ status: 'ok' }));
app.use('/api', routes);
app.use(errorHandler);

const port = process.env.PORT || 4000;
app.listen(port, () => console.log(`API listening on http://localhost:${port}`));
