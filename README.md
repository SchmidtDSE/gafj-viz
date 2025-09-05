# GAFJ Viz
Visualization of a topic model describing global news articles discussing food.

<br>

## Purpose
Helping inform hybrid quantitative / qualitative research about food justice, this visualization allows for user exploration of a topic model fit on top of a global news media dataset containing translated article metadata for articles discussing food. This software tool which can run in browser or on desktop allows users to look at food topic frequency and co-occurance both globally and regionally.

<br>

## Usage
Recommended usage is through the deployment at [https://food-news-viz.org/](https://food-news-viz.org/).

<br>

## Local environment setup
Install Python before installing required packages with `pip install -r requirements.txt`. Users can then execute either the desktop or web app.

### Desktop app
After installing requirements, simply run `python viz.py`.

### Web app
First prepare the web application with `bash support/load_deps.sh; bash support/prepare_deploy.sh`. Then change into the deploy directory before starting a local web server like `python -m http.server`.

<br>

## Testing
Automated testing is available in two forms: code analysis, unit, and integration tests.

### Code analysis
This project recommends the following standard code analysis tests:

 - Errors: `pyflakes *.py`
 - Style issues: `pycodestyle *.py`
 - Type checks: `mypy *.py`

Note that these are executed during CI / CD.

### Unit tests
The recommended way to run these standard Python unit tests is by installing [nose2](https://docs.nose2.io/en/latest/index.html) and running the `nose2` command.

### Integration tests
A simple integration test is available which outputs the starting view of the visualization to an image file. Simply run `python viz.py static`.

<br>

## Code standards
Please conform to existing standards where possible and, in cases of ambiguity, follow the [Python Google Style Guide](https://google.github.io/styleguide/pyguide.html). For contributions to the project, please ensure all CI / CD operations complete successfully. When possible, please attempt both type and test coverage where the later can be achieved using either unit or integration tests. Please provide docstrings on all public members with optional exception for subclasses who may "inherit" docstrings from their parent.

<br>

## Deployment
The preferred mechanism of deployment is through CI / CD which is automatically executed on merge to `main`. For manual deployment, run `bash support/load_deps.sh; bash support/prepare_deploy.sh` and release the `deploy` directory to static hosting. This hybrid web / desktop application is cloud agnostic. That said, developers may also optionally release lambdas at `article_getter.py` and `article_stat_gen.py`. For more details see `support/prepare_lambdas.sh`. These serverless solutions are used primarily for the express version.

<br>

## License
Code is released under the BSD license while data are released under CC-BY-NC but with additional caveats. See `LICENSE.md` for more details before using data from this project.

<br>

## Open source
This project uses the following open source packages:

 - [IBM Plex](https://github.com/IBM/plex) (Mono and Sans families) under the [OFL 1.0 License](https://github.com/IBM/plex/blob/master/LICENSE.txt).
 - [Cormorant](https://github.com/CatharsisFonts/Cormorant) under the [SIL Open Font License](https://github.com/CatharsisFonts/Cormorant/blob/master/OFL.txt).
 - [Sketchingpy](https://sketchingpy.org/) under the [BSD License](https://codeberg.org/sketchingpy/Sketchingpy/src/branch/main/LICENSE.md) including the packages included in its stand alone hosting archive.
 - [Tabby.js](https://github.com/cferdinandi/tabby) under the [MIT License](https://github.com/cferdinandi/tabby/blob/master/LICENSE.md).

The "express" version also uses:

 - [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) under the [Apache v2 License](https://github.com/boto/boto3/blob/develop/LICENSE).
 - [D3.js](https://d3js.org/) under the [ISC License](https://github.com/d3/d3/blob/main/LICENSE).

Thanks also to:

 - [Color Brewer](https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3) under the [Apache v2 License](https://github.com/axismaps/colorbrewer/).
 - [Google Country Centerpoints](https://developers.google.com/public-data/docs/canonical/countries_csv) under the [CC-BY-4.0 License](https://creativecommons.org/licenses/by/4.0/).
 - [Natural Earth](https://www.naturalearthdata.com/) under the public domain.
