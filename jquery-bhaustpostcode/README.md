# jQuery plugin: bhAustPostcode

A jQuery plugin which enables searching for Australian postcodes based on locality aka suburb.

The back-end that this plugin uses is the web API written in Python, its repo is 
[https://github.com/behai-nguyen/bh-aust-postcode](https://github.com/behai-nguyen/bh-aust-postcode/).

Detail description of the web API can be found in this post:
[Python: A simple web API to search for Australian postcodes based on locality aka suburb](https://behainguyen.wordpress.com/2023/05/18/python-a-simple-web-api-to-search-for-australian-postcodes-based-on-locality-aka-suburb/).

This following post discusses hosting this web API: [Ubuntu 22.10: hosting a Python Flask web API with Gunicorn and Nginx]( https://behainguyen.wordpress.com/2023/05/25/ubuntu-22-10-hosting-a-python-flask-web-api-with-gunicorn-and-nginx/ ).

## Third Party Libraries

1. [ jQuery v3.6.0 ](https://blog.jquery.com/2021/03/02/jquery-3-6-0-released/)

2. [ Bootstrap v5.1.3 ](https://getbootstrap.com/docs/5.1/getting-started/introduction/)

3. [ Bootstrap Icons v1.9.1 ](https://blog.getbootstrap.com/2022/07/13/bootstrap-icons-1-9-0/) -- 
underneath the directory where the CSS is, we need to have <code>fonts/bootstrap-icons.woff</code>
and <code>fonts/bootstrap-icons.woff2</code>.

## bhAustPostcode In Brief

There can be multiple instances of <code>bhAustPostcode</code> within a single page.

### Options

The inline comments in the source code should be sufficient to explain all the options. 
This section reiterates the important ones.

1. <code>url</code> -- this is the URL of the above mentioned web API in your own environment.
You should have successfully run this web API before attempting to run this plugin.

2. <code>localityName</code> and <code>localityId</code> -- values of the HTML 
<code>name</code> and <code>id</code> attributes of the locality text input.

3. <code>stateName</code> and <code>stateId</code> -- values of the HTML 
<code>name</code> and <code>id</code> attributes of the state text input.

4. <code>postcodeName</code> and <code>postcodeId</code> -- values of the HTML 
<code>name</code> and <code>id</code> attributes of the postcode text input.

### Creation Of The Locality, State and Postcode Fields

<code>bhAustPostcode</code> creates <code>locality</code>, <code>state</code> 
and <code>postcode</code> text fields as a Bootstrap [ input group ]( https://getbootstrap.com/docs/5.0/forms/input-group/ ). The default size is small, i.e. <code>input-group-sm</code>, it can be overwritten 
via option <code>bootstrapInputGroupSize</code>.

<code>bhAustPostcode</code>'s element is the container for this group, ensure there is sufficient
horizontal space for the three fields.

## Usage

Briefly:

```
	    <div class="row g-3 align-items-center mb-2">
		    <div class="col-1">Suburb</div>
			<div class="col" id="austPostcode"></div>
		</div>
```

```
    <script>
		$( document ).ready( function() {

			$( '#austPostcode' ).bhAustPostcode({
				localityName: 'suburb',
				localityId: 'suburb',
				stateName: 'state',
				stateId: 'state',
				postcodeName: 'postcode',
				postcodeId: 'postcode'
			});
        });

    </script>
```

See the plugin <code>example/</code> directory for complete working example HTML pages.

## My Development Environment

This section helps making the later section(s) easier to follow. I am using Windows 10 Pro as the primary development environment. My main <code>JavaScript</code> development area is:

-- <code>D:\Codes\WebWork</code>.

The IIS Virtual Directory pointing to the above directory is:

-- <code>http://localhost/work/</code>.

## CSS and JavaScript Inclusions In the <code>example/</code> Directory

Relative to the <code>D:\Codes\WebWork</code> directory mentioned above, within my development
environment this plugin uses:

1. <code>D:\Codes\WebWork\js</code> -- common generic <code>JavaScript</code> routines, which have
been checked in at [ https://github.com/behai-nguyen/js ](https://github.com/behai-nguyen/js). These files are 
small. Some have only a single function in them. The idea is, each project should minify and combine 
relevant files to only a single <code>minified JavaScript</code> file.

2. <code>D:\Codes\WebWork\jquery\js</code> -- [ jQuery v3.6.0 ](https://blog.jquery.com/2021/03/02/jquery-3-6-0-released/).

3. <code>D:\Codes\WebWork\bootstrap\dist\js</code> -- [ Bootstrap v5.1.3 ](https://getbootstrap.com/docs/5.1/getting-started/introduction/) <code>JavaScript</code>.

4. <code>D:\Codes\WebWork\bootstrap\dist\css</code> --  [ Bootstrap v5.1.3 ](https://getbootstrap.com/docs/5.1/getting-started/introduction/) <code>CSS</code>.

5. <code>D:\Codes\WebWork\bootstrap\icons-1.9.1\font</code> -- [ Bootstrap Icons v1.9.1 ](https://blog.getbootstrap.com/2022/07/13/bootstrap-icons-1-9-0/) <code>CSS</code>.

6. <code>D:\Codes\WebWork\jquery-bhaustpostcode\src</code> -- this plugin own <code>JavaScript</code> 
and <code>CSS</code>.

All examples in the plugin <code>example/</code> directory have the following inclusions:

```
    <!-- JQuery -->
    <script src="http://localhost/work/jquery/js/jquery-3.6.0.js"></script>

    <!-- Bootstrap 5.0 core. -->
	<link href="http://localhost/work/bootstrap/dist/css/bootstrap.css" rel="stylesheet">
	<script src="http://localhost/work/bootstrap/dist/js/bootstrap.bundle.js"></script>

	<!-- Bootstrap Font Icon CSS -->
	<link href="http://localhost/work/bootstrap/icons-1.9.1/font/bootstrap-icons.css" rel="stylesheet">

	<script src="http://localhost/work/js/delay_callback_func.js"></script>
	<script src="http://localhost/work/js/css_funcs.js"></script>
	<script src="http://localhost/work/js/content_types.js"></script>
	<script src="http://localhost/work/js/http_status.js"></script>
	<script src="http://localhost/work/js/ajax_funcs.js"></script>
	<script src="http://localhost/work/js/elem_height_funcs.js"></script>
	<script src="http://localhost/work/js/bootstrap_funcs.js"></script>
    <script src="http://localhost/work/js/drags.js"></script>
    <script src="http://localhost/work/js/bootstrap_dialogs.js"></script>

    <!-- jQuery plugin bhAustPostcode's CSS and JS. --->
	<link href="http://localhost/work/jquery-bhaustpostcode/src/bhAustPostcode.css" rel="stylesheet">
    <script src="http://localhost/work/jquery-bhaustpostcode/src/bhAustPostcode.js"></script>
```

This plugin will be used as part of my other projects, whereby I minify and combine all required 
<code>CSS</code> files, including third party's one into a single minified file. The same process
for <code>JavaScript</code> files. 

That means, each of my project has to include only a single minified <code>CSS</code> file, and
a single minified <code>JavaScript</code> file in production.

## CSS, JavaScript Minifying and Combining: <code>minify/css-minify.bat</code> and <code>minify/js-minify.bat</code>

<code>minify/css-minify.bat</code> and <code>minify/js-minify.bat</code> prepare the final
single minified <code>CSS</code> file and <code>JavaScript</code> file for this plugin. 

The above inclusions can be be rewritten to:

```
	<link href="URL of bh-aust-postcode.min.css or whatever.min.css" rel="stylesheet">
    <script src="URL of bh-aust-postcode.min.js or whatever.min.js"></script>
```

I've discussed the minification method I use in this post -- [JavaScript and CSS minification]( https://behainguyen.wordpress.com/2022/11/06/javascript-and-css-minification/ ).

## Theming

This plugin has two built-in themes: <code>safe</code> and <code>eyesore</code>. 
<code>safe</code> is basically the default colours provided by Bootstrap CSS. 
<code>eyesore</code> is my own colour scheme. I am horrible with colours, I name it so
for attention catching.

Users can define their colour scheme as seen in <code>example/example03.html</code>.

## Others

Copyright (c) 2023, Be Hai Nguyen.

This project is dual licensed under the
[ MIT license ](http://www.opensource.org/licenses/mit-license.php)
and the [ GPL license](http://www.gnu.org/licenses/gpl.html).
