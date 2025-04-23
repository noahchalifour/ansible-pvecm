#==============================================================================
# Ansible Collection Makefile
#==============================================================================

.PHONY: version info publish clean

#------------------------------------------------------------------------------
# Configuration
#------------------------------------------------------------------------------
# Extract metadata from galaxy.yml (macOS/Linux compatible)
VERSION   := $(shell sed -n 's/^version: //p' galaxy.yml | tr -d ' ')
NAMESPACE := $(shell sed -n 's/^namespace: //p' galaxy.yml | tr -d ' ')
NAME      := $(shell sed -n 's/^name: //p' galaxy.yml | tr -d ' ')
ARTIFACT  := build/$(NAMESPACE)-$(NAME)-$(VERSION).tar.gz

#------------------------------------------------------------------------------
# Targets
#------------------------------------------------------------------------------
# Default target
all: build

# Build the collection
build:
	@echo "Building collection $(NAMESPACE).$(NAME) v$(VERSION)..."
	ansible-galaxy collection build \
		--output-path build

# Publish the collection to Ansible Galaxy
publish: build
	@echo "Publishing collection to Ansible Galaxy..."
	ansible-galaxy collection publish $(ARTIFACT)

# Clean build artifacts
clean:
	@echo "Cleaning build directory..."
	rm -rf build/

# Show collection info
info:
	@echo "Collection: $(NAMESPACE).$(NAME)"
	@echo "Version:    $(VERSION)"
	@echo "Artifact:   $(ARTIFACT)"

# Update version in galaxy.yml
# Usage: make version VERSION=x.y.z
version:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION parameter is required. Usage: make version VERSION=x.y.z"; \
		exit 1; \
	fi
	@echo "Updating version to $(VERSION)..."
	@sed -i '' 's/^version:.*$$/version: $(VERSION)/' galaxy.yml
	@echo "Version updated to $(VERSION)"
	@echo "Don't forget to commit the changes!"
