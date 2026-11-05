import http.server,os,sys
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'dist')
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=D,**k)
    def log_message(s,*a): pass
    def send_head(s):
        p=s.path.split('?')[0]
        if p!='/' and '.' not in p.split('/')[-1] and os.path.exists(D+p+'.html'): s.path=p+'.html'
        elif not os.path.exists(D+p) and p!='/':
            s.send_response(404); s.send_header('Content-Type','text/html'); b=open(D+'/404.html','rb').read(); s.send_header('Content-Length',str(len(b))); s.end_headers(); s.wfile.write(b); return None
        return super().send_head()
http.server.ThreadingHTTPServer(('127.0.0.1',8787),H).serve_forever()
