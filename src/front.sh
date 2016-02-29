#!/bin/bash
# see scripts/debian-init.d for production deployments

export PYTHONPATH=`dirname $0`
twistd -n cyclone -p 8800 -l 0.0.0.0 \
	          -r front.app.Application $*


