#!/bin/sh
revisioncount=`git log --oneline | wc -l| tr -d ' '`
projectversion=`git describe --tags --long`
cleanversion=${projectversion%%-*}
branchName=`git rev-parse --abbrev-ref HEAD`;

bigName="$projectversion-$revisioncount";
smallName="$cleanversion.$revisioncount";
fallBackName="0.0.0.$revisioncount-$branchName";

if [ -z "$projectversion" ]; then
    echo "$fallBackName";
else
    echo "$bigName";
fi
