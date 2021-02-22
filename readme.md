

## Building Locally
Run `npm install` 
You can then run:
* `gulp sass` to build and `gulp sass:watch` to repeatedly rebuild the SASS files on change
* `gulp collectstatic` to update Django's static folder with the new CSS files
* `gulp django` to combine it all together: watch the SASS folder, recompile, and rebuild to Django. Happens almost instantly.