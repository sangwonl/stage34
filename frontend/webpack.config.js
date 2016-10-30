var webpackPath = 'webpack.dev.js';
if (process.env.NODE_ENV == 'production' ||
    process.env.ENV == 'production') {
    webpackPath = 'webpack.prod.js';
}

module.exports = require('./config/' + webpackPath);