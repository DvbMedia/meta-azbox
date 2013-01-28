DESCRIPTION = "Hardware drivers for ${MACHINE}"
SECTION = "base"
PRIORITY = "required"
LICENSE = "CLOSED"

KV = "3.3.1-opensat"

SRCDATE_azboxme = "20130123"
SRCDATE_azboxminime = "20130123"
SRCDATE_azboxhd = "20130125"


PV = "${KV}+${SRCDATE}"
MACHINE_KERNEL_PR_append = ".13"


SRC_URI = "http://azbox-enigma2-project.googlecode.com/files/${MACHINE}-dvb-modules-${KV}-${SRCDATE}.tar.gz;name=azbox-dvb-modules-${MACHINE}"

SRC_URI[azbox-dvb-modules-azboxhd.md5sum] = "eca4bf5a0e744d8550a0479d0aa91072"
SRC_URI[azbox-dvb-modules-azboxhd.sha256sum] = "787204cf1bdbd0ae0a0113403d75605e2f916319f01dde997c57af7adde96dc5"
SRC_URI[azbox-dvb-modules-azboxme.md5sum] = "550a2f55e0061c55696f01d3619af745"
SRC_URI[azbox-dvb-modules-azboxme.sha256sum] = "19932210adbed6e38ef703133883c91352c31e7787b6811b298647e6d369ecf5"
SRC_URI[azbox-dvb-modules-azboxminime.md5sum] = "9cfe07854d615b587c5f632f2c14b92a"
SRC_URI[azbox-dvb-modules-azboxminime.sha256sum] = "5046abf091e443ece67e2b908102bfef68c479c53f72110f7db1eb47182961b3"

S = "${WORKDIR}"


PACKAGE_STRIP = "no"

inherit module

do_compile() {
}

do_install_azboxhd() {
    install -d ${D}/lib/modules/${KV}/extra
    install -d ${D}/${sysconfdir}/modutils

    for f in llad em8xxx 863xi2c az_cx24116 az_mxl201rf az_mxl5007t az_stv6110x az_stv090x az_tda10023 az_zl10353 nimdetect sci 863xdvb; do
	install -m 0644 ${WORKDIR}/$f.ko ${D}/lib/modules/${KV}/extra/$f.ko
	echo $f >> ${D}/${sysconfdir}/modutils/_${MACHINE}
    done

    install -d ${D}/lib/firmware
    install -m 0644 ${WORKDIR}/dvb-fe-cx24116.fw ${D}/lib/firmware/dvb-fe-cx24116.fw

}

do_install_azboxme() {
    install -d ${D}/lib/modules/${KV}/extra
    install -d ${D}/${sysconfdir}/modutils

    for f in llad em8xxx 865xi2c avl6211 avl2108 mxl241sf nimdetect sci 865xdvb; do
	install -m 0644 ${WORKDIR}/$f.ko ${D}/lib/modules/${KV}/extra/$f.ko
	echo $f >> ${D}/${sysconfdir}/modutils/_${MACHINE}
    done

    install -d ${D}/lib/firmware
    install -m 0644 ${WORKDIR}/dvb-fe-avl2108.fw ${D}/lib/firmware/dvb-fe-avl2108.fw
    install -m 0644 ${WORKDIR}/dvb-fe-avl2108-blind.fw ${D}/lib/firmware/dvb-fe-avl2108-blind.fw
    install -m 0644 ${WORKDIR}/dvb-fe-avl6211.fw ${D}/lib/firmware/dvb-fe-avl6211.fw

}

do_install_azboxminime() {
 do_install_azboxme
}

FILES_${PN} = "/"


