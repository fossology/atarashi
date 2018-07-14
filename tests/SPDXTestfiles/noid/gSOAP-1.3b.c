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
** SPDX License to detect: https://spdx.org/licenses/gSOAP-1.3b.html				
*/



/*
The contents of this file are subject to the gSOAP Public License
Version 1.3 (the "License"); you may not use this file except in
compliance with the License. You may obtain a copy of the License at
http://www.cs.fsu.edu/ engelen/soaplicense.html

Software distributed
under the License is distributed on an "AS IS" basis, WITHOUT WARRANTY
OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the
License.

The Original Code of the gSOAP Software is: stdsoap.h,
stdsoap2.h, stdsoap.c, stdsoap2.c, stdsoap.cpp, stdsoap2.cpp,
soapcpp2.h, soapcpp2.c, soapcpp2_lex.l, soapcpp2_yacc.y, error2.h,
error2.c, symbol2.c, init2.c, soapdoc2.html, and soapdoc2.pdf,
httpget.h, httpget.c, stl.h, stldeque.h, stllist.h, stlvector.h,
stlset.h.

The Initial Developer of the Original Code is Robert A. van
Engelen. Portions created by Robert A. van Engelen are Copyright (C)
2001-2004 Robert A. van Engelen, Genivia inc. All Rights
Reserved.
Contributor(s):
"________________________."
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

