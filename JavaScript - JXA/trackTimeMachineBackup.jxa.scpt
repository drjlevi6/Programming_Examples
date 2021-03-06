JsOsaDAS1.001.00bplist00?Vscript_?/* trackTimeMachineBackup.jxa.scpt: track progress of Time Machine backups
 * using JavaScript for Automation.
 *
 * Script crashes if we're using virtual desktops and switch during operation.
 */

/*-----Initialization---------------------------------------------------------*/
var curApp = Application.currentApplication();
curApp.includeStandardAdditions = true;

var sysEvts = Application('System Events');
var sysPrefsApp = Application('System Preferences');
var sysPrefs = sysEvts.applicationProcesses.byName("System Preferences");

var tmWindow = sysPrefs.windows.byName("Time Machine");
var tmTable = tmWindow.groups.at(0).groups.at(0).scrollAreas.at(0).tables.at(0);

/* Active cell contains a progress indicator/busy indicator.
   If there's none, then backup's done or script has crashed. */
var activeCell = getActiveCell(tmTable);

if (!activeCell) {
	console.log('No active cell was found.');
	curApp.doShellScript('exit 1');
}

var backupProgressText = activeCell.staticTexts.at(1);

mainLoop();

/*-----Functions--------------------------------------------------------------*/
function getDateAndTime() {
	return curApp.doShellScript("date '+%m/%d/%Y %H:%M:%S' ");
}

function mainLoop() {
	while(true) {
		if ( cellStillValid( activeCell ) ) {
			console.log( getDateAndTime() + ':  ' + 
				activeCell.staticTexts.at(1).value());
		} else {
			console.log(getDateAndTime() + ':  ' +
				'Backup appears complete or interrupted; exiting.');
			break;
		}
		delay(60);
	}
}

function cellStillValid(activeCell) {
	return(
		activeCell.uiElements.whose( {description: 'progress indicator'} ).length + 
		activeCell.uiElements.whose( {description: 'busy indicator'} ).length
	);
}

function getActiveCell(tmTable) {
	for (let i=0; i<tmTable.rows.length; i++) {
		if( (tmTable.rows.at(i).uiElements.at(0).progressIndicators.length > 0) ||
				(tmTable.rows.at(i).uiElements.at(0).busyIndicators.length > 0) ) {
			return tmTable.rows.at(i).uiElements.at(0);
		}	
	}
	return false;	// nothing was found
}
                              ? jscr  ??ޭ