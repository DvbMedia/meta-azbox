DESCRIPTION = "Hardware drivers for ${MACHINE}"
SECTION = "base"
PRIORITY = "required"
LICENSE = "CLOSED"

KV = "3.3.1-opensat"

SRCDATE_azboxme = "20130204"
SRCDATE_azboxminime = "20130204"
SRCDATE_azboxhd = "20130204"


PV = "${KV}+${SRCDATE}"
MACHINE_KERNEL_PR_append = ".14"


SRC_URI = "http://azbox-enigma2-project.googlecode.com/files/${MACHINE}-dvb-modules-${KV}-${SRCDATE}.tar.gz;name=azbox-dvb-modules-${MACHINE}"

SRC_URI[azbox-dvb-modules-azboxhd.md5sum] = "8b9d9f7216ff9d0830e52b16cf40caf7"
SRC_URI[azbox-dvb-modules-azboxhd.sha256sum] = "2585c090fef7fc469665ef3492e11cab8aefc483999ebf1cd4fdbcc3796400bc"
SRC_URI[azbox-dvb-modules-azboxme.md5sum] = "1f2b389abaf6b47329fcb7f874bbf245"
SRC_URI[azbox-dvb-modules-azboxme.sha256sum] = "d2d8c35fa3cd12e9197faccdc4a9286320383da081ff6b417d21a0ec9c590464"
SRC_URI[azbox-dvb-modules-azboxminime.md5sum] = "efe429a258f06f4057306ad11f2c3f8d"
SRC_URI[azbox-dvb-modules-azboxminime.sha256sum] = "bd955cc34fed5167f20abd3b63619e640dbb62bcc9cd8b1481536d1f5dc77118"

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


