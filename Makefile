.PHONY: publish clean

build:
	ansible-galaxy collection build \
		--output-path build

publish:
	ansible-galaxy collection publish \
		build/noahchalifour-pvecm-1.0.0.tar.gz

clean:
	rm -rf build/