#!/bin/bash
echo "salam";
managePath=$1
echo "salam $managePath";
python "$managePath" migrate;
echo "salam";
supervisord -n;
echo "salam";