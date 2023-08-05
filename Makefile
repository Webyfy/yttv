all: deb pip

run:
	python3 setup.py build
	python3 -m yttv

deb: clean
	fakeroot dpkg-buildpackage -us -uc -b

pip:clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build/ dist/ yttv.egg-info/ .eggs/
	rm -rf .pybuild/ debian/yttv debian/.debhelper debian/yttv.debhelper.log \
	debian/files debian/yttv.substvars debian/yttv.prerm.debhelper \
	debian/yttv.postinst.debhelper usr

.PHONY: all deb pip clean run