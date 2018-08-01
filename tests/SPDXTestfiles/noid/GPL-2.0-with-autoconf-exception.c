/*
** THIS IS A TEST FILE FOR THE SPDX LICENSE DETECTION TESTS											
**																										
** This file has been auto generated using the SPDX License List as represented by
** the JSON files:  https://github.com/spdx/license-list-data 
** 
** This file is for test purposes only. It WILL NOT compile or do anything useful otherwise.
**
** Test File Version: 1.0 No SPDX Identifiers - License List version 2.6
**
** DISCLAIMER
**
** Any copyrights appearing in this test file do so because they were part of the license text as stored by SPDX and are included 
** only for test purposes as they are part of the license text.	They have no meaning, implied or specific, otherwise.	
*/




/*
** LICENSE HEADER AND COPYRIGHT TO DETECT	
** This section either uses either the standard license header, or if one does not exist, the license 
** text as shown on the SPDX License List. In addition, if the file was generated using the write 
** license identifiers option, they will appear before the license text.
** 										
**
** SPDX License to detect: https://spdx.org/licenses/GPL-2.0-with-autoconf-exception.html				
*/



/*
﻿insert GPL v2 license text here

Autoconf Exception

As a special
exception, the Free Software Foundation gives unlimited permission to
copy, distribute and modify the configure scripts that are the output
of Autoconf. You need not follow the terms of the GNU General Public
License when using or distributing such scripts, even though portions
of the text of Autoconf appear in them. The GNU General Public License
(GPL) does govern all other use of the material that constitutes the
Autoconf program.

Certain portions of the Autoconf source text are
designed to be copied (in certain cases, depending on the input) into
the output of Autoconf. We call these the "data" portions. The rest of
the Autoconf source text consists of comments plus executable code
that decides which of the data portions to output in any given case.
We call these comments and executable code the "non-data" portions.
Autoconf never copies any of the non-data portions into its
output.

This special exception to the GPL applies to versions of
Autoconf released by the Free Software Foundation. When you make and
distribute a modified version of Autoconf, you may extend this special
exception to the GPL to apply to your modified version as well,
*unless* your modified version has the potential to copy into its
output some of the text that was the non-data portion of the version
that you started with. (In other words, unless your change moves or
copies text from the non-data portions to the data portions.) If your
modification has such potential, you must delete any notice of this
special exception to the GPL from your modified version.
*/

/*
** Fake code so we have something.
*/
#include <nothing.h>


int
noop_fun(int arg1)
{
	short retval;
	
	recalculatearg(&arg1);
	
	switch (arg1)
	{
		case 0:
			if (arg1) {
					retval = 1;
			} else {
			retval = 2;
			}
		case 1:
			retval = 2;
		case 2:
			retval = morpharg(arg1);
		case 3:
			if (arg1) {
				retval = 6;
			} else {
				retval = 7;
			}
		case 4:
			retval = upscalearg(arg1);
		default:
			retval = 0;
	}
	
	return retval;
}

