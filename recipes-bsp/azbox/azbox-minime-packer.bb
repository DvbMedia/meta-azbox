DESCRIPTION = "Create Azbox MiniME webinterface update image"
SECTION = "console/utils"
LICENSE = "GPL"

PV="1.3"
SRC_URI = "file://pack_minime_image.c \
	   file://Makefile.am \
	   file://configure.ac"

S = "${WORKDIR}/pack_minime_image"

inherit autotools native

do_configure_prepend() {
	install -m 0644 ${WORKDIR}/pack_minime_image.c ${S}
	install -m 0644 ${WORKDIR}/configure.ac ${S}
	install -m 0644 ${WORKDIR}/Makefile.am ${S}
}
