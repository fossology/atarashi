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
** SPDX License to detect: https://spdx.org/licenses/NetCDF.html				
*/



/* SPDX-License-Identifier: NetCDF */
/*
Copyright 1993-2014 University Corporation for Atmospheric
Research/Unidata

Portions of this software were developed by the
Unidata Program at the University Corporation for Atmospheric
Research.

Access and use of this software shall impose the following
obligations and understandings on the user. The user is granted the
right, without any fee or cost, to use, copy, modify, alter, enhance
and distribute this software, and any derivative works thereof, and
its supporting documentation for any purpose whatsoever, provided that
this entire notice appears in all copies of the software, derivative
works and supporting documentation. Further, UCAR requests that the
user credit UCAR/Unidata in any publications that result from the use
of this software or in any product that includes this software,
although this is not an obligation. The names UCAR and/or Unidata,
however, may not be used in any advertising or publicity to endorse or
promote any products or commercial entity unless specific written
permission is obtained from UCAR/Unidata. The user also understands
that UCAR/Unidata is not obligated to provide the user with any
support, consulting, training or assistance of any kind with regard to
the use, operation and performance of this software nor to provide the
user with any updates, revisions, new versions or "bug fixes."

THIS
SOFTWARE IS PROVIDED BY UCAR/UNIDATA "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL UCAR/UNIDATA BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE ACCESS, USE OR PERFORMANCE OF THIS SOFTWARE.
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

