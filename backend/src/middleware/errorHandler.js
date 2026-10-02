export class ApiError extends Error {
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

// eslint-disable-next-line no-unused-vars
export function errorHandler(err, req, res, next) {
  if (err instanceof ApiError) {
    return res.status(err.status).json({ error: { code: err.code, message: err.message } });
  }
  if (err.type === 'entity.parse.failed') {
    return res.status(400).json({ error: { code: 'INVALID_REQUEST', message: 'Invalid request.' } });
  }
  console.error(err); // details stay in server logs
  res.status(500).json({ error: { code: 'INTERNAL', message: 'Something went wrong. Please try again.' } });
}
