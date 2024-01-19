[ -e deploy ] && rm -r lambda_deploy
mkdir lambda_deploy
cd lambda_deploy

mkdir exporter
cd exporter
cp ../../article_getter.py article_getter.py
mv article_getter.py lambda_function.py
zip exporter.zip lambda_function.py
cd ..

mkdir statgen
cd statgen
cp ../../article_getter.py article_getter.py
cp ../../article_stat_gen.py article_stat_gen.py
mv article_stat_gen.py lambda_function.py
zip statgen.zip article_getter.py lambda_function.py
