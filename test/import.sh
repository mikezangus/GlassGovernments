#!/bin/bash

eval $(node config.js)
mongoimport --uri "${uri}" --collection "${collection}" --type csv --headerline --file "${dataFile}"