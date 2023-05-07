/* global module, __dirname */
const HTMLWebpackPlugin = require('html-webpack-plugin');
const common = require("./webpack.common.js");
const { merge } = require("webpack-merge");
const path = require("path");

module.exports = merge(common, {
    mode: "development",
    entry: {
        "langex": path.resolve(__dirname, "../src/entry.js"),
        "langex.init": path.resolve(__dirname, "../src/langex/index.js"),
    },
    devtool: "inline-source-map",
    devServer: {
        static: [ path.resolve(__dirname, '../') ],
        port: 3003
    },
    plugins: [
        new HTMLWebpackPlugin({
            title: 'Langex App',
            template: 'webpack.html',
            filename: 'index.html'
        })
    ],
});
