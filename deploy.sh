#! /usr/bin/env bash
git add -f env/etc
eb deploy --staged --profile ubic
git reset HEAD env/etc