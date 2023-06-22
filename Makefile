all: deb pip

deb: clean
	fakeroot dpkg-buildpackage -b

pip:clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build/ dist/ yttv.egg-info/ .eggs/
	rm -rf .pybuild/ debian/yttv debian/.debhelper debian/yttv.debhelper.log \
	debian/files debian/yttv.substvars debian/yttv.prerm.debhelper \
	debian/yttv.postinst.debhelper

.PHONY: all deb pip clean