[ -e static.png ] &&  rm static.png
python3 viz.py static
[ ! -e static.png ] && exit 1
rm static.png
echo "Passed"