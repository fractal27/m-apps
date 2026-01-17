
PREFIX_GLOBAL=/usr/local
PREFIX_LOCAL=~/.local

all: update 


update:
	./m-apps update all

global-install:
	@{ \
		ln -s $(PWD)/m-apps $(PREFIX_GLOBAL)/bin/m-apps &&\
		chmod +x $(PREFIX_GLOBAL)/bin/m-apps &&\
		printf "\033[32mSuccessfully installed \`m-apps\` globally into '$(PREFIX_GLOBAL)/bin'\n";\
	} || { \
		printf "\033[31mError accurred while installing \`m-apps\` globally into '$(PREFIX_GLOBAL)/bin'\n";\
	}

local-install:
	@{ \
		ln -s $(PWD)/m-apps $(PREFIX_LOCAL)/bin/m-apps &&\
		chmod +x $(PREFIX_LOCAL)/bin/m-apps &&\
		printf "\033[32mSuccessfully installed \`m-apps\` locally into '$(PREFIX_LOCAL)/bin'\n";\
	} || { \
		printf "\033[31mError accurred while installing \`m-apps\` locally into '$(PREFIX_LOCAL)/bin'\n";\
	}

.PHONY: update all 
