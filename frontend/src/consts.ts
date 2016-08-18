const mocking = false;
const forProd = process.env.ENV === 'production';
const apiHost = forProd ? 'http://api.stage34.org': 'http://localhost:8000';

export const API_BASE = mocking ? '/app' : `${apiHost}/api/v1`;