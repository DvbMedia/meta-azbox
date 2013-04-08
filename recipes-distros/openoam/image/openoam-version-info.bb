DESCRIPTION = "OpenOAM version info"
SECTION = "base"
PRIORITY = "required"
LICENSE = "proprietary"
MAINTAINER = "OpenOAM"

require conf/license/license-gplv2.inc

PV = "${IMAGE_VERSION}"
PR = "r${DATETIME}-${DISTRO_TYPE}"
PACKAGE_ARCH = "${MACHINE_ARCH}"

URL = "http://forum.sifteam.eu"

S = "${WORKDIR}"

inherit autotools

PACKAGES = "${PN}"

do_install() {
			if [ "${DISTRO_TYPE}" = "experimental" ] ; then
				BUILDTYPE="1"
			else
				BUILDTYPE="0"
			fi

			install -d ${D}/etc
			# generate /etc/image-version
			echo "box_type=${MACHINE}" > ${D}/etc/image-version
			echo "build_type=${BUILDTYPE}" >> ${D}/etc/image-version
			echo "version=${IMAGE_VERSION}" >> ${D}/etc/image-version
			echo "build=${BUILD_VERSION}" >> ${D}/etc/image-version
			echo "date=${DATETIME}" >> ${D}/etc/image-version
			echo "comment=openoam" >> ${D}/etc/image-version
			echo "target=9" >> ${D}/etc/image-version
			echo "creator=OpenOAM" >> ${D}/etc/image-version
			echo "url=${URL}" >> ${D}/etc/image-version
			echo "catalog=${URL}" >> ${D}/etc/image-version
			echo "${MACHINE}" > ${D}/etc/model
}

FILES_${PN} += "/etc"

