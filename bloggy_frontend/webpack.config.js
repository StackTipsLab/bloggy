const webpack = require('webpack');
const path = require('path');
// const currentTask = process.env.output
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const {VueLoaderPlugin} = require('vue-loader');
const CopyPlugin = require("copy-webpack-plugin");
// var fs = require('fs');

const config = {
    entry: {
        app: './js/index.js',
        vue: "./js/components.js"
    },

    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, "../bloggy/static/dist")
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "[name].styles.css"
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
        }),
        new VueLoaderPlugin(),
        new CopyPlugin({
            patterns: [
                {from: "assets", to: "../media"},
            ],
        }),
    ],
    module: {
        rules: [
            {
                test: /\.s[ac]ss$/,
                exclude: /node_modules/,
                use: [
                    "style-loader",
                    "css-loader",
                    "sass-loader",
                ]
            },
            {
                test: /\.js$/,
                include: '/js/',
                exclude: /node_modules/,
                loader: "babel-loader"
            },
            {
                test: /\.vue$/,
                loader: "vue-loader",
                options: {
                    runtimeCompiler: true
                }
            },
            {
                test: /\.bootstrap\.js$/,
                loader: 'babel-loader',
                options: {
                    cacheDirectory: true,
                    presets: ['@babel/preset-env']
                }
            }
        ]
    }
}

config.module.rules[0].use[0] = MiniCssExtractPlugin.loader

module.exports = (env, argv) => {
    if (argv.mode === 'development') {
        config.watch = true
        config.mode = "development"
        config.devtool = 'source-map';
        config.devtool = 'eval-source-map'

    }

    if (argv.mode === 'production') {

    }
    return config;
};
