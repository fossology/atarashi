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
** SPDX License to detect: https://spdx.org/licenses/DSDP.html				
*/



/* SPDX-License-Identifier: DSDP */
/*
COPYRIGHT NOTIFICATION

(C) COPYRIGHT 2004 UNIVERSITY OF CHICAGO

This
program discloses material protectable under copyright laws of the
United States. Permission to copy and modify this software and its
documentation is hereby granted, provided that this notice is retained
thereon and on all copies or modifications. The University of Chicago
makes no representations as to the suitability and operability of this
software for any purpose. It is provided "as is"; without express or
implied warranty. Permission is hereby granted to use, reproduce,
prepare derivative works, and to redistribute to others, so long as
this original copyright notice is retained. Any publication resulting
from research that made use of this software should cite this
document.

     This software was authored by:

     Steven J. Benson
Mathematics and Computer Science Division Argonne National Laboratory
Argonne IL 60439

     Yinyu Ye Department of Management Science and
Engineering Stanford University Stanford, CA U.S.A

     Any questions
or comments on the software may be directed to benson@mcs.anl.gov or
yinyu-ye@stanford.edu 

Argonne National Laboratory with facilities in
the states of Illinois and Idaho, is owned by The United States
Government, and operated by the University of Chicago under provision
of a contract with the Department of Energy.

DISCLAIMER 
THIS PROGRAM
WAS PREPARED AS AN ACCOUNT OF WORK SPONSORED BY AN AGENCY OF THE
UNITED STATES GOVERNMENT. NEITHER THE UNITED STATES GOVERNMENT NOR ANY
AGENCY THEREOF, NOR THE UNIVERSITY OF CHICAGO, NOR ANY OF THEIR
EMPLOYEES OR OFFICERS, MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR
ASSUMES ANY LEGAL LIABILITY OR RESPONSIBILITY FOR THE ACCURACY,
COMPLETENESS, OR USEFULNESS OF ANY INFORMATION, APPARATUS, PRODUCT, OR
PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE
PRIVATELY OWNED RIGHTS. REFERENCE HEREIN TO ANY SPECIFIC COMMERCIAL
PRODUCT, PROCESS, OR SERVICE BY TRADE NAME, TRADEMARK, MANUFACTURER,
OR OTHERWISE, DOES NOT NECESSARILY CONSTITUTE OR IMPLY ITS
ENDORSEMENT, RECOMMENDATION, OR FAVORING BY THE UNITED STATES
GOVERNMENT OR ANY AGENCY THEREOF. THE VIEW AND OPINIONS OF AUTHORS
EXPRESSED HEREIN DO NOT NECESSARILY STATE OR REFLECT THOSE OF THE
UNITED STATES GOVERNMENT OR ANY AGENCY THEREOF.
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

