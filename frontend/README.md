# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

Before running, install the necessary packages with

```
npm install
```

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

You must also activate the local cors proxy to work with locally hosted endpoints

### `lcp --proxyUrl http://localhost:8000`

Runs local-cors-proxy node JS package to locally proxy around CORS issues.
This will save us from wanting to drop-out of college due to CORS issues.
https://www.npmjs.com/package/local-cors-proxy
