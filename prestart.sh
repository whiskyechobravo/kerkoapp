#!/bin/sh

set -x
set -e

flask kerko clean
flask kerko index
