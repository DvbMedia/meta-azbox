DESCRIPTION = "Azbox Specific plugin"
RDEPENDS = "enigma2"
DEPENDS = "python-native"
PACKAGE_ARCH = "${MACHINE_ARCH}"
LICENSE="CLOSED"

SRCREV = "e2cee01d2a6829fe95687a9a130a712581fbb8d6"
inherit gitpkgv

PR = "r5"


SRC_URI = "git://azboxopenpli.git.sourceforge.net/gitroot/azboxopenpli/RtiSYS;protocol=git;tag=${SRCREV} \
	  file://VideoSettingsSetup \
	 "

S = "${WORKDIR}"

do_install() {
	install -d  ${D}/usr/lib/enigma2/python/Plugins/SystemPlugins/RtiSYS
	
	install -m 0644 ${S}/git/*.py \
	${D}/usr/lib/enigma2/python/Plugins/SystemPlugins/RtiSYS

	install -m 0755 ${S}/git/ntpdate \
	${D}/usr/lib/enigma2/python/Plugins/SystemPlugins/RtiSYS


	
	install -d  ${D}/usr/lib/enigma2/python/Plugins/SystemPlugins/VideoSettingsSetup

	install -m 0644 ${S}/VideoSettingsSetup/*.pyo \
	${D}/usr/lib/enigma2/python/Plugins/SystemPlugins/VideoSettingsSetup

	
}

FILES_enigma2-plugin-systemplugins-rtisys = "/usr/lib/enigma2/python/Plugins/SystemPlugins/RtiSYS"
FILES_enigma2-plugin-systemplugins-videosettingssetup = "/usr/lib/enigma2/python/Plugins/SystemPlugins/VideoSettingsSetup"

PACKAGES = "\
	enigma2-plugin-systemplugins-rtisys \	
	enigma2-plugin-systemplugins-videosettingssetup \
	"

PROVIDES="${PACKAGES}"
