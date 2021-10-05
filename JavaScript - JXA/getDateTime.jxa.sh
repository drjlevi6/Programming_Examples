#! /usr/bin/osascript -l JavaScript

/* getDateTime.jxa.sh: get date, time via a shell script, using JavaScript for
 * Automation.
 *
 * This snippet is designed to be worked into any JavaScript capable of
 * running osascript with the JavaScript option (probably OS X 10.4 or later.)
 */
 
var curApp = Application.currentApplication();
curApp.includeStandardAdditions = true;

dateTimeString = getDateTime('+%Y%d%m-%H%M%S');
console.log(dateTimeString);

function getDateTime(formatString) {
	return (curApp.doShellScript("date \'" + formatString + "\'"));
}

