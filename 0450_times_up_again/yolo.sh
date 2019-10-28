#!/bin/bash

res=`grep -o '(.*)' | bc`
echo -n $res >&1
