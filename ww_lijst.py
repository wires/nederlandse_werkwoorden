import os, string, urllib2, json
import lxml.html as lh

url = lambda s: "http://www.fourlangwebprogram.com/fourlang/es/ww_nl_%s.htm" % s

# cleanup function
clean = lambda s: string.strip(s).encode('utf8')
noNuns = lambda xs: filter(lambda x: not x is None, xs)

# paginering
ps = list("abcdefghijklmnop") + ["qr"] + list("rstuvw") + ["xyz"]

pagina = lambda s: urllib2.urlopen(url(s.upper()))

fn = lambda i: 'data/%s.html' % i

for i in ps:
	print fn(i)

	# effe cachen
	if not os.path.exists(fn(i)):
		with open(fn(i), 'wb') as f:
			f.write(pagina(i).read())

print "-"*20

dus = []

with open('lijst.txt','wb') as lijst:
	for i in ps:
		print fn(i)

		stats = 0
		# inladen van disc en parsen
		with open(fn(i), 'rb') as f:

			doc = lh.parse(f)

			# infinitieven
			for row in doc.xpath('//table//tr'):
				cols = row.xpath('.//td')

				if not len(cols) == 3:
					continue

				# infinitief, verleden tijd, voltooid deelwoord
				vormen = row.xpath('.//td/a/text()|.//td/text()')

				# cleanup
				vormen = noNuns(map(clean, noNuns(vormen)))

				if not len(vormen) == 3:
					continue

				if len(vormen[1].split(' ')) > 1:
					print vormen[1]
					continue

				lijst.write("%s\t%s\t%s\n" % tuple(vormen))
				dus.append(vormen)
				stats += 1

		print stats

json.dump(dus, open('lijst.json','wb'))
