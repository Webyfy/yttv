run:
	python3 -m yttv

debug:
	python3 -m yttv --debug

portable: clean
	pyinstaller app.py --name yttv -p yttv/icons \
		--hiddenimport=yttv.icons \
		--add-data "yttv/icons/com.webyfy.yttv-48x48.png":yttv/icons
	rm -f dist/yttv/_internal/libstdc++.so.6

appimage: portable
	cp yttv/icons/com.webyfy.yttv-48x48.png dist/com.webyfy.yttv.png
	wget -c https://gitlab.com/quna/python-packaging/-/raw/main/pyinstaller2appimage \
		-O pyinstaller2appimage
	chmod +x ./pyinstaller2appimage 
	./pyinstaller2appimage -i dist/com.webyfy.yttv.png \
		-d platform/com.webyfy.yttv.desktop dist

clean:
	git clean -fdX --exclude="!pyinstaller2appimage"

.PHONY: run debug clean appimage
