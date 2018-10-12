DESTDIR=/

INSTALL=install

all:

clean:
	find . -iname '*.pyc' | xargs rm -f
	find . -iname '__pycache__' | xargs rm -rf

install:
	$(INSTALL) -m755 -d $(DESTDIR)/usr/sbin/
	$(INSTALL) -m750 sbin/* $(DESTDIR)/usr/sbin/

	$(INSTALL) -m755 -d $(DESTDIR)/etc/init.d/
	$(INSTALL) -m755 init-scripts/* $(DESTDIR)/etc/init.d

	$(INSTALL) -m755 -d $(DESTDIR)/etc/runlevels/boot
	ln -sf /etc/init.d/fruit-boot $(DESTDIR)/etc/runlevels/boot/fruit-boot

	$(INSTALL) -m755 -d $(DESTDIR)/etc/runlevels/default
	ln -sf /etc/init.d/fruit-default $(DESTDIR)/etc/runlevels/default/fruit-default

	$(INSTALL) -m755 -d $(DESTDIR)/boot
	rm -f $(DESTDIR)/boot/overlays
	ln -sf /media/mmcblk0p1/overlays $(DESTDIR)/boot/overlays # required by dtparam

	$(INSTALL) -m755 -d $(DESTDIR)/etc/local.d/ # rc.local scripts
	$(INSTALL) -m755 fruit-local.start $(DESTDIR)/etc/local.d/

	$(INSTALL) -m755 -d $(DESTDIR)/usr/share # default fruit.json and other common files
	cp -rp share/* $(DESTDIR)/usr/share
