# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# commands
.PHONY: help Makefile build up down clean logs exec

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Docker section:

# Builds the Docker environment
build:
        docker-compose build

# Brings up the Docker environment
up:
        docker-compose up -d

# Brings down the Docker environment
down:
        docker-compose down

# Cleans up Docker environment and removes volumes
clean:
        docker-compose down -v

# Views the output from containers for debugging
logs:
        docker-compose logs

# Execute a command inside the Docker app container
exec:
        docker-compose exec app bash
