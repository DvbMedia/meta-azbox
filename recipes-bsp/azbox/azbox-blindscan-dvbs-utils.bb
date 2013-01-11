DESCRIPTION = "Tool for DVB-S/S2 blindscan"
SECTION = "base"
PRIORITY = "optional"
LICENSE = "CLOSED"

PACKAGE_ARCH = "${MACHINE_ARCH}"
SRC_URI = "http://azbox-enigma2-project.googlecode.com/files/azbox-blindscan-utils-${MACHINE}-${PV}.tar.bz2;name=azbox-blind-${MACHINE}"

SRC_URI[azbox-blind-azboxhd.md5sum] = "702067dce4d0abb618c7a7d4e9179eb7"
SRC_URI[azbox-blind-azboxhd.sha256sum] = "51f50387c0dcea4ccfc823a08b959c1c2437cafb959cc07cb32852323e55383a"

PROVIDES += "virtual/blindscan-dvbs"
RPROVIDES_${PN} += "virtual/blindscan-dvbs"

RREPLACES_${PN} += "azbox-blindscan-utils"
RCONFLICTS_${PN} += "azbox-blindscan-utils"

PV = "1.2"
PR = "r2"

S = "${WORKDIR}/blindscan-utils"

do_install() {
	install -d "${D}/${bindir}"
	install -m 0755 "${S}/avl_azbox_blindscan" "${D}/${bindir}"
}

