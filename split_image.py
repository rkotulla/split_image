#!/usr/bin/env python

import os
import sys
import astropy.io.fits as fits
import itertools
import math
import numpy

if __name__ == "__main__":


    fn = sys.argv[1]
    if (not os.path.isfile(fn)):
        print("Could not find input file %s" % (fn))
        sys.exit(0)

    nx = int(sys.argv[2])
    ny = int(sys.argv[3])
    overlap = int(sys.argv[4])

    print("Loading input frame %s" % (fn))
    hdulist = fits.open(fn)
    img = hdulist[0].data
    header = hdulist[0].header

    sx = img.shape[1]/nx
    sy = img.shape[0]/ny


    for x,y in itertools.product(range(nx), range(ny)):

        out_fn = "%s.x%02dy%02d.fits" % (fn[:-5], x, y)

        start_x = numpy.max([int(math.floor(x * sx - overlap)), 0])
        end_x = numpy.min([int(math.ceil((x+1)*sx + overlap)), img.shape[1]])

        start_y = numpy.max([int(math.floor(y * sy - overlap)), 0])
        end_y = numpy.min([int(math.ceil((y+1)*sy + overlap)), img.shape[0]])

        print("Creating cutout x=%02d, y=%02d (x: %5d--%5d, y: %5d--%5d) --> %s" % (
            x,y,start_x, end_x, start_y, end_y, out_fn)
              )
        cutout = img[start_y:end_y, start_x:end_x]

        phdu = fits.PrimaryHDU(data=cutout, header=header)
        phdu.header['CRPIX1'] -= start_x
        phdu.header['CRPIX2'] -= start_y

        # print("Writing cutout to %s" % (out_fn))
        phdu.writeto(out_fn, clobber=True)

