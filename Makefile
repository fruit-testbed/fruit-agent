DESTDIR=build

build:


clean:
	@[ "$(DESTDIR)" = "/" ] && exit 1 || true
	rm -rf $(DESTDIR)


install:
	@[ "$(DESTDIR)" = "" ] && exit 1 || true
	mkdir -p $(DESTDIR)/etc/init.d
	cp -f src/fruit $(DESTDIR)/etc/init.d/
	cp -f src/fruit-data $(DESTDIR)/etc/init.d/
	cp -f src/fruit-hostname $(DESTDIR)/etc/init.d/
	cp -f src/fruit-monitor $(DESTDIR)/etc/init.d/
	cp -f src/fruit-nat $(DESTDIR)/etc/init.d/
	cp -f src/fruit-netboot $(DESTDIR)/etc/init.d/
	cp -f src/fruit-netboot-files $(DESTDIR)/etc/init.d/
	cp -f src/fruit-overlay $(DESTDIR)/etc/init.d/
	cp -f src/fruit-update $(DESTDIR)/etc/init.d/
	mkdir -p $(DESTDIR)/etc/apk
	cp -f src/apk-repositories $(DESTDIR)/etc/apk/repositories
	mkdir -p $(DESTDIR)/etc/runlevels/boot
	cd $(DESTDIR)/etc/runlevels/boot && ls
	mkdir -p $(DESTDIR)/etc/runlevels/default
	cd $(DESTDIR)/etc/runlevels/default && ls
