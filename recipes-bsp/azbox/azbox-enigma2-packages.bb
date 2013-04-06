DESCRIPTION = "Azbox Specific plugin"
RDEPENDS = "enigma2"
DEPENDS = "python-native"
PACKAGE_ARCH = "${MACHINE_ARCH}"
LICENSE="CLOSED"

SRCREV = "dcdb5056b4e43feccf7d750d70e32b4e9a6dee9c"
inherit gitpkgv pkgconfig

PR = "r10"


SRC_URI = "git://azboxopenpli.git.sourceforge.net/gitroot/azboxopenpli/RtiSYS;protocol=git;tag=${SRCREV} \
	  file://VideoSettingsSetup \
	 "

S = "${WORKDIR}"

do_compile() {
	python -O -m compileall ${S}
}

python populate_packages_prepend () {
	enigma2_plugindir = bb.data.expand('${libdir}/enigma2/python/Plugins', d)

	do_split_packages(d, enigma2_plugindir, '^(\w+/\w+)/[a-zA-Z0-9_]+.*$', 'enigma2-plugin-%s', 'Enigma2 Plugin: %s', recursive=True, match_path=True, prepend=True)
	do_split_packages(d, enigma2_plugindir, '^(\w+/\w+)/.*\.py$', 'enigma2-plugin-%s-src', 'Enigma2 Plugin: %s', recursive=True, match_path=True, prepend=True)
	do_split_packages(d, enigma2_plugindir, '^(\w+/\w+)/(.*/)?\.debug/.*$', 'enigma2-plugin-%s-dbg', 'Enigma2 Plugin: %s', recursive=True, match_path=True, prepend=True)
}

do_install() {
	install -d  ${D}/usr/lib/enigma2/python/Plugins/SystemPlugins/RtiSYS
	
	install -m 0644 ${S}/git/*.pyo \
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
