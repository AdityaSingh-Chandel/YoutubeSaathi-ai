import { Router } from 'express';
import * as c from '../controllers/videoController.js';

const router = Router();
// Express 4 doesn't catch async errors, so wrap handlers.
const wrap = (fn) => (req, res, next) => fn(req, res).catch(next);

router.post('/analyze', wrap(c.analyze));
router.post('/question', wrap(c.question));
router.delete('/session/:id', wrap(c.removeSession));

export default router;
