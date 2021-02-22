var gulp = require('gulp');
var exec = require('child_process').exec;
var sass = require('gulp-sass');
sass.compiler = require('sass');

var SASS_DIR = 'website/static/website/css/*.scss'
var CSS_DIR = 'website/static/website/css/'
var JS_DIR = 'website/static/website/js/'
var JS_MATCH = JS_DIR + '*.js'
var PARTICLES_DIR = 'node_modules/particles.js/'

gulp.task('sass', function() {
	return gulp.src(SASS_DIR)
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest(CSS_DIR));
})

gulp.task('sass:watch', function() { 
	gulp.watch(SASS_DIR, gulp.series('sass'));
});

gulp.task('collectstatic', function(cb) {
	exec('echo "Updating Django..."');
	exec('echo "Updating Django..." && python manage.py collectstatic --noinput && echo "...Done"', function (err, stdout, stderr) {
			console.log(stdout);
			console.log(stderr);
			cb(err);
		});
	exec('echo "Done"');
})

gulp.task('django', function() {
	gulp.watch(SASS_DIR, gulp.series('sass', 'collectstatic'));
	gulp.watch(JS_MATCH, gulp.series('collectstatic'));
})

gulp.task('deploy', function() {
	gulp.series('sass','collectstatic');
})
