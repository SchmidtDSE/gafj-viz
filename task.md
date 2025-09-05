Hello! We have a few issues to address.

# Style guide

We need to make a style.md file which describes new colors to use to match the report at https://story.futureoffood.org/rooted-in-justice/index.html. This involves requiring that the text on buttons is always white, that the background is rgb(248, 236, 212) though it may change to be a little darker on hover or active, that highlight colors (like those with `.highlight`) use rgb(234, 237, 252) as background. This highlight can also be used for header colors. Let's aso specify that we want to use IBM Plex Mono (already in use) for interactive elements. However, we want to use IBM Plex Sans for body text. Finally, we want to use Cormorant for header text. We should get IBM Plex Sans from https://github.com/IBM/plex. We should get Cormorant from https://github.com/CatharsisFonts/Cormorant. We should web search to determine how best to include following the pattern already set in this repo for IBM Plex Mono.

# Apply style to HTML and CSS

Part but not all of the application runs through HTML and CSS. We should apply the new style guide in style.md to the HTML and CSS elements with index.html as the entrypoint. We should be careful that there is an issue with the current implementation where text on buttons (in HTML) are not visibile until one hovers. This needs to be fixed.

# Apply style to Python sketch

The other parts of the application run through Sketchingpy and Python. Please see const.py. Please apply the style.md to this part of the application (including changing the background color and fonts to match). Please review the Python code to see what styles are used if any outside const.py.

# Fix web execution

In running the web version of this application, we get the following:

```
Traceback (most recent call last):
  File "/lib/python311.zip/_pyodide/_base.py", line 499, in eval_code
    .run(globals, locals)
     ^^^^^^^^^^^^^^^^^^^^
  File "/lib/python311.zip/_pyodide/_base.py", line 340, in run
    coroutine = eval(self.code, globals, locals)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<exec>", line 495, in <module>
  File "<exec>", line 491, in main
  File "<exec>", line 133, in show
  File "/lib/python3.11/site-packages/sketchingpy/sketch2dweb.py", line 491, in show
    self._show_internal(ax=ax, quit_immediately=False)
  File "/lib/python3.11/site-packages/sketchingpy/sketch2dweb.py", line 529, in _show_internal
    self._inner_loop()
  File "/lib/python3.11/site-packages/sketchingpy/sketch2dweb.py", line 541, in _inner_loop
    self._callback_step(self)
  File "<exec>", line 118, in <lambda>
  File "<exec>", line 158, in _draw
  File "/home/pyodide/overview_viz.py", line 138, in draw
    self._map_component.draw()
  File "/home/pyodide/map_viz.py", line 134, in draw
    self._sketch.draw_buffer(0, 0, 'basemap')
  File "/lib/python3.11/site-packages/sketchingpy/sketch2dweb.py", line 285, in draw_buffer
    web_buffer = self._buffers[name]
                 ~~~~~~~~~~~~~^^^^^^
KeyError: 0
```

We should check https://sketchingpy.org/reference.html for details. We may have an issue where the web deployment (see github actions) is not using the right version. We should update to the latest version of sketchingpy. See github actions.

# Fix express

We have an "express" version for accessibility. However, a recent issue seems to have broken it. See below.

```
Uncaught TypeError: Cannot read properties of null (reading 'style')
    at setupExpress (express.js?v=0.1.4:140:47)
    at express.js?v=0.1.4:155:1
```

Please investigate.

# Update tutorial

The tutorial video is too small. Let's make it bigger. Let's also please mention in the page "Some example articles are listed with URLs. These are provided as examples solely for the purpose of academic research. Rights retained by their authors."

# Update open source listing

Under "Open source" in our README, please add the new font.
