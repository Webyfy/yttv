run:
	python3 -m yttv

debug:
	python3 -m yttv --debug

portable: clean
	pyinstaller app.py --name yttv -p yttv/icons \
		--hiddenimport=yttv.icons \
		--add-data "yttv/icons/com.webyfy.yttv.png":yttv/icons
	rm -f dist/yttv/_internal/libstdc++.so.6

appimage: portable
	wget -c https://gitlab.com/quna/python-packaging/-/raw/main/pyinstaller2appimage \
		-O pyinstaller2appimage
	chmod +x ./pyinstaller2appimage 
	cp platform/com.webyfy.yttv.desktop dist
	sed -i '/NotShowIn/d' dist/com.webyfy.yttv.desktop
	./pyinstaller2appimage -i yttv/icons/com.webyfy.yttv.png \
		-d dist/com.webyfy.yttv.desktop dist

gen-reqs:
	pipreqs yttv --savepath requirements.txt --mode compat --force

pip: clean
	python3 setup.py sdist bdist_wheel

version := $(shell cat yttv/__init__.py | grep YTTV_VERSION | cut -d'=' -f 2 | cut -d'"' -f 2)
codename := $(shell lsb_release -a 2>/dev/null | grep Codename | cut -f 2)

deb: clean
	chmod -x debian/*.install debian/*.links debian/*.manpages
	dpkg-buildpackage -us -uc
	mv "../yttv_$(version)_all.deb" "./yttv_$(version)+$(codename)_all.deb"

man: 
	chmod +x ./run
	python3 -m help2man ./run > platform/yttv.1

clean:
	git clean -fdX --exclude="!pyinstaller2appimage"

.PHONY: run debug clean appimage deb gen-reqs pip test man
