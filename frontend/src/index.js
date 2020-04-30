import 'react-app-polyfill/ie11';
import 'react-app-polyfill/stable';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

import App from './App';

var md = require('markdown-it')()
            .use(require('markdown-it-sub'))
            .use(require('markdown-it-sup'))
            .use(require('markdown-it-mark'))
            .use(require('markdown-it-footnote'));

const app = (
        <BrowserRouter>
            <App md={md}/>
        </BrowserRouter>
);


ReactDOM.render( app, document.getElementById('app'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();
