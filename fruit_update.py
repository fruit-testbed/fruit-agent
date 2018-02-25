#!/usr/bin/env python

import subprocess as sp
import os
import stat
import syslog
import time


__ROOT_BACKUP__ = "/media/root-backup"


def mounted_at(dir):
	"""
	Return the device mounted at given directory. `None` if there is no such
	device.
	"""
	with open("/proc/mounts") as fin:
		for line in fin.readlines():
			dev, path, _ = line.split(" ", 2)
			if path == dir:
				return dev
	return None


def root_partitions():
	"""
	Return a tuple of (active, non_active) root partitions
	"""
	try:
		dev = mounted_at("/media/root-ro")
		if dev == "/dev/mmcblk0p3":
			return dev, "/dev/mmcblk0p2"
	except:
		pass
	return "/dev/mmcblk0p2", "/dev/mmcblk0p3"


def flag_file(root_dev, dir="/media/mmcblk0p1"):
	return os.path.join(dir, "%s.dirty" % root_dev.replace("/", "."))


def isdirty(root_dev):
	return os.path.exists(flag_file(root_dev))


def mark_dirty(root_dev):
	"""
	Mark 'root_dev' as dirty. Raise an exception when fail.
	"""
	flag = flag_file(root_dev)
	dir = os.path.dirname(flag)
	sp.check_call(["mount", "-o", "remount,rw", dir])
	with open(flag, "w"):
		pass
	sp.check_call(["mount", "-o", "remount,ro", dir])


def mark_clean(root_dev):
	"""
	Mark 'root_dev' as clean. Raise an exception when fail.
	"""
	flag = flag_file(root_dev)
	if os.path.exists(flag):
		sp.check_call(["mount", "-o", "remount,rw", dir])
		os.remove(flag)
		sp.check_call(["mount", "-o", "remount,ro", dir])


def mount_root_backup(root_dev, dir=__ROOT_BACKUP__):
	"""
	Mount given root device at root backup directory, which the default is
	'/media/root-backup'
	"""
	try:
		if not os.path.exists(dir):
			os.mkdir(dir, stat.S_IRWXU)
		sp.check_call(["mount", root_dev, dir])
		sp.check_call(["mount", "-t", "proc", "non", "%s/proc" % dir])
		sp.check_call(["mount", "-o", "bind", "/sys", "%s/sys" % dir])
		sp.check_call(["mount", "-o", "bind", "/dev", "%s/dev" % dir])
	except:
		raise RuntimeError, "Failed mounting %s at %s" % (root_dev, dir)


def unmount_root_backup(dir=__ROOT_BACKUP__):
	"""
	Unmount root device from root backup directory, which the default is
	'/media/root-backup'
	"""
	devnull = open(os.devnull, "wb")
	dirs = ["%s/dev" % dir, "%s/sys" % dir, "%s/proc" % dir, dir]
	for d in dirs:
		sp.call(["umount", "-f", d], stdout=devnull, stderr=devnull)
	if mounted_at(dir) is not None:
		raise RuntimeError, "Failed unmounting %s" % (dir)


def apk_upgrade(dir=__ROOT_BACKUP__):
	"""
	Perform `apk upgrade` on root backup directory, which the default is
	'/media/root-backup'
	"""
	update_stdout = os.path.join(tempfile.gettempdir(),
								 ".fruit_update.apk.update.stdout")
	update_stderr = os.path.join(tempfile.gettempdir(),
								 ".fruit_update.apk.update.stderr")
	sp.call(["apk", "-q", "--root", dir, "update"],
			stdout=open(update_stdout, "w"),
			stderr=open(update_stderr, "w"))

	upgrade_stdout = os.path.join(tempfile.gettempdir(),
								 ".fruit_update.apk.upgrade.stdout")
	upgrade_stderr = os.path.join(tempfile.gettempdir(),
								 ".fruit_update.apk.upgrade.stderr")
	sp.check_call(["apk", "--root", dir, "--purge", "--wait", "1200", "upgrade"],
				  stdout=open(upgrade_stdout, "w"),
				  stderr=open(upgrade_stderr, "w"))
	out = sp.check_output(["grep", " Upgrading ", upgrade_stdout]).strip()
	if out == "":
		return 0
	return len(out.split("\n"))


def update():
	"""
	Update the non-active root partition by upgrading its software packages.
	"""
	active, nonactive = root_partitions()
	try:
		devnull = open(os.devnull, "wb")
		unmount_root_backup()

		if isdirty(nonactive):
			syslog.syslog(syslog.LOG_WARNING, "Recovering dirty (non-active) root partition %s" % nonactive)
			sp.check_call(["dd", "if=%s" % active, "of=%s" % nonactive], stderr=devnull)

		mark_dirty(nonactive)
		mount_root_backup(nonactive)
		total_upgraded = apk_upgrade()
		unmount_root_backup(nonactive)
		mark_clean(nonactive)

		if total_upgraded > 0:
			with open("/run/fruit_update.reboot", "w+") as fout:
				fout.write("%f %d\n" % (time.time(), total_upgraded))

	except:
		pass
        t, val, trace = sys.exc_info()
        syslog.syslog(syslog.LOG_ERR, "Failed updating %s - %s" % (nonactive, val))
		unmount_root_backup(nonactive)
        raise t, val, trace


if __name__ == "__main__":
	syslog.openlog(ident=os.path.basename(__file__))
	update()
