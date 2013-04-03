DESCRIPTION = "OpenOAM Image"
SECTION = "base"
PRIORITY = "required"
LICENSE = "proprietary"
MAINTAINER = "OAM team"

require conf/license/license-gplv2.inc

PV = "${IMAGE_VERSION}"
PR = "r${DATETIME}"
PACKAGE_ARCH = "${MACHINE_ARCH}"

IMAGE_INSTALL = "openoam-base"

export IMAGE_BASENAME = "openoam-image"
IMAGE_LINGUAS = ""

IMAGE_FEATURES += "package-management"

inherit image
