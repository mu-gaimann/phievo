from phievo import __silent__,__verbose__
if __verbose__:
    print("Execute palette.py")
from matplotlib import pylab,colors

default_colormap = "gist_rainbow"

def update_default_colormap(colormap):
    """
    Update the color map used by the palette modules

    Arg:
        colormap (str): name of the matplotlib colormap
            http://matplotlib.org/examples/color/colormaps_reference.html
    """
    global default_colormap
    default_colormap = colormap


def HSL_to_RGB(h,s,l):
    '''Converts HSL colorspace (Hue/Saturation/Value) to RGB colorspace.
    Formula from http://www.easyrgb.com/math.php?MATH=M19#text19

    Args:
        h (float) : Hue (0...1, but can be above or below
                          (This is a rotation around the chromatic circle))
        s (float) : Saturation (0...1)    (0=toward grey, 1=pure color)
        l (float) : Lightness (0...1)     (0=black 0.5=pure color 1=white)

    Return:
        (r,g,b) (integers 0...255) : Corresponding RGB values

    Examples:
        >>> print HSL_to_RGB(0.7,0.7,0.6)
        (110, 82, 224)
        >>> r,g,b = HSL_to_RGB(0.7,0.7,0.6)
        >>> print g
        82
    '''
    def Hue_2_RGB( v1, v2, vH ):
        while vH<0.0: vH += 1.0
        while vH>1.0: vH -= 1.0
        if 6*vH < 1.0 : return v1 + (v2-v1)*6.0*vH
        if 2*vH < 1.0 : return v2
        if 3*vH < 2.0 : return v1 + (v2-v1)*((2.0/3.0)-vH)*6.0
        return v1

    if not (0 <= s <=1): raise ValueError("s (saturation) parameter must be between 0 and 1.")
    if not (0 <= l <=1): raise ValueError("l (lightness) parameter must be between 0 and 1.")

    r,b,g = (l*255,)*3
    if s!=0.0:
       if l<0.5 : var_2 = l * ( 1.0 + s )
       else     : var_2 = ( l + s ) - ( s * l )
       var_1 = 2.0 * l - var_2
       r = 255 * Hue_2_RGB( var_1, var_2, h + ( 1.0 / 3.0 ) )
       g = 255 * Hue_2_RGB( var_1, var_2, h )
       b = 255 * Hue_2_RGB( var_1, var_2, h - ( 1.0 / 3.0 ) )

    return (int(round(r)),int(round(g)),int(round(b)))

def floatrange(start,stop,steps):
    '''Computes a range of floating value.

    Args:
        start (float)  : Start value.
        end   (float)  : End value
        steps (integer): Number of values

    Return:
        list: A list of floats with fixed step

    Example:
        >>> print floatrange(0.25, 1.3, 5)
        [0.25, 0.51249999999999996, 0.77500000000000002, 1.0375000000000001, 1.3]
    '''
    return [start+float(i)*(stop-start)/(float(steps)-1) for i in range(steps)]

def color_generate(n,colormap=None):
    """Returns a palette of colors suited for charting.

    Args:
        n (int): The number of colors to return
        colormap (str): matplotlib colormap name
                http://matplotlib.org/examples/color/colormaps_reference.html

    Return:
        list: A list of colors in HTML notation (eg.['#cce0ff', '#ffcccc', '#ccffe0', '#f5ccff', '#f5ffcc'])

    Example:
        >>> print color_generate(5)
        ['#5fcbff','#e5edad','#f0b99b','#c3e5e4','#ffff64']
    """

    
    if type(colormap)==colors.LinearSegmentedColormap:
        cm = colormap
    else:
        if not colormap:
            colormap = default_colormap
        cm = pylab.get_cmap(default_colormap)
    color_l= [colors.rgb2hex(cm(1.*i/n)) for i in range(n)]
    return color_l


def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [colors.ColorConverter().to_rgb(col) if type(col)!=float else col for col in seq]
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return colors.LinearSegmentedColormap('CustomMap', cdict)

def generate_gradient(values,seq):
    """
    Generates a desired list of colors along a gradient from a custom list of colors.

    args:
        values: list of values that need to ba allocated to a color
        seq: sequence of colors in the gradient
    """
    cm = make_colormap(seq)
    return [colors.rgb2hex(cm((val - min(values))/(max(values) - min(values)))) for val in  values]
    
