A Guide to Understanding Color
=============================
source: https://www.xrite.com/-/media/xrite/files/whitepaper_pdfs/l10-001_a_guide_to_understanding_color_communication/l10-001_understand_color_en.pdf

Attributes of Color
-------------------
Hue, chroma and value accurately identifies a particular color
### Hue
* the percieves objetc's color (red, orange, green, blue, etc.)
* like a color wheel
### Chroma (or saturation)
* color vividness dullness
* pure hue (high chroma) vs gray (low chroma)
### Value (Brightness)
* luminous intensity of color
* degree of lightness 
* dark vs light


Three requirements of color
---------------------------
* light source
* object or sample (?reflective surface)
* observer or processor (eyes or sensor)

CIE Color Systems
-----------------
CIE: Commission Internationale de l'Eclairage 
(International Commision on Illumination)

### Three coordinates
* CIE XYZ
* CIE L\*a\*b
* CIE L\*C\*h^o

### Approach
Instruments percieve color the same way we do:
by gathering and filtering wavelengths of light reflected 
from an object, i.e. recording spectral data. The spectrum
is then mapped to a color in color space.

1. spectral reflective properties of surface
2. multiply with spectral properties of light source
   (A-incadescent, D65-daylight, or F2-fluorescent)
3. multiply standard observer spectral curves - 3 different
   curves - giving 3 scalar values - a 3d color representation
   called tristimulus values of XYZ (CIE).
   ?The curves' shape vary by observer angle?
  
### CIEXYZ 
#### CIEXYZ weaknesses
Tristimulus values have limited use as color specifications,
as they correlate poorly with visual attributes:
* Y relates to value (lightness) **- good**
* X and Z do not correlate to hue and chroma **- bad**

#### CIEXYZ chromaticity diagram
* **Hue** is changed by moving in the direction of the
  perimeter (turnwise and widdershins)
* **Saturation/Chroma**, is changed by moving between center (white) 
  and perimeter (at max saturation). 
  * Rimwards: more saturated colors (100 % saturation = pure hue)
  * Hubwards: more dull/gray colors

 
### CIELAB (L\*a\*b\*)
* L\* represents lightness. L=0 represents black or total absorbtion. 
  At the center of L=0 plane is neutral or gray
* a\* represents (low a)green/red(high a)
* b\* represents (low b)blue/yellow(high b)

### CIELCH (L\*C\*h^o)
The cylindrical coordinate system version of CIELAB (which is cartesian)
* L\* represents lightness (z)
* C\* represents chroma (radius)
* h^o represents hue angle (angle) giving the color

### Color Differences
CIELAB color difference:  `dE = np.sqrt((dL**2 + da**2 + db**2))`
CIELCH color difference:  `dE = np.sqrt((dL**2 + dC**2 + dh**2))`

Visual Color and Tolerancing
----------------------------
The eye does not detect differences in hue, chroma or lightness equally:
1. Hue differences (most detectable)
2. chroma differences
3. lightness differences (least detectable)
This means that we can change lightness the most, without someone
being able to notice that it is a different color.

The allowed differences in Hue, Chroma and Lightness before an 
observer can recognize it as another color is representer by
a **tolerance ellipsoid** (most elongated in the direction of lightness).
around the standard (color).

The tolerance ellipsoid sizes also varies with the hue values (green seems
to have broadest ones, while orange has the smallest values.





Pitfalls
========
* Mapping LAB colors (large color space) to RGB (limited color space)
  may cause colors not present in RGB space to be respresented by other
  colors in rgb space (giving some color where there should be none)
  Source: https://photo.stackexchange.com/questions/57576/why-does-l-0-not-correspond-to-black-in-the-lab-color-space


sRGB
====
sRGB (Standard Red Green Blue) is the standardized (or default) color space for 
online images, monitors and printers.
* contains no color space information
* pixels are stored in 8-bit integers per color channel (red-, green- 
  and blue-channel; gray scale photos have only one channel)

Gamut
=====
*Color Gamut* is a certain complete subset of colors.
Usually, it refers to the subset of colors which can be accurately represented in a
given circumstance, such as within a given color space or by a certain output device.

For example, the colors available to sRGB (typically used in computer monitors)
is only a subset of the color space of CIE 1931. The available colors of sRGB is
its gamut, and is only a small triangle within the larger "shark fin" of the CIE 1931
color space. See: https://en.wikipedia.org/wiki/Gamut


Additional Notes
================
* Typically, the full L\* range [0, 100] is encoded. However, the encoding 
  range of the a\* and b\* components is usually restricted to cover the 
  range [-128, 127]. Therefore, all possible Lab colors cannot be encoded 
  using this scheme. Even when 16-bit values are used instead of 8-bit values,
  the extra bits are used to make finer divisions between values, and are not 
  used to extend the range of values.
  http://www.brucelindbloom.com/index.html?LabGamutDisplayHelp.html

Other useful sources:
====================
* https://programmingdesignsystems.com/color/perceptually-uniform-color-spaces/
* https://sensing.konicaminolta.us/blog/understanding-the-cie-lch-color-space/
