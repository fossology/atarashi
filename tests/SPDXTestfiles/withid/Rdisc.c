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
** SPDX License to detect: https://spdx.org/licenses/Rdisc.html				
*/



/* SPDX-License-Identifier: Rdisc */
/*
Rdisc (this program) was developed by Sun Microsystems, Inc. and is 
provided for unrestricted use provided that this legend is included on
 all tape media and as a part of the software program in whole or
part.  Users may copy or modify Rdisc without charge, and they may
freely  distribute it.   

RDISC IS PROVIDED AS IS WITH NO WARRANTIES
OF ANY KIND INCLUDING THE  WARRANTIES OF DESIGN, MERCHANTIBILITY AND
FITNESS FOR A PARTICULAR  PURPOSE, OR ARISING FROM A COURSE OF
DEALING, USAGE OR TRADE PRACTICE.   

Rdisc is provided with no
support and without any obligation on the  part of Sun Microsystems,
Inc. to assist in its use, correction,  modification or enhancement.  


SUN MICROSYSTEMS, INC. SHALL HAVE NO LIABILITY WITH RESPECT TO THE 
INFRINGEMENT OF COPYRIGHTS, TRADE SECRETS OR ANY PATENTS BY RDISC  OR
ANY PART THEREOF.   

In no event will Sun Microsystems, Inc. be
liable for any lost revenue  or profits or other special, indirect and
consequential damages, even  if Sun has been advised of the
possibility of such damages.   

Sun Microsystems, Inc.  
2550 Garcia
Avenue  
Mountain View, California 94043
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

