#! /usr/bin/osascript -l JavaScript

/* exitShellScript.jxa.sh: exit a shell script using JavaScript for Automation.
 *
 * This snippet is designed to be worked into any JavaScript capable of
 * running osascript with the JavaScript option (probably OS X 10.4 or later.)
 */
 
var curApp = Application.currentApplication();
curApp.includeStandardAdditions = true;

// Following line causes script to exit _before_ 'echo 1; exit 1'.
curApp.doShellScript('echo 0; exit 0; echo 1; exit 1');

// console.log:
// 0

