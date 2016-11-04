# split_image

split_image is a small tool to chop up large files into smaller chunks for easier processing.
 
## How to use it
A typical command line run looks like this:

```
split_image.py large_file.fits 3 5 100
```

This command would take the image from `large_file.fits` and chop it up into a grid of 
smaller images, 3 wide and 5 high, each with an overlap region to its neighbors of 100 pixels.
 The resulting output files are named after the input file using the following convention:
 
```
large_image.xXXyYY.fits
```

where XX is the horizontal position and YY the vertical position in a XX-by-YY array. 
In the above example, you would get the following files:
 
```
large_image_x00y00.fits
large_image_x01y00.fits
large_image_x02y00.fits
large_image_x00y01.fits
large_image_x01y01.fits
large_image_x02y01.fits
large_image_x00y02.fits
large_image_x01y02.fits
large_image_x02y02.fits

```



## Known caveats

At the moment, split_image only handles single-extension FITS images, i.e. the image data needs to be 
  stored in the primary FITS unit.