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
** SPDX License to detect: https://spdx.org/licenses/Xerox.html				
*/



/* SPDX-License-Identifier: Xerox */
/*
Copyright (c) 1995, 1996 Xerox Corporation. All Rights Reserved.

Use
and copying of this software and preparation of derivative works based
upon this software are permitted. Any copy of this software or of any
derivative work must include the above copyright notice of Xerox
Corporation, this paragraph and the one after it. Any distribution of
this software or derivative works must comply with all applicable
United States export control laws.

This software is made available AS
IS, and XEROX CORPORATION DISCLAIMS ALL WARRANTIES, EXPRESS OR
IMPLIED, INCLUDING WITHOUT LIMITATION THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, AND
NOTWITHSTANDING ANY OTHER PROVISION CONTAINED HEREIN, ANY LIABILITY
FOR DAMAGES RESULTING FROM THE SOFTWARE OR ITS USE IS EXPRESSLY
DISCLAIMED, WHETHER ARISING IN CONTRACT, TORT (INCLUDING NEGLIGENCE)
OR STRICT LIABILITY, EVEN IF XEROX CORPORATION IS ADVISED OF THE
POSSIBILITY OF SUCH DAMAGES.
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

