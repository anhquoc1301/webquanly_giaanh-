import datetime
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from urllib.parse import urljoin
import hashlib

class nvr_client:
    def __init__(self, host, login=None, password=None, timeout=3, isapi_prefix='ISAPI'):
        self.host = host
        self.login = login
        self.password = password
        self.timeout = float(timeout)
        self.isapi_prefix = isapi_prefix
        self.req = self._check_session()
        self.count_events = 1

    def download_file(self, url, file_path):
        # NOTE the stream=True parameter below
        with self.req.get(url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        return

    def _check_session(self):
        """Check the connection with device

         :return request.session() object
        """
        full_url = urljoin(self.host, self.isapi_prefix + '/System/status')
        session = requests.session()
        session.auth = HTTPBasicAuth(self.login, self.password)
        response = session.get(full_url)
        if response.status_code == 401:
            session.auth = HTTPDigestAuth(self.login, self.password)
            response = session.get(full_url)
        response.raise_for_status()
        return session

    def getNumberPlates(self, date, channel):
        date_str = date.strftime("%Y-%m-%d")
        hash = hashlib.sha1()
        hash.update(date_str.encode('utf-8'))
        
        payload = \
        '<CMSearchDescription>\
            <searchID>C96CF7F1-3690-0001-3339-'+ hash.hexdigest()[:12].upper() +'</searchID>\
            <trackList>\
                <trackID>'+ str(channel) + '03</trackID>\
            </trackList>\
            <timeSpanList>\
                <timeSpan>\
                    <startTime>' + date_str + 'T00:00:00Z</startTime>\
                    <endTime>' + date_str + 'T23:59:59Z</endTime>\
                </timeSpan>\
            </timeSpanList>\
            <contentTypeList>\
                <contentType>metadata</contentType>\
            </contentTypeList>\
            <maxResults>10000</maxResults>\
            <searchResultPostion>0</searchResultPostion>\
            <metadataList>\
                <metadataDescriptor>//recordType.meta.std-cgi.com/vehicleDetection</metadataDescriptor>\
                <SearchProperity>\
                    <plateSearchMask/>\
                    <country>255</country>\
                </SearchProperity>\
            </metadataList>\
        </CMSearchDescription>'\
            .format("0")

        response = self.req.request(
            method='post', url=self.host + "/ISAPI/ContentMgmt/search", timeout=self.timeout, stream=True, data=payload)
        return response

# selectedDate = datetime.datetime(year=2021, month=7, day=9)
# cam = nvr_client('http://thanhphat-modem.ddns.net', 'admin', '123456a@')
# res = cam.getPlates(selectedDate, 2)
# print(res.text)