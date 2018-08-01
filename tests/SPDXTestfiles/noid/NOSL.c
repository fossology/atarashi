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
** SPDX License to detect: https://spdx.org/licenses/NOSL.html				
*/



/*
The contents of this file are subject to the Netizen Open Source
License Version 1.0 (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License
at http://netizen.com.au/licenses/NOPL/ 

Software distributed under
the License is distributed on an "AS IS" basis, WITHOUT WARRANTY OF
ANY KIND, either express or implied. See the License for the specific
language governing rights and limitations under the License. 

The
Original Code is ______________________________________. 

The Initial
Developer of the Original Code is ________________________. Portions
created by ______________________ are Copyright (C) ______
_______________________. All Rights Reserved. 

Contributor(s):
______________________________________. 

Alternatively, the contents
of this file may be used under the terms of the _____ license (the
"[___] License"), in which case the provisions of [______] License are
applicable instead of those above. If you wish to allow use of your
version of this file only under the terms of the [____] License and
not to allow others to use your version of this file under the NOSL,
indicate your decision by deleting the provisions above and replace
them with the notice and other provisions required by the [___]
License. If you do not delete the provisions above, a recipient may
use your version of this file under either the NOSL or the [___]
License.
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

