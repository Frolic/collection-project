<script language="javascript">

function getDiv(name){return (document.layers&&document.layers[name])?document.layers[name]:(document.all&&document.all[name]&&document.all[name].style)?document.all[name].style:document[name]?document[name]:(document.getElementById(name)?document.getElementById(name).style:0);}

function getRootNode(xml, nodeName)
{
	if( xml == '' )
		return null;

	if (window.ActiveXObject)
	{
	
		// code for IE
		doc=new ActiveXObject("Microsoft.XMLDOM");
		doc.async="false";
		doc.loadXML(xml);
		if( doc == null ) return null;
	    return doc.documentElement.selectSingleNode(nodeName);
	}
	else
	{
		// code for Mozilla, Firefox, Opera, etc.
		var parser=new DOMParser();
		doc=parser.parseFromString(xml,"text/xml");
		
		
		  var xpe = new XPathEvaluator();
		  var xmlDoc=doc;		  
          var results = xpe.evaluate(nodeName,xmlDoc,null,XPathResult.ANY_TYPE, null);
          var result=results.iterateNext();

         return result;
	}
}

function execCommand(commandURL)
{
	var xmlHttp = null;
	if (navigator.appName.toLowerCase().indexOf("microsoft") >= 0)
	{
		xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	else if (navigator.appName.toLowerCase().indexOf("netscape") >= 0) 
	{
		xmlHttp = new XMLHttpRequest();
	}

	if(xmlHttp != null)
	{
		xmlHttp.open("GET", commandURL, false);
		xmlHttp.send(null);
		return xmlHttp.responseText;
	}		
	return null;
}

function showAJAXinTip(command,divName){
    showDiv(divName);
	var xml = execCommand(command);	
	q=document.getElementById(divName);
    q.innerHTML+=xml;
}

function cleanDiv(divName){
	q=document.getElementById(divName);
	q.innerHTML="";	
	hideDiv(divName);
}


function showDiv(divName){
    a=getDiv(divName);
    a.visibility=(document.layers)?"show":"visible";
}
		    
		    
function hideDiv(divName){
    q=getDiv(divName);
    q.visibility=(document.layers)?"hide":"hidden"; 
}

</script>