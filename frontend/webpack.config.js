// webpack.config.js
const cssModuleRegex = /\.module\.css$/;
const cssRegex = /\.css$/;

module.exports = function(webpackEnv) {
    const isEnvDevelopment = webpackEnv === 'development';
    const isEnvProduction = webpackEnv === 'production';

    const getStyleLoaders = (cssOptions, preProcessor) => {
      const loaders = [
        isEnvDevelopment && require.resolve('style-loader'),
        isEnvProduction && {
          loader: MiniCssExtractPlugin.loader,
          // css is located in `static/css`, use '../../' to locate index.html folder
          // in production `paths.publicUrlOrPath` can be a relative path
          options: paths.publicUrlOrPath.startsWith('.')
            ? { publicPath: '../../' }
            : {},
        },
        {
          loader: require.resolve('css-loader'),
          options: cssOptions,
        },
        {
          // Options for PostCSS as we reference these options twice
          // Adds vendor prefixing based on your specified browser support in
          // package.json
          loader: require.resolve('postcss-loader'),
          options: {
            // Necessary for external CSS imports to work
            // https://github.com/facebook/create-react-app/issues/2677
            ident: 'postcss',
            plugins: () => [
              require('postcss-flexbugs-fixes'),
              require('postcss-preset-env')({
                autoprefixer: {
                  flexbox: 'no-2009',
                },
                stage: 3,
              }),
              // Adds PostCSS Normalize as the reset css with default options,
              // so that it honors browserslist config in package.json
              // which in turn let's users customize the target behavior as per their needs.
              postcssNormalize(),
            ],
            sourceMap: isEnvProduction && shouldUseSourceMap,
          },
        },
      ].filter(Boolean);
      if (preProcessor) {
        loaders.push(
          {
            loader: require.resolve('resolve-url-loader'),
            options: {
              sourceMap: isEnvProduction && shouldUseSourceMap,
            },
          },
          {
            loader: require.resolve(preProcessor),
            options: {
              sourceMap: true,
            },
          }
        );
      }
      return loaders;
    };
    
    return {
      module: {
        rules: [
          {
            test: [/\.bmp$/, /\.gif$/, /\.jpe?g$/, /\.png$/],
            loader: require.resolve('url-loader'),
            options: {
              limit: 1000,
              name: 'img/[name].[hash:8].[ext]',
            },
          },
          {
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            use: {
              loader: 'babel-loader'
            }
          },
          {
            test: /\.(woff|woff2)$/,
            use: {
              loader: 'url-loader',
            },
          },
          {
            test: /\.css$/,
            exclude: cssModuleRegex,
            use: [
              {
                loader: 'style-loader'
              },
              {
                loader: 'css-loader',
                options: {
                  modules: true,
                  importLoaders: 1,
                  modules: {
                    localIdentName: '[name]__[local]__[hash:base64:7]'
                  }
                }
              }
            ]
          }
        ]
      }
    }
    
  };