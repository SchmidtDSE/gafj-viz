[ -e deploy ] && rm -r deploy
mkdir deploy
cp *.py deploy
cp *.html deploy
cp -r css deploy/css
cp -r csv deploy/csv
cp -r geojson deploy/geojson
cp -r js deploy/js
cp -r third_party deploy/third_party
cp -r third_party_web deploy/third_party_web
cp -r txt deploy/txt
cd deploy

for name in *.py; do
    mv -- "$name" "${name%.py}.pyscript"
done
