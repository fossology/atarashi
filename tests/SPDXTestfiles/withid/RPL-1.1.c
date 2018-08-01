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
** SPDX License to detect: https://spdx.org/licenses/RPL-1.1.html				
*/



/* SPDX-License-Identifier: RPL-1.1 */
/*
Copyright (C) 1999-2002 Technical Pursuit Inc., All Rights Reserved.
Patent Pending, Technical Pursuit Inc.

    Unless explicitly acquired
and licensed from Licensor under the Technical Pursuit License ("TPL")
Version 1.0 or greater, the contents of this file are subject to the
Reciprocal Public License ("RPL") Version 1.1, or subsequent versions
as allowed by the RPL, and You may not copy or use this file in either
source code or executable form, except in compliance with the terms
and conditions of the RPL.

    You may obtain a copy of both the TPL
and the RPL (the "Licenses") from Technical Pursuit Inc. at
http://www.technicalpursuit.com.

    All software distributed under
the Licenses is provided strictly on an "AS IS" basis, WITHOUT
WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, AND TECHNICAL PURSUIT
INC. HEREBY DISCLAIMS ALL SUCH WARRANTIES, INCLUDING WITHOUT
LIMITATION, ANY WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE, QUIET ENJOYMENT, OR NON-INFRINGEMENT. See the
Licenses for specific language governing rights and limitations under
the Licenses.
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

