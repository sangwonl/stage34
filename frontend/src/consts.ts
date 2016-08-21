const mocking = false;
const forProd = process.env.ENV === 'production';
const hostBase = forProd ? 'http://api.stage34.org': 'http://localhost:8000';

export const STAGE34_HOST_BASE = hostBase;
export const STAGE34_API_BASE = mocking ? '/app' : `${hostBase}/api/v1`;
export const GITHUB_API_BASE = 'https://api.github.com';
