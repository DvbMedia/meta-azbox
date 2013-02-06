DESCRIPTION = "Linux kernel for ${MACHINE}"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${WORKDIR}/linux-${KV}/COPYING;md5=d7810fab7487fb0aad327b76f1be7cd7"
MACHINE_KERNEL_PR_append = ".6"

KV = "3.3.1"

SRC_URI += "http://azbox-enigma2-project.googlecode.com/files/linux-azbox-${KV}-new-2.tar.bz2 \
	   file://${MACHINE}_defconfig \
	   file://genzbf.c \
	   file://sigblock.h \
	   file://zboot.h \
	   file://emhwlib_registers_tango2.h \	   
	   "

SRC_URI_append_azboxme = "http://azbox-enigma2-project.googlecode.com/files/initramfs-${MACHINE}-08012013.tar.bz2;name=azbox-initrd-${MACHINE}"

SRC_URI_append_azboxminime = "http://azbox-enigma2-project.googlecode.com/files/initramfs-${MACHINE}-08012013.tar.bz2;name=azbox-initrd-${MACHINE}"

SRC_URI_append_azboxhd = "http://azbox-enigma2-project.googlecode.com/files/initramfs-${MACHINE}-08012013.tar.bz2;name=azbox-initrd-${MACHINE}"

SRC_URI[azbox-initrd-azboxhd.md5sum] = "0490b6920635ef7097cc06483e657a9d"
SRC_URI[azbox-initrd-azboxhd.sha256sum] = "1c344c644f5a93d71f4c87bc4d4543574826700c2c71cb653b7f7b4378a708a2"
SRC_URI[azbox-initrd-azboxme.md5sum] = "6e11118d1061b8d7e55b4bd0f31499c5"
SRC_URI[azbox-initrd-azboxme.sha256sum] = "b706db300f0ea72060ffcb2e15093361072c430fb2089892abc6d051088e1055"

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
