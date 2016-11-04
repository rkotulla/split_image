#!/usr/bin/env python

import os
import sys
import astropy.io.fits as fits
import astropy.io.votable as vot
import astropy.wcs as WCS

#import astropy.nddata.utils as astro_utils
import itertools
import math
import numpy


def cutout_region(imghdu, ra, dec, size, output_fn):

    wcs = WCS.WCS(imghdu.header)

    xy = wcs.all_world2pix(ra, dec, 1)
    pixelscale = WCS.utils.proj_plane_pixel_scales(wcs)[0] * 3600.

    npixels = size / pixelscale

    x1 = numpy.max([0, int(math.floor(xy[0] - npixels))])
    x2 = numpy.min([imghdu.data.shape[1], int(math.ceil(xy[0] + npixels))])
    y1 = numpy.max([0, int(math.floor(xy[1] - npixels))])
    y2 = numpy.min([imghdu.data.shape[0], int(math.ceil(xy[1] + npixels))])

    cutout = imghdu.data[y1:y2, x1:x2]

    out_hdu = fits.PrimaryHDU(data=cutout, header=imghdu.header)
    out_hdu.header['CRPIX1'] -= x1
    out_hdu.header['CRPIX2'] -= y1

    if (os.path.isfile(output_fn)):
        os.remove(output_fn)
    out_hdu.writeto(output_fn)

    #print xy, pixelscale, x1, x2, y1, y2

    pass

if __name__ == "__main__":

    fits_fn = sys.argv[1]
    if (not os.path.isfile(fits_fn)):
        print("Could not find input file %s" % (fits_fn))
        sys.exit(0)

    cat_fn = sys.argv[2]
    if (not os.path.isfile(cat_fn)):
        print("could not open table (%s)" % (cat_fn))
        sys.exit(0)

    out_fn_format = sys.argv[3]

    print("Loading input frame %s" % (fits_fn))
    hdulist = fits.open(fits_fn)
    img = hdulist[0].data
    header = hdulist[0].header


    print("Loading input catalog %s" % (cat_fn))
    table = vot.parse_single_table(cat_fn)

    ra = table.array['ra']
    dec = table.array['dec']
    petro_radius = table.array['petroRad_r']
    exp_radius = table.array['expRad_r']
    dev_radius = table.array['deVRad_r']
    objid = table.array['objid']

    for i_galaxy in range(ra.shape[0]):

        max_radius = numpy.max([petro_radius[i_galaxy],
                                exp_radius[i_galaxy],
                                dev_radius[i_galaxy]])
        print ra[i_galaxy], dec[i_galaxy], max_radius, objid[i_galaxy]

        output_fn = out_fn_format % (objid[i_galaxy])
        print output_fn

        cutout_region(hdulist[0], ra[i_galaxy], dec[i_galaxy], 5*max_radius, output_fn)

    #
    #
    # nx = int(sys.argv[2])
    # ny = int(sys.argv[3])
    # overlap = int(sys.argv[4])
    #
    #
    # sx = img.shape[1]/nx
    # sy = img.shape[0]/ny
    #
    #
    # for x,y in itertools.product(range(nx), range(ny)):
    #
    #     out_fn = "%s.x%02dy%02d.fits" % (fits_fn[:-5], x, y)
    #
    #     start_x = numpy.max([int(math.floor(x * sx - overlap)), 0])
    #     end_x = numpy.min([int(math.ceil((x+1)*sx + overlap)), img.shape[1]])
    #
    #     start_y = numpy.max([int(math.floor(y * sy - overlap)), 0])
    #     end_y = numpy.min([int(math.ceil((y+1)*sy + overlap)), img.shape[0]])
    #
    #     print("Creating cutout x=%02d, y=%02d (x: %5d--%5d, y: %5d--%5d) --> %s" % (
    #         x,y,start_x, end_x, start_y, end_y, out_fn)
    #           )
    #     cutout = img[start_y:end_y, start_x:end_x]
    #
    #     phdu = fits.PrimaryHDU(data=cutout, header=header)
    #     phdu.header['CRPIX1'] -= start_x
    #     phdu.header['CRPIX2'] -= start_y
    #
    #     # print("Writing cutout to %s" % (out_fn))
    #     phdu.writeto(out_fn, clobber=True)