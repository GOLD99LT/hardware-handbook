import urllib.request, time
urls = [
  'https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/echarts/5.5.1/echarts.min.js',
  'https://unpkg.com/echarts@5.5.1/dist/echarts.min.js',
]
for u in urls:
    try:
        t0 = time.time()
        r = urllib.request.urlopen(u, timeout=12)
        data = r.read(2000)
        print('OK  %.1fs  %dbytes  %s' % (time.time()-t0, len(data), u))
    except Exception as e:
        print('FAIL  %s  %s' % (type(e).__name__, u))
