DESCRIPTION = "Linux kernel for ${MACHINE}"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${WORKDIR}/linux-${KV}/COPYING;md5=d7810fab7487fb0aad327b76f1be7cd7"
MACHINE_KERNEL_PR_append = ".7"

KV = "3.3.1"

SRC_URI += "http://azbox-enigma2-project.googlecode.com/files/linux-azbox-${KV}-new-2.tar.bz2 \
	   file://${MACHINE}_defconfig \
	   file://genzbf.c \
	   file://sigblock.h \
	   file://zboot.h \
	   file://emhwlib_registers_tango2.h \	   
	   "

SRC_URI_append_azboxme = "http://azbox-enigma2-project.googlecode.com/files/initramfs-${MACHINE}-14022013.tar.bz2;name=azbox-initrd-${MACHINE}"

SRC_URI_append_azboxminime = "http://azbox-enigma2-project.googlecode.com/files/initramfs-${MACHINE}-14022013.tar.bz2;name=azbox-initrd-${MACHINE}"

SRC_URI_append_azboxhd = "http://azbox-enigma2-project.googlecode.com/files/initramfs-${MACHINE}-14022013.tar.bz2;name=azbox-initrd-${MACHINE}"

SRC_URI[azbox-initrd-azboxhd.md5sum] = "4ca0977c0b89f922abaf4e384198b530"
SRC_URI[azbox-initrd-azboxhd.sha256sum] = "91d9bae6dc79370822c90b298fcae6f8c0840da1b8b9384d81a50edecce335c1"
SRC_URI[azbox-initrd-azboxme.md5sum] = "8843278aa530d9da8a125e86e2b56b8d"
SRC_URI[azbox-initrd-azboxme.sha256sum] = "242ed6efc25d8961d1d9e63378d336851b7e7b89e2f28ae399aa900351aba3d2"
SRC_URI[azbox-initrd-azboxminime.md5sum] = "b165af7a8355f4c0d42f758b2d898512"
SRC_URI[azbox-initrd-azboxminime.sha256sum] = "947a232eb266ae6d5a7e6ad6a8aa4cacebc1e10800d3652dae8e530e69d185bb"

S = "${WORKDIR}/linux-${KV}"

inherit kernel

export OS = "Linux"
KERNEL_OBJECT_SUFFIX = "ko"
KERNEL_OUTPUT = "zbimage-linux-xload"
KERNEL_IMAGETYPE = "zbimage-linux-xload"
KERNEL_IMAGEDEST = "/tmp"


FILES_kernel-image = "/boot/zbimage-linux-xload"

CFLAGS_prepend = "-I${WORKDIR} "

do_configure_prepend() {
	oe_machinstall -m 0644 ${WORKDIR}/${MACHINE}_defconfig ${S}/.config
	oe_runmake oldconfig
}

kernel_do_compile() {
	gcc ${CFLAGS} ${WORKDIR}/genzbf.c -o ${WORKDIR}/genzbf
	
	install -m 0755 ${WORKDIR}/genzbf ${S}/arch/mips/boot/

	unset CFLAGS CPPFLAGS CXXFLAGS LDFLAGS MACHINE
	oe_runmake include/linux/version.h CC="${KERNEL_CC}" LD="${KERNEL_LD}"
	oe_runmake ${KERNEL_IMAGETYPE} CC="${KERNEL_CC}" LD="${KERNEL_LD}" AR="${AR}" OBJDUMP="${OBJDUMP}" NM="${NM}"
	oe_runmake modules CC="${KERNEL_CC}" LD="${KERNEL_LD}" AR="${AR}" OBJDUMP="${OBJDUMP}"
}

do_install_append () {
	install -d ${D}/boot
	install -m 0644 ${S}/arch/mips/boot/zbimage-linux-xload ${D}/boot/zbimage-linux-xload

}
