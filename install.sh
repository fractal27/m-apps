#!/bin/bash
if [ "$1" = g ]; then
	sudo make global-install
else
	make local-install
fi
