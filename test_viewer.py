"""Reader, comparison, persistence and local HTTP integration checks.

Five real recordings are optional local fixtures. Synthetic tests always run;
real-file checks are explicitly skipped when those private fixtures are absent.
"""
import copy
import json
import os
from pathlib import Path
import struct
import tempfile
import threading
import unittest
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import numpy as np
from rph_reader import read_rph
from graph_viewer import Session, make_server, validate_view
from standard_views import STANDARD_VIEWS

RPH_DIR = Path(os.environ.get("EAF_RPH_DIR", Path.home() / "Downloads"))
REAL = RPH_DIR / "Hoeganaes23217.rph"


def fixture(names=("Current1", "Current2"), delta=0):
    raw=bytearray(23);raw[:4]=b'\x81\x07\x0f\x2c';struct.pack_into('<H',raw,21,len(names))
    for name in names:
        b=name.encode('ascii');raw.extend(bytes([len(b)])+b)
    raw.extend(struct.pack('<I',3))
    for row in range(3):raw.extend(struct.pack('<H',len(names))+struct.pack('<'+'f'*len(names),*[row+i+delta for i in range(len(names))]))
    raw.extend(struct.pack('<H',3))
    for sec in (1000,1001,1010):raw.extend(struct.pack('<IHHI',sec+delta,250,360,0))
    raw.extend(b'\0'*4)
    return bytes(raw)


class ViewerTests(unittest.TestCase):
    @unittest.skipUnless(REAL.is_file(), "Private RPH fixture not available; set EAF_RPH_DIR")
    def test_real_file_and_all_presets(self):
        r=read_rph(REAL.read_bytes())
        self.assertEqual(r.values.shape,(3701,644));self.assertEqual(r.gaps,15)
        self.assertEqual(r.values[-1,r.names.index('MWH_PX3')],25)
        self.assertAlmostEqual(r.seconds[0],1794552762.611,places=3)
        for view in STANDARD_VIEWS:
            self.assertTrue(set(s['name'] for s in view['signals']) <= set(r.names))

    def test_corrupt_files_rejected(self):
        raw=fixture()
        for bad in (raw[:20],raw[:-1],raw+b'\0',b'CSV!'+raw[4:]):
            with self.assertRaises(ValueError):read_rph(bad)
        bad=bytearray(raw);bad[-12:-10]=b'\xff\xff'
        with self.assertRaises(ValueError):read_rph(bad)

    def test_overlay_preserves_values_and_breaks_gaps(self):
        with tempfile.TemporaryDirectory() as d:
            s=Session(d);a=s.add('first.rph',fixture());b=s.add('second.rph',fixture(delta=100))
            request={'files':[a['id'],b['id']], 'signals':[{'name':'Current1','axis':'right','color':'#112233'}]}
            traces=s.data(request)['traces'];self.assertEqual(len(traces),2)
            self.assertEqual(traces[0]['x'],traces[1]['x']);self.assertEqual(traces[0]['y'],[0,1,None,2]);self.assertEqual(traces[1]['y'],[100,101,None,102])
            self.assertEqual(traces[0]['yaxis'],'y2');self.assertNotEqual(traces[0]['line']['dash'],traces[1]['line']['dash'])
            request['x']='clock';t=s.data(request)['traces'];self.assertEqual(t[1]['x'][0]-t[0]['x'][0],100000)
            request['files']=[b['id']];self.assertEqual(len(s.data(request)['traces']),1)
            self.assertEqual(s.add('duplicate.rph',fixture())['id'],a['id']);self.assertEqual(len(s.files),2)

    def test_missing_signal_and_view_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            s=Session(d);a=s.add('first.rph',fixture())
            v=copy.deepcopy(STANDARD_VIEWS[1]);v['name']='Sergio / phase comparison';s.save(v)
            self.assertEqual(Session(d).views[v['name']]['signals'],v['signals'])
            second=Session(d)
            s.save({**v,'name':'First window'})
            second.save({**v,'name':'Second window'})
            self.assertIn('First window',Session(d).views)
            result=s.data({**v,'files':[a['id']]});self.assertEqual(len(result['missing']),2)
            self.assertEqual(len(result['traces']),2)
            self.assertEqual(list(Path(d).glob('*.tmp')),[])
            (Path(d)/'views.json').write_text('broken')
            broken=Session(d)
            with self.assertRaises(ValueError):broken.save(v)
            self.assertEqual((Path(d)/'views.json').read_text(),'broken')

    def test_http_routes_and_origin(self):
        with tempfile.TemporaryDirectory() as d:
            s=Session(d);server,url=make_server(s);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                with urlopen(url) as r:self.assertIn(b'Overlay files',r.read())
                with urlopen(url+'cursor_tools.js') as r:self.assertIn(b'PinStore',r.read())
                with urlopen(Request(url+'upload?name=test.rph',data=fixture())) as r:meta=json.load(r)
                with urlopen(url+'state') as r:state=json.load(r)
                self.assertEqual(len(state['presets']),5);self.assertEqual(state['files'][0]['id'],meta['id'])
                with self.assertRaises(HTTPError):urlopen(Request(url+'state',headers={'Origin':'https://example.org'}))
                with self.assertRaises(HTTPError):urlopen(url.replace(url.split('/')[-2],'wrong'))
            finally:server.shutdown();server.server_close();thread.join()

    def test_bad_view_shapes_and_settings(self):
        for broken in ({}, {'unexpected':'shape'}, None, 'text'):
            with tempfile.TemporaryDirectory() as d:
                file=Path(d)/'views.json';original=json.dumps(broken);file.write_text(original,encoding='utf-8')
                session=Session(d)
                self.assertTrue(session.warning)
                with self.assertRaises(ValueError):session.save(STANDARD_VIEWS[0])
                self.assertEqual(file.read_text(encoding='utf-8'),original)
        for field,bad in [('width',True),('width',float('nan')),('width',0),('chart','bad'),('mode','bad'),('x','bad'),('lines','bad')]:
            with self.assertRaises(ValueError):validate_view({**STANDARD_VIEWS[0],field:bad})
        with self.assertRaises(ValueError):validate_view({'name':'Bad','signals':[{'name':'Current1','axis':'oops'}]})

    @unittest.skipUnless(all((RPH_DIR / f"Hoeganaes{n}.rph").is_file() for n in range(23215,23220)), "Five private RPH fixtures not available; set EAF_RPH_DIR")
    def test_real_recordings_and_stable_file_styles(self):
        with tempfile.TemporaryDirectory() as d:
            s=Session(d)
            for path in sorted(REAL.parent.glob('Hoeganaes2321[5-9].rph')):s.add(path.name,path.read_bytes())
            self.assertEqual(len(s.files),5)
            ids=list(s.files);view={**STANDARD_VIEWS[3],'files':ids,'chart':'scatter'}
            together=s.data(view)['traces'];count=len(view['signals'])
            self.assertEqual(len(together),5*count)
            alone=s.data({**view,'files':[ids[3]]})['traces']
            self.assertEqual(alone[0]['line'],together[count*3]['line'])
            self.assertEqual(alone[0]['marker'],together[count*3]['marker'])
            self.assertEqual(alone[0]['uid'],together[count*3]['uid'])
            for trace in together:self.assertRegex(trace['uid'],r'^t[0-9a-f]{24}$')

    def test_external_view_changes_and_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            first=Session(d);second=Session(d)
            second.save({**STANDARD_VIEWS[0],'name':'Second window'})
            first.reload_views();self.assertIn('Second window',first.views)
            file=Path(d)/'views.json';file.write_text('{}',encoding='utf-8')
            first.reload_views();self.assertTrue(first.warning)
            file.write_text('[]',encoding='utf-8');first.reload_views();self.assertFalse(first.warning)
            first.save(STANDARD_VIEWS[0])

    def test_xy_pairs_preserve_sample_order_gaps_and_timestamps(self):
        raw=bytearray(fixture(('Drive','Response')))
        offset=23+sum(1+len(n) for n in ('Drive','Response'))+4
        for i,(x,y) in enumerate([(3,30),(1,10),(3,31)]):
            struct.pack_into('<ff',raw,offset+i*10+2,x,y)
        with tempfile.TemporaryDirectory() as d:
            s=Session(d);a=s.add('loop.rph',bytes(raw))
            view={'name':'X-Y','files':[a['id']],'x':'signal','x_signal':'Drive','chart':'scatter','signals':[{'name':'Response','axis':'right'}]}
            t=s.data(view)['traces'][0]
            self.assertEqual(t['x'],[3,1,None,3]);self.assertEqual(t['y'],[30,10,None,31])
            self.assertEqual(t['yaxis'],'y2');self.assertEqual(t['mode'],'markers')
            self.assertEqual(t['customdata'][0],['1970-01-01T00:16:40.250+00:00',0])
            self.assertIsNone(t['customdata'][2]);self.assertEqual(t['customdata'][3][1],10/60)
            for chart,mode in [('lines','lines'),('both','lines+markers')]:
                line=s.data({**view,'chart':chart})['traces'][0]
                self.assertEqual(line['x'],t['x']);self.assertFalse(line['connectgaps']);self.assertEqual(line['mode'],mode)
            s.save(view);saved=Session(d).views['X-Y'];self.assertEqual(saved['x_signal'],'Drive');self.assertEqual(saved['x'],'signal')
            identity=s.data({**view,'signals':[{'name':'Drive'}]})['traces'][0]
            self.assertEqual(identity['x'],identity['y'])

    def test_xy_missing_and_nonfinite_samples_and_file_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            s=Session(d);a=s.add('A.rph',fixture());b=s.add('B.rph',fixture(delta=100));c=s.add('C.rph',fixture(('Other','Current2')))
            view={'files':[a['id'],b['id'],c['id']],'x':'signal','x_signal':'Current1','signals':[{'name':'Current2'}]}
            result=s.data(view);self.assertEqual(len(result['traces']),2)
            self.assertEqual(result['missing'],['C.rph: X signal Current1'])
            self.assertEqual(result['traces'][1]['x'],[100,101,None,102]);self.assertEqual(result['traces'][1]['y'],[101,102,None,103])
            empty=s.data({**view,'x_signal':'Absent'});self.assertEqual(empty['traces'],[]);self.assertEqual(len(empty['missing']),3)
            s.files[a['id']]['recording'].values[0,0]=np.nan;s.files[a['id']]['recording'].values[1,1]=np.inf
            t=s.data({**view,'files':[a['id']]})['traces'][0]
            self.assertEqual(t['x'],[None,1,None,2]);self.assertEqual(t['y'],[None,None,None,3])
            json.dumps(t,allow_nan=False)

    def test_xy_validation_and_legacy_views(self):
        for bad in (None,False,123,[],{},'', '   ', 'x'*256):
            with self.assertRaises(ValueError):validate_view({'name':'Bad','signals':[],'x':'signal','x_signal':bad})
        with self.assertRaises(ValueError):validate_view({'name':'Bad','signals':[],'x':'signal'})
        old=validate_view(STANDARD_VIEWS[0]);self.assertEqual(old['x'],'elapsed');self.assertEqual(old['x_signal'],'')
        with tempfile.TemporaryDirectory() as d:
            s=Session(d)
            for bad in ([],None,'bad'):
                with self.assertRaises(ValueError):s.data(bad)


if __name__=='__main__':unittest.main()
