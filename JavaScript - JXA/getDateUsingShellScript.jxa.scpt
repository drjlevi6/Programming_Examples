JsOsaDAS1.001.00bplist00?Vscript_function getDateUsingShellScript(formatString) {
	let curApp = Application.currentApplication();
	curApp.includeStandardAdditions = true;
	return curApp.doShellScript("date " + formatString);
}

getDateUsingShellScript('+%m/%d/%Y');

/*
Result:"10/01/2021"
*/
                              jscr  ??ޭ