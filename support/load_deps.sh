[ ! -e third_party_web/IBMPlexMono-Regular.ttf ] && wget --directory-prefix=third_party_web https://github.com/IBM/plex/raw/master/IBM-Plex-Mono/fonts/complete/ttf/IBMPlexMono-Regular.ttf
[ ! -e third_party_web/tabby-ui.min.css ] && wget --directory-prefix=third_party_web https://cdn.jsdelivr.net/gh/cferdinandi/tabby/dist/css/tabby-ui.min.css
[ ! -e third_party_web/tabby.polyfills.min.js ] && wget --directory-prefix=third_party_web https://cdn.jsdelivr.net/gh/cferdinandi/tabby/dist/js/tabby.polyfills.min.js

[ ! -e third_party/self_host.zip ] && wget --directory-prefix=third_party https://sketchingpy.org/dist/self_host.zip
cd third_party
unzip -o self_host.zip
rm self_host.zip
mv self_host/* ./
rm -r self_host
