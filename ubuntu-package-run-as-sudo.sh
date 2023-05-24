#!/bin/bash

pkgname="lol-for-linux-installer"
pkgver="2.2"
pkgrel="1"
pkgdesc="League of Legends installer and manager for Linux"
arch="amd64"
url="https://github.com/kassindornelles/lol-for-linux-installer"
license="GPL-3.0"
depends=("python3" "python3-psutil" "python3-pyqt5" "wine" "python3-requests" "python3-pyqt5.qtwebkit" "tar" "libgnutls30" "libgnutls30:i386" "libldap-2.4-2" "libldap-2.4-2:i386" "libpng16-16" "libpng16-16:i386" "libgl1-mesa-glx" "libgl1-mesa-glx:i386" "gphoto2" "libpulse0" "libpulse0:i386")
source="https://github.com/kassindornelles/lol-for-linux-installer/archive/refs/tags/v.${pkgver}.tar.gz"
sha512sums="01f9fbd1f61d132432ebe457e257bae7664b8f4caa3334a1dda29c86e5ae9a40704a6822eaa3a3f7fadf536ea12ca9b9aeccd5b1cab99144cba9b675092286ea"

# Function to download and extract the source archive
download_and_extract() {
    echo "Downloading source archive..."
    curl -L -O "${source}"
    echo "Extracting source archive..."
    tar -xf "v.${pkgver}.tar.gz"
    rm "v.${pkgver}.tar.gz"
}

# Function to build the package
build_package() {
    echo "Building package..."
    cd "lol-for-linux-installer-v.${pkgver}/src"
    install -Dm755 lol-for-linux-installer.py "${pkgdir}/usr/bin/lol-for-linux-installer"
    install -Dm644 env_vars.json "${pkgdir}/usr/share/lol-for-linux-installer/env_vars.json"
    install -Dm644 lol-for-linux-installer.png "${pkgdir}/usr/share/lol-for-linux-installer/lol-for-linux-installer.png"
    install -Dm644 leagueinstaller_code.py "${pkgdir}/usr/share/lol-for-linux-installer/leagueinstaller_code.py"
    install -Dm644 lol-for-linux-installer.desktop "${pkgdir}/usr/share/applications/lol-for-linux-installer.desktop"
    cp -R python_src "${pkgdir}/usr/share/lol-for-linux-installer/"
}

# Function to create the .deb package
create_deb_package() {
    echo "Creating .deb package..."
    mkdir -p "${pkgname}-${pkgver}-${pkgrel}/DEBIAN"
    touch "${pkgname}-${pkgver}-${pkgrel}/DEBIAN/control"
    echo "Package: ${pkgname}" >> "${pkgname}-${pkgver}-${pkgrel}/DEBIAN/control"
    echo "Version: ${pkgver}-${pkgrel}" >> "${pkgname}-${pkgver}-${pkgrel}/DEBIAN/control"
    echo "Architecture: ${arch}" >> "${pkgname}-${pkgver}-${pkgrel}/DEBIAN/control"
    echo "Maintainer: Kassin Dornelles <kassin.dornelles@gmail.com>" >> "${pkgname}-${pkgver}-${pkgrel}/DEBIAN/control"
    echo "Description: ${pkgdesc}" >> "${pkgname}-${pkgver}-${pkgrel}/DEBIAN/control"
    echo "Homepage: ${url}" >> "${pkgname}-${pkgver}-${pkgrel}/DEBIAN/control"
    dpkg-deb --build "${pkgname}-${pkgver}-${pkgrel}"
    mv "${pkgname}-${pkgver}-${pkgrel}.deb" "$(dirname "$0")/${pkgname}-${pkgver}-${pkgrel}.deb"
    echo "Package built successfully: ${pkgname}-${pkgver}-${pkgrel}.deb"

    # Remove the source folder
    cd "$(dirname "$0")"
    rm -rf "lol-for-linux-installer-v.${pkgver}"
}

# Main function
main() {
    download_and_extract
    build_package
    create_deb_package
}

main