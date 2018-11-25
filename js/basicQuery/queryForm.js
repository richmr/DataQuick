/*
Copyright 2018 Michael R Rich (mike@tofet.net)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions 
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

function queryFormStart () {
	// Activate the submit button
	$("#sendQuery").click(sendQuery);	
}

function sendQuery() {
	// Build the payload per basicquery site
	/*
		This is the cgi-callable pipe for basicQuery
		
		Called by a post call with a json payload:
			{
				sourcedb:"filename",
				tablename:"tablename",
				returnlimit:500 // Optional
				query:""	
			}
		
		Responds with a json type response from basicQuery
	*/
	// TODO: Need a thinking modal while waiting for the response.
	
	console.log("sendQuery clicked");
	payload = {
							sourcedb:$("#sourcedb").val(),
							tablename:$("#tablename").val(),
							returnlimit:$("#returnlimit").val(),
							query:$("#query").val()
						};
	$.post("cgi-bin/basicQuerySite.py", payload, queryResponse, "json");
}
