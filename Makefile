DESTDIR=/

INSTALL=install

all:

clean:
	find . -iname '*.pyc' | xargs rm -f
	find . -iname '__pycache__' | xargs rm -rf

install:
	install -m755 -d $(DESTDIR)/usr/sbin/
	install -m750 sbin/* $(DESTDIR)/usr/sbin/

	install -m755 -d $(DESTDIR)/etc/init.d/
	install -m755 init-scripts/* $(DESTDIR)/etc/init.d

	install -m755 -d $(DESTDIR)/etc/runlevels/boot
	ln -sf /etc/init.d/fruit-boot $(DESTDIR)/etc/runlevels/boot/fruit-boot

	install -m755 -d $(DESTDIR)/etc/runlevels/default
	ln -sf /etc/init.d/fruit-default $(DESTDIR)/etc/runlevels/default/fruit-default

	install -m755 -d $(DESTDIR)/boot
	ln -sf /media/mmcblk0p1/overlays $(DESTDIR)/boot/overlays # required by dtparam

	install -m755 -d $(DESTDIR)/etc/local.d/ # rc.local scripts
	install -m755 fruit-local.start $(DESTDIR)/etc/local.d/

	install -m755 -d $(DESTDIR)/usr/share # default fruit.json and other common files
	cp -rp share/* $(DESTDIR)/usr/share
