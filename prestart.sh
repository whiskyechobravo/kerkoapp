#!/bin/sh

set -x
set -e

[ "$KERKO_CLEAN" = "True" ] && flask kerko clean
[ "$KERKO_CLEAN" = "True" -o "$KERKO_INDEX" = "True" ] && flask kerko index
