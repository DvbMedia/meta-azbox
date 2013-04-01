DESCRIPTION = "Azbox AZplayer app plugin"
RDEPENDS = "enigma2 curl fuse libupnp"
LICENSE = "CLOSED"

inherit pkgconfig

PR = "r11"

SRC_URI = "file://bin \
	   file://lib \
	   file://img \
	   file://plugin \
	  "

do_compile() {
	python -O -m compileall ${WORKDIR}
}

python populate_packages_prepend () {
	enigma2_plugindir = bb.data.expand('${libdir}/enigma2/python/Plugins', d)

	do_split_packages(d, enigma2_plugindir, '^(\w+/\w+)/[a-zA-Z0-9_]+.*$', 'enigma2-plugin-%s', 'Enigma2 Plugin: %s', recursive=True, match_path=True, prepend=True)
	do_split_packages(d, enigma2_plugindir, '^(\w+/\w+)/.*\.py$', 'enigma2-plugin-%s-src', 'Enigma2 Plugin: %s', recursive=True, match_path=True, prepend=True)
	do_split_packages(d, enigma2_plugindir, '^(\w+/\w+)/(.*/)?\.debug/.*$', 'enigma2-plugin-%s-dbg', 'Enigma2 Plugin: %s', recursive=True, match_path=True, prepend=True)
}

do_install_azboxhd() {
	install -d ${D}/usr/bin/
	install -m 0755 ${WORKDIR}/bin/rmfp_player-ForHD ${D}/usr/bin/rmfp_player

	install -m 0755 ${WORKDIR}/bin/djmount ${D}/usr/bin/

	install -d ${D}/etc/init.d
	install -m 0755 ${WORKDIR}/bin/init ${D}/etc/init.d/djmount


	install -d ${D}/usr/lib/
	install -m 0755 ${WORKDIR}/lib/lib* ${D}/usr/lib/

	install -d ${D}/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/
	install -m 0755 ${WORKDIR}/plugin/*.pyo ${D}/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/

        install -d ${D}/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/img/
        install -m 0755 ${WORKDIR}/img/*.png ${D}/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/img/
}

do_install_azboxme() {
	install -d ${D}/usr/bin/
	install -m 0755 ${WORKDIR}/bin/rmfp_player ${D}/usr/bin/

	install -m 0755 ${WORKDIR}/bin/djmount ${D}/usr/bin/

	install -d ${D}/etc/init.d
	install -m 0755 ${WORKDIR}/bin/init ${D}/etc/init.d/djmount


	install -d ${D}/usr/lib/
	install -m 0755 ${WORKDIR}/lib/lib* ${D}/usr/lib/

	install -d ${D}/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/
	install -m 0755 ${WORKDIR}/plugin/*.pyo ${D}/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/

        install -d ${D}/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/img/
        install -m 0755 ${WORKDIR}/img/*.png ${D}/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/img/
}

do_install_azboxminime() {
do_install_azboxme
}

FILES_${PN} = "/usr/bin/"
FILES_${PN} += "/usr/lib/"
FILES_${PN} += "/etc/init.d/"
FILES_${PN} += "/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/"
FILES_${PN} += "/usr/lib/enigma2/python/Plugins/Extensions/AZPlay/img/"



