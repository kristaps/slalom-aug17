var browserSync  = require('browser-sync');
var watchify     = require('watchify');
var browserify   = require('browserify');
var source       = require('vinyl-source-stream');
var buffer       = require('vinyl-buffer');
var gulp         = require('gulp');
var gutil        = require('gulp-util');
var gulpSequence = require('gulp-sequence');
var includehtml  = require('gulp-include-html');
var processhtml  = require('gulp-minify-html');
var sass         = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var watch        = require('gulp-watch');
var cleanCSS    = require('gulp-clean-css');
var uglify       = require('gulp-uglify');
var streamify    = require('gulp-streamify');
var sourcemaps   = require('gulp-sourcemaps');
var concat       = require('gulp-concat');
var babel        = require('gulp-babel');
var prod         = gutil.env.prod;

var onError = function(err) {
  console.log(err.message);
  this.emit('end');
};

// bundling js with browserify and watchify
var b = watchify(browserify('./src/js/main', {
  cache: {},
  packageCache: {},
  fullPaths: true
}));

gulp.task('js', bundle);
b.on('update', bundle);
b.on('log', gutil.log);


gulp.task('other-js', function() {
	return gulp.src('./src/other-js/**')
		.pipe(gulp.dest('build/other-js'))
	    .pipe(browserSync.stream());
});

gulp.task('lib', function() {
	return gulp.src('./src/lib/**')
		.pipe(gulp.dest('build/lib'));
});


function bundle() {
  return b.bundle()
    .on('error', onError)
    .pipe(source('bundle.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init())
    .pipe(prod ? babel({
      presets: ['es2015']
    }) : gutil.noop())
    .pipe(concat('bundle.js'))
    // .pipe(!prod ? sourcemaps.write('.') : gutil.noop())
    // .pipe(prod ? streamify(uglify()) : gutil.noop())
    .pipe(gulp.dest('./build/js'))
    .pipe(browserSync.stream());
}

// html
gulp.task('html', function() {
  return gulp.src('./src/templates/**/*')
    .pipe(includehtml())
    .pipe(processhtml())
    .pipe(gulp.dest('build'))
    .pipe(browserSync.stream());
});

// sass
gulp.task('sass', function() {
  return gulp.src('./src/scss/**/*.scss')
    .pipe(sass({
      includePaths: [].concat(['node_modules/foundation-sites/scss'])
    }))
    .on('error', onError)
    .pipe(prod ? cleanCSS() : gutil.noop())
    .pipe(prod ? autoprefixer({
      browsers: ['last 2 versions'],
      cascade: false
    }) : gutil.noop())
    .pipe(gulp.dest('./build/stylesheets'))
    .pipe(browserSync.stream());
});

gulp.task('assets', function() {
	return gulp.src('./src/assets/**/*.{gif,jpg,png,svg}')
		.pipe(gulp.dest('build/assets'));
});

// browser sync server for live reload
gulp.task('serve', function() {
  browserSync.init({
    server: {
      baseDir: './build'
    }
  });

  gulp.watch('./src/assets/**/*', ['assets']);
  gulp.watch('./src/js/**/*', ['js']);
  gulp.watch('./src/other-js/**/*', ['other-js']);
  gulp.watch('./src/templates/**/*', ['html']);
  gulp.watch('./src/scss/**/*.scss', ['sass']);
});

// use gulp-sequence to finish building html, sass and js before first page load
gulp.task('default', gulpSequence(['html', 'sass', 'js', 'other-js', 'lib', 'assets'], 'serve'));

