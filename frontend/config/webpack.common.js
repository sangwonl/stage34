var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var autoprefixer = require('autoprefixer');
var helpers = require('./helpers');

module.exports = {
    entry: {
        'polyfills': './src/polyfills.ts',
        'vendor': './src/vendor.ts',
        'app': './src/main.ts'
    },

    resolve: {
        extensions: ['', '.js', '.ts']
    },

    module: {
        loaders: [{
            test: /\.ts/,
            loaders: ['ts', 'angular2-template-loader']
        }, {
            test: /\.html/,
            loader: 'html'
        }, {
            test: /\.(png|jpe?g|gif|ico)/,
            loader: 'file?name=assets/[name].[hash].[ext]'
        }, {
            test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?/,
            loader: 'url?limit=10000&mimetype=application/font-woff'
        }, {
            test: /\.(ttf|otf)(\?v=\d+\.\d+\.\d+)?/,
            loader: 'url?limit=10000&mimetype=application/octet-stream'
        }, {
            test: /\.eot(\?v=\d+\.\d+\.\d+)?/,
            loader: 'file'
        }, {
            test: /\.svg(\?v=\d+\.\d+\.\d+)?/,
            loader: 'url?limit=10000&mimetype=image/svg+xml'
        }, {
            test: /\.css/,
            exclude: helpers.root('src'),
            loader: "style-loader!css-loader?sourceMap"
        }, {
            test: /\.css/,
            include: helpers.root('src'),
            loader: 'raw'
        }, {
            test: /\.scss/,
            exclude: /node_modules/,
            loaders: ['raw-loader', 'sass-loader']
        },
        {
            test: /bootstrap\/dist\/js\/\.js/,
            loader: 'imports?jQuery=jquery'
        }]
    },

    postcss: [autoprefixer],

    plugins: [
        new webpack.optimize.CommonsChunkPlugin({
            name: ['app', 'vendor', 'polyfills']
        }),

        new HtmlWebpackPlugin({
            template: 'src/index.html'
        }),

        new webpack.ProvidePlugin({
            'window.jQuery': 'jquery',
            jQuery: 'jquery',
            jquery: 'jquery',
            $: 'jquery'
        }),

        new webpack.DefinePlugin({
            'process.env': {
                'CONF': JSON.stringify((function() {
                    var exists = helpers.fileExists('./config.json');
                    return exists ? require('../config.json') : {};
                })())
            }
        })
    ]
};
