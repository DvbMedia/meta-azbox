DESCRIPTION = "Hardware user space LIBs for ${MACHINE}"
SECTION = "libs"
PRIORITY = "required"
LICENSE = "CLOSED"

PR = "r0"

SRC_URI_azboxme = "http://azbox-enigma2-project.googlecode.com/files/${MACHINE}-mrua-3.11-1.tar.gz;name=azbox-mrua-${MACHINE}"
SRC_URI_azboxminime = "http://azbox-enigma2-project.googlecode.com/files/${MACHINE}-mrua-3.11-1.tar.gz;name=azbox-mrua-${MACHINE}"
SRC_URI_azboxhd = "http://azbox-enigma2-project.googlecode.com/files/${MACHINE}-mrua-2.8-1.tar.gz;name=azbox-mrua-${MACHINE}"

SRC_URI[azbox-mrua-azboxhd.md5sum] = "f595f793c42fe7985624bf76128a6843"
SRC_URI[azbox-mrua-azboxhd.sha256sum] = "7b638fff5603e8599fb61543a9c1be17ce9c8ea7d9ced536352aa57a42f37b8b"

S = "${WORKDIR}"

INHIBIT_PACKAGE_STRIP = "1"

do_install() {
    install -d ${D}${libdir}
    for f in *.so; do
        oe_libinstall -s -C ${S}/ ${f%\.*} ${D}${libdir};
    done

}
FILES_${PN} += "${libdir}/lib*"
