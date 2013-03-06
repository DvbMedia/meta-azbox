DESCRIPTION = "Hardware drivers for ${MACHINE}"
SECTION = "base"
PRIORITY = "required"
LICENSE = "CLOSED"

KV = "3.3.1-opensat"

SRCDATE_azboxme = "20130305"
SRCDATE_azboxminime = "20130305"
SRCDATE_azboxhd = "20130305"


PV = "${KV}+${SRCDATE}"
MACHINE_KERNEL_PR_append = ".16"


SRC_URI = "http://azbox-enigma2-project.googlecode.com/files/${MACHINE}-dvb-modules-${KV}-${SRCDATE}.tar.gz;name=azbox-dvb-modules-${MACHINE}"

SRC_URI[azbox-dvb-modules-azboxhd.md5sum] = "57cea88e1bf4ded0eacc743b39aba3a1"
SRC_URI[azbox-dvb-modules-azboxhd.sha256sum] = "09f494cf74b3bd6b802d3a0e5640919c2ba679bbb9dc1faa59e3ef0ae13d5341"
SRC_URI[azbox-dvb-modules-azboxme.md5sum] = "b93828a81f4272d7ee212bec0e0e9924"
SRC_URI[azbox-dvb-modules-azboxme.sha256sum] = "ac2631c0e0d358778660a5ca24f3d4162a7c270d2c23ebaafd8b5ac48e1a29a0"
SRC_URI[azbox-dvb-modules-azboxminime.md5sum] = "fe3d0f97fcd63cca672e5f2ab246c45f"
SRC_URI[azbox-dvb-modules-azboxminime.sha256sum] = "27798dd825493550aef391b8511d1a2344193d3d2bd2aa486146b8e60ed2d32e"

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


