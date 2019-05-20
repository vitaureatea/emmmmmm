/**
 * Created by magedu on 2017/4/20.
 */

const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    devtool: 'source-map',
    entry: {
        'app': [
            './src/index'
        ]
    },
    output: {
        path: path.join(__dirname, 'dist'),
        filename: '[name]-[hash:8].js',
        publicPath: '/ops_doc/'
    },
    resolve: {
        extensions: ['.js']
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/, // 不编译第三方包
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
        new webpack.DefinePlugin({ 'process.env': { NODE_ENV: JSON.stringify('production') } }),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            },
            sourceMap: true
        }),
        new HtmlWebpackPlugin({
            template: 'src/index.html',
            inject: true
        })
    ]
};
