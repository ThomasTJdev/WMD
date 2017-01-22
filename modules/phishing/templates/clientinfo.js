<script>
var timeOpened = Date();
var pathname = window.location.pathname;
var referrer = document.referrer;
var previousSites = history.length;

var browserName = navigator.appName;
var browserEngine = navigator.product;
var browserVersion1a = navigator.appVersion;
var browserVersion1b = navigator.userAgent;
var browserLanguage = navigator.language;
var browserOnline = navigator.onLine;
var browserPlatform = navigator.platform;
var javaEnabled = navigator.javaEnabled();
var dataCookiesEnabled = navigator.cookieEnabled;
var dataCookies1 = document.cookie;
var dataCookies2 = decodeURIComponent(document.cookie.split(";"));
var dataStorage = localStorage;

var sizeScreenW = screen.width;
var sizeScreenH = screen.height;
var sizeDocW = document.width;
var sizeDocH = document.height;
var sizeInW = innerWidth;
var sizeInH = innerHeight;
var sizeAvailW = screen.availWidth;
var sizeAvailH = screen.availHeight;
var scrColorDepth = screen.colorDepth;
var scrPixelDepth = screen.pixelDepth;

document.getElementById("browser").value = '{"timeOpened": "' + timeOpened +'", "pathname": "' + pathname
  + '", "referrer": "' + referrer + '", "previousSites": "' + previousSites + '", "browserName": "' + browserName
  + '", "browserEngine": "' + browserEngine + '", "browserVersion1a": "' + browserVersion1a + '", "browserVersion1b": "' + browserVersion1b
  + '", "browserLanguage": "' + browserLanguage + '", "browserOnline": ' + browserOnline + '", "browserPlatform": ' + browserPlatform
  + '", "javaEnabled": "' + javaEnabled + '", "dataCookiesEnabled": "' + dataCookiesEnabled + '", "dataCookies1": ' + dataCookies1
  + '", "dataCookies2": "' + dataCookies2 + '", "dataStorage": "' + dataStorage + '", "sizeScreenW": "' + sizeScreenW
  + '", "sizeScreenH": "' + sizeScreenH + '", "sizeDocW": "' + sizeDocW + '", "sizeDocH": "' + sizeDocH
  + '", "sizeInW": ' + sizeInH + '", "sizeAvailW": ' + sizeAvailW + '", "sizeAvailH": ' + sizeAvailH
  + '", "scrColorDepth": "' + scrColorDepth + '", "scrPixelDepth": "' + scrPixelDepth + '"}';


</script>



<script type="application/javascript">
  function getAll(json) {
      var allas = json.as;
      var allcity = json.city;
      var allcountry = json.country
      var allcountryCode = json.countryCode
      var allisp = json.isp;
      var alllat = json.lat;
      var alllon = json.lon;
      var allorg = json.org;
      var allquery = json.query;
      var allregion = json.region;
      var allregionName = json.regionName;
      var allstatus = json.status;
      var alltimezone = json.timezone;
      var allzip = json.zip;

      document.getElementById("network").value = '{"AS": "' + allas +'", "city": "' + allcity
        + '", "country": "' + allcountry + '", "isp": "' + allisp + '", "lat": "' + alllat
        + '", "lon": "' + alllon + '", "query": "' + allquery + '", "status": "' + allstatus
        + '", "timezone": "' + alltimezone + '", "zip": "' + allzip + '"}';

  }
</script>
<script type="application/javascript" src="http://ip-api.com/json?format=json&callback=getAll"></script>




<script>
function getUserIP(onNewIP) { //  onNewIp - your listener function for new IPs
    //compatibility for firefox and chrome
    var myPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
    var pc = new myPeerConnection({
        iceServers: []
    }),
    noop = function() {},
    localIPs = {},
    ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/g,
    key;

    function iterateIP(ip) {
        if (!localIPs[ip]) onNewIP(ip);
        localIPs[ip] = true;
    }

     //create a bogus data channel
    pc.createDataChannel("");

    // create offer and set local description
    pc.createOffer(function(sdp) {
        sdp.sdp.split('\n').forEach(function(line) {
            if (line.indexOf('candidate') < 0) return;
            line.match(ipRegex).forEach(iterateIP);
        });

        pc.setLocalDescription(sdp, noop, noop);
    }, noop);

    //listen for candidate events
    pc.onicecandidate = function(ice) {
        if (!ice || !ice.candidate || !ice.candidate.candidate || !ice.candidate.candidate.match(ipRegex)) return;
        ice.candidate.candidate.match(ipRegex).forEach(iterateIP);
    };
}
getUserIP(function(ip){
    document.getElementById("iplocal").value = ip;
});
</script>


<script type="application/javascript">
  function getIP(json) {
      document.getElementById("ipexternal").value = json.ip;
  }
</script>
<script type="application/javascript" src="https://api.ipify.org?format=jsonp&callback=getIP"></script>
