[ ! -e third_party_web/IBMPlexMono-Regular.ttf ] && {
    wget -O /tmp/plex.zip https://github.com/IBM/plex/releases/download/v6.4.0/TrueType.zip
    cd /tmp && unzip -q plex.zip
    cp TrueType/IBM-Plex-Mono/IBMPlexMono-Regular.ttf "$OLDPWD/third_party_web/"
    cd "$OLDPWD"
    rm -rf /tmp/plex.zip /tmp/TrueType
}

[ ! -e third_party_web/IBMPlexSans-Regular.ttf ] && {
    wget -O /tmp/plex.zip https://github.com/IBM/plex/releases/download/v6.4.0/TrueType.zip
    cd /tmp && unzip -q plex.zip
    cp TrueType/IBM-Plex-Sans/IBMPlexSans-Regular.ttf "$OLDPWD/third_party_web/"
    cp TrueType/IBM-Plex-Sans/IBMPlexSans-Bold.ttf "$OLDPWD/third_party_web/"
    cd "$OLDPWD"
    rm -rf /tmp/plex.zip /tmp/TrueType
}

[ ! -e third_party_web/Cormorant-Regular.ttf ] && {
    wget -O /tmp/cormorant.zip https://github.com/CatharsisFonts/Cormorant/releases/download/v3.609/Cormorant-3.609.zip
    cd /tmp && unzip -q cormorant.zip
    cp "Cormorant-3.609/2. OpenType Files/Cormorant-Regular.otf" "$OLDPWD/third_party_web/Cormorant-Regular.otf"
    cp "Cormorant-3.609/2. OpenType Files/Cormorant-Bold.otf" "$OLDPWD/third_party_web/Cormorant-Bold.otf"
    cd "$OLDPWD"
    rm -rf /tmp/cormorant.zip /tmp/Cormorant-3.609
}
[ ! -e third_party_web/tabby-ui.min.css ] && wget --directory-prefix=third_party_web https://cdn.jsdelivr.net/gh/cferdinandi/tabby/dist/css/tabby-ui.min.css
[ ! -e third_party_web/tabby.polyfills.min.js ] && wget --directory-prefix=third_party_web https://cdn.jsdelivr.net/gh/cferdinandi/tabby/dist/js/tabby.polyfills.min.js
[ ! -e third_party_web/d3.min.js ] && wget --directory-prefix=third_party_web https://cdn.jsdelivr.net/npm/d3@7
mv third_party_web/d3@7 third_party_web/d3.min.js

[ ! -e third_party/self_host.zip ] && wget --directory-prefix=third_party https://sketchingpy.org/dist/self_host.zip
cd third_party
unzip -o self_host.zip
rm self_host.zip
mv self_host/* ./
rm -r self_host
