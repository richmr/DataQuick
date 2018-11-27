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

// Fields to displayed in results header
responseHeaderFields = ["filename"];

// Fields that get translated to human readable times
responseTimeFields = [];

$("#warningBlock").hide()

function queryResponse (data) {
	console.log("Query response received");
	$("#warningBlock").hide();

	if (data['Error']) {
		errorResponse(data);
		data["Results"] = [];
	}
	if (data['Warning']) warningResponse(data);
	showResults(data["Results"]);
	
	//$("#queryResults").html(JSON.stringify(data));
}

function errorResponse(data) {
	console.log(JSON.stringify(data));
	$("#BQueryError-ErrMsg").text(data["ErrorMsg"]);
	$("#BQueryError").modal('open');
}

function warningResponse(data) {
	console.log(JSON.stringify(data));
	$("#warningMsg").text(data["WarningMsg"]);
	$("#warningBlock").show()
}

function showResults(results) {
	// builds and inserts the html for the table
	// Build first
	console.log(JSON.stringify(results))
	htmlsnippet = ""
	if (results.length == 0) {
		htmlsnippet += '<li><div class="collapsible-header">No matching records found</div></li>';
		$("#results_collapsible").html(htmlsnippet);
		return;     
	}
	
	$.each(results, function (index, aresult) {
		//timeConvert(aresult);
		htmlsnippet += resultHeader(aresult);
		htmlsnippet += resultTable(aresult);	
	});
	
	$("#results_collapsible").html(htmlsnippet);
 }

function timeConvert(aresult) {
	// Converts times in a result to human readable form	
	// TODO
	return
}

function resultHeader(aresult) {
	htmlsnippet = '<li><div class="collapsible-header">';
	resultKeys = Object.keys(aresult);
	resultValues = Object.values(aresult);
	
	headerdata = [];
	noHeaderFound = true;
	$.each(responseHeaderFields, function (index, fieldname) {
		if (fieldname in aresult) {
			noHeaderFound = false;
			headerdata.push(aresult[fieldname]);			
		}
	});
	htmlsnippet += headerdata.join(",");	
		
	if (noHeaderFound) {
		// Then the header is a	concatenated string of values
		htmlsnippet += resultValues.join(",");
	}
		
	htmlsnippet += "</div>";
	return htmlsnippet;
}

function resultTable(aresult) {
	// Builds and returns a table in a <li> element
	htmlsnippet = '<div class="collapsible-body">';
	htmlsnippet += '<table class="striped"><thead><tr><th>Field</th><th>Value</th></tr></thead>';
	htmlsnippet += '<tbody>';
	$.each(aresult, function (key, value) {
			htmlsnippet += '<tr>';
			htmlsnippet += '<td>'+key+'</td>';
			htmlsnippet += '<td>'+value+'</td>';
			htmlsnippet += '</tr>';		
		});
	htmlsnippet += '</tbody></table></div></li>'
	return htmlsnippet;

}

/*
<ul id="featured_collapsible" class="collapsible expandable">
						<li>
						      <div class="collapsible-header">Results</div>
						      <div class="collapsible-body"><span>Send a query!</span></div>
						</li>
				</ul>
				<br>
				Fields
				<ul id="fields_collapsible" class="collapsible expandable">
						<li>
						      <div class="collapsible-header">Results</div>
						      <div class="collapsible-body"><span>Send a query!</span></div>
						</li>
				</ul>			
				
function setupFieldsMenu() {

}
*/

 