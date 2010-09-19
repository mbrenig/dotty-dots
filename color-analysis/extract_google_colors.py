import re, colorsys

hexvals = re.compile('Point\((?P<xx>[^,]+),(?P<yy>[^,]+),(?P<zz>[^,]+),(?P<size>[^,]+), "(?P<color>\#\w\w\w\w\w\w)"\)')

# The line from Rob Hawkes' original code defining each point..
data = """[new Point(202, 78, 0.0, 9, "#ed9d33"), new Point(348, 83, 0.0, 9, "#d44d61"), new Point(256, 69, 0.0, 9, "#4f7af2"), new Point(214, 59, 0.0, 9, "#ef9a1e"), new Point(265, 36, 0.0, 9, "#4976f3"), new Point(300, 78, 0.0, 9, "#269230"), new Point(294, 59, 0.0, 9, "#1f9e2c"), new Point(45, 88, 0.0, 9, "#1c48dd"), new Point(268, 52, 0.0, 9, "#2a56ea"), new Point(73, 83, 0.0, 9, "#3355d8"), new Point(294, 6, 0.0, 9, "#36b641"), new Point(235, 62, 0.0, 9, "#2e5def"), new Point(353, 42, 0.0, 8, "#d53747"), new Point(336, 52, 0.0, 8, "#eb676f"), new Point(208, 41, 0.0, 8, "#f9b125"), new Point(321, 70, 0.0, 8, "#de3646"), new Point(8, 60, 0.0, 8, "#2a59f0"), new Point(180, 81, 0.0, 8, "#eb9c31"), new Point(146, 65, 0.0, 8, "#c41731"), new Point(145, 49, 0.0, 8, "#d82038"), new Point(246, 34, 0.0, 8, "#5f8af8"), new Point(169, 69, 0.0, 8, "#efa11e"), new Point(273, 99, 0.0, 8, "#2e55e2"), new Point(248, 120, 0.0, 8, "#4167e4"), new Point(294, 41, 0.0, 8, "#0b991a"), new Point(267, 114, 0.0, 8, "#4869e3"), new Point(78, 67, 0.0, 8, "#3059e3"), new Point(294, 23, 0.0, 8, "#10a11d"), new Point(117, 83, 0.0, 8, "#cf4055"), new Point(137, 80, 0.0, 8, "#cd4359"), new Point(14, 71, 0.0, 8, "#2855ea"), new Point(331, 80, 0.0, 8, "#ca273c"), new Point(25, 82, 0.0, 8, "#2650e1"), new Point(233, 46, 0.0, 8, "#4a7bf9"), new Point(73, 13, 0.0, 8, "#3d65e7"), new Point(327, 35, 0.0, 6, "#f47875"), new Point(319, 46, 0.0, 6, "#f36764"), new Point(256, 81, 0.0, 6, "#1d4eeb"), new Point(244, 88, 0.0, 6, "#698bf1"), new Point(194, 32, 0.0, 6, "#fac652"), new Point(97, 56, 0.0, 6, "#ee5257"), new Point(105, 75, 0.0, 6, "#cf2a3f"), new Point(42, 4, 0.0, 6, "#5681f5"), new Point(10, 27, 0.0, 6, "#4577f6"), new Point(166, 55, 0.0, 6, "#f7b326"), new Point(266, 88, 0.0, 6, "#2b58e8"), new Point(178, 34, 0.0, 6, "#facb5e"), new Point(100, 65, 0.0, 6, "#e02e3d"), new Point(343, 32, 0.0, 6, "#f16d6f"), new Point(59, 5, 0.0, 6, "#507bf2"), new Point(27, 9, 0.0, 6, "#5683f7"), new Point(233, 116, 0.0, 6, "#3158e2"), new Point(123, 32, 0.0, 6, "#f0696c"), new Point(6, 38, 0.0, 6, "#3769f6"), new Point(63, 62, 0.0, 6, "#6084ef"), new Point(6, 49, 0.0, 6, "#2a5cf4"), new Point(108, 36, 0.0, 6, "#f4716e"), new Point(169, 43, 0.0, 6, "#f8c247"), new Point(137, 37, 0.0, 6, "#e74653"), new Point(318, 58, 0.0, 6, "#ec4147"), new Point(226, 100, 0.0, 5, "#4876f1"), new Point(101, 46, 0.0, 5, "#ef5c5c"), new Point(226, 108, 0.0, 5, "#2552ea"), new Point(17, 17, 0.0, 5, "#4779f7"), new Point(232, 93, 0.0, 5, "#4b78f1")]"""

points = hexvals.findall(data)

rgbs = []

reds = []
blues = []
greens = []
yellows = []

for point in points:
	c = point[4]
	size = int(point[3])
	red = int(c[1:3], 16)
	green = int(c[3:5], 16)
	blue = int(c[5:7], 16)
	hue = colorsys.rgb_to_hls(red/255.0, green/255.0, blue/255.0)[0]*360
	if hue < 5:
		hue += 360
	rgbs.append( (red,green,blue, hue, size) )
	
	if 200 < hue < 250:
		blues.append( (red, green, blue, size) ) 
	elif 340 < hue < 365:
		reds.append( (red, green, blue, size))
	elif 120 < hue < 130:
		greens.append( (red, green, blue, size) )
	elif 30 < hue < 50:
		yellows.append( (red, green, blue, size) )
	else:
		print "ERROR with %s" % [red, green, blue, hue]
	
rgbs.sort(lambda x,y: cmp(x[3],y[3]))

#for x in rgbs:
#	print x

def write_rgbs( filename, colors):	
	ouf = open(filename,'w')
	ouf.write("R\tG\tB\tSize\n")
	for c in colors:
		ouf.write("%s\t%s\t%s\t%s\n" % (c[0], c[1], c[2], c[3]) )
	

write_rgbs("google_rgb.txt", rgbs)
write_rgbs("google_reds.txt", reds)
write_rgbs("google_blues.txt", blues)
write_rgbs("google_yellows.txt", yellows)
write_rgbs("google_greens.txt", greens)
