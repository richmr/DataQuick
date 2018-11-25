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
$(document).ready(function(){
	 // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
	
	$('.modal').modal();
	//$('select').material_select();
	
	queryFormStart();
	
});

function newData() {
	//console.log("newData() running.");
	initializeComboReadings();	
	comboListInit();
	//clearHTML();
	initializePortfolio();
	//initializePriorityTable();
	//initializeArchive();
	//initializedonePeople();
	//initializegraveyard();
}

function clearHTML() {
	// These functions are designed to delete the existing DOM/HTML data, but not
	// the values in the global variables.  Those are needed to recreate the correct table!
	clearPriorityTable();
	clearArchive();
	//cleardonePeople();
	clearGraveyard();
}

function exitCombo() {
	// An attempt to save the data when the user leaves the page, or the window closes
	//saveArchive();
	//saveGraveyard();
	//saveDone();
	saveAllData();
	console.log("Combo data saved.");
} 
	 
console.log("basicQuery loaded");