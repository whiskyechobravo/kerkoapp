#!/bin/sh

set -x
set -e

if [ "$KERKO_CLEAN" = "True" ]; then 
  flask kerko clean
fi

if [ "$KERKO_CLEAN" = "True" -o "$KERKO_INDEX" = "True" ]; then
  flask kerko index
fi
