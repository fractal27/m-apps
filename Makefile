
PREFIX=/usr/local

all: update 


update:
	m-apps update all

install:
	cat m-apps > $(PREFIX)/bin/m-apps
	chmod +x $(PREFIX)/bin/m-apps

.PHONY: update all
