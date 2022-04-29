# KAD - frontend

- [Requirements](#requirements)
    - [Installation](#installation)
    - [Overview](#overview)
- [Usage](#usage)
    - [Config](#config)
    - [Running](#running)
    - [Building](#building)
- [Troubleshooting](#troubleshooting)

## Requirements

Known working Node version: `v17.6.0`

### Installation

Using npm:
```
npm install
```

### Overview

- [React](https://github.com/facebook/react)
    - For dynamic webpages and ease of integration with api backend
- [MUI](https://github.com/mui/material-ui)
    - For layout and visual style
- [ESLint](https://github.com/eslint/eslint)
    - For code quality and linting
- [Jest](https://github.com/facebook/jest)
    - For testing

## Usage

### Config

The repo includes a [config file template](src/config.json.template) that needs to be filled out with necessary information for the module to run.

Final config file should be put at `src/config.json` 

### Running

For development / simple use, the frontend can be served with:
```
npm run start
```

### Building

For building static files to use in production:
```
npm run build
```

Point the webserver to `index.html` in the built files.

### Tests
For tests, you must first retrieve dependecies with:
```
npm install
```

Then, tests can be run with
```
npm run test
```


## Troubleshooting

TBD