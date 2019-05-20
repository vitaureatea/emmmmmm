/**
 * Created by magedu on 2017/4/20.
 */

var ip = require('ip');
const path = require('path');
const webpack = require('webpack');

module.exports = {
    devtool: 'source-map',
    entry: {
        'app': [
            'react-hot-loader/patch',
            './src/index'
        ]
    },
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: '/ops_doc/'
    },
    resolve: {
        extensions: ['.js']
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: [
                    { loader: 'react-hot-loader/webpack' },
                    { loader: 'babel-loader' }
                ]
            },
            {
                test: /\.css$/,
                use: [
                    { loader: "style-loader" },
                    { loader: "css-loader" }
                ]

            },
            {
                test: /\.scss$/,
                use: ['style-loader', 'css-loader', 'sass-loader']
            },
            {
                test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                use: 'url-loader?limit=10000',
            },
            {
                test: /\.(ttf|eot|svg)(\?[\s\S]+)?$/,
                use: 'file-loader',
            },
            {
                test: /\.less$/,
                use: [
                    { loader: "style-loader" },
                    { loader: "css-loader" },
                    { loader: "less-loader" }
                ]
            }
        ]
    },
    plugins: [
        new webpack.optimize.OccurrenceOrderPlugin(true),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.DefinePlugin({'process.env': {NODE_ENV: JSON.stringify('development')}})
    ],
    devServer: {
        compress: true,
        host: ip.address(),
        port: 3000,
        publicPath: '/assets/',
        hot: true,
        inline: true,
        historyApiFallback: true,
        stats: {
            chunks: false
        },
        proxy: {
            '/doc': {
                target: 'http://127.0.0.1:8080',
                // pathRewrite: {'^/api': ''},
                changeOrigin: true
            }
        }
    }
};
