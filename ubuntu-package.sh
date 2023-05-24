#!/bin/bash

pkgname=lol-for-linux-installer
pkgver=2.2
pkgrel=1
pkgdesc="League of Legends installer and manager for Linux"
maintainer="Kassin Dornelles <kassin.dornelles@gmail.com>"
url="https://github.com/kassindornelles/lol-for-linux-installer"
license="GPL-3.0"
arch="amd64"

dependencies=$(dpkg-query -W -f='${Depends}' python3 python3-psutil python3-pyqt5 wine64 python3-requests qt5-default libgnutls30 libldap-2.4-2 libpng16-16 libgphoto2-6 libpulse0 libqt5gui5 | sed 's/,/ /g')

pkgdir="$pkgname-$pkgver"
mkdir -p "$pkgdir/DEBIAN"
mkdir -p "$pkgdir/usr/bin"
mkdir -p "$pkgdir/usr/share/lol-for-linux-installer"
mkdir -p "$pkgdir/usr/share/applications"

cp src/lol-for-linux-installer.py "$pkgdir/usr/bin/lol-for-linux-installer"
cp src/env_vars.json "$pkgdir/usr/share/lol-for-linux-installer/env_vars.json"
cp src/lol-for-linux-installer.png "$pkgdir/usr/share/lol-for-linux-installer/lol-for-linux-installer.png"
cp src/leagueinstaller_code.py "$pkgdir/usr/share/lol-for-linux-installer/leagueinstaller_code.py"
cp src/lol-for-linux-installer.desktop "$pkgdir/usr/share/applications/lol-for-linux-installer.desktop"
cp -R src/python_src "$pkgdir/usr/share/lol-for-linux-installer/"

# Create control file
cat > "$pkgdir/DEBIAN/control" << EOL
Package: $pkgname
Version: $pkgver-$pkgrel
Architecture: $arch
Maintainer: $maintainer
Description: $pkgdesc
Homepage: $url
License: $license
Depends: $dependencies
EOL

chmod 755 "$pkgdir/usr/bin/lol-for-linux-installer"

dpkg-deb --build "$pkgdir"

echo "Package built successfully: $pkgdir.deb"
