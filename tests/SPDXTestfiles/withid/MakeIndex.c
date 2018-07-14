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
** SPDX License to detect: https://spdx.org/licenses/MakeIndex.html				
*/



/* SPDX-License-Identifier: MakeIndex */
/*
MakeIndex Distribution Notice

11/11/1989

Copyright (C) 1989 by Chen
& Harrison International Systems, Inc.
Copyright (C) 1988 by Olivetti
Research Center
Copyright (C) 1987 by Regents of the University of
California

Author:
     Pehong Chen (phc@renoir.berkeley.edu)
    
Chen & Harrison International Systems, Inc.
     Palo Alto,
California
     USA

Permission is hereby granted to make and
distribute original copies of this program provided that the copyright
notice and this permission notice are preserved and provided that the
recipient is not asked to waive or limit his right to redistribute
copies as allowed by this permission notice and provided that anyone
who receives an executable form of this program is granted access to a
machine-readable form of the source code for this program at a cost
not greater than reasonable reproduction, shipping, and handling
costs.  Executable forms of this program distributed without the
source code must be accompanied by a conspicuous copy of this
permission notice and a statement that tells the recipient how to
obtain the source code.

Permission is granted to distribute modified
versions of all or part of this program under the conditions above
with the additional requirement that the entire modified work must be
covered by a permission notice identical to this permission notice.
Anything distributed with and usable only in conjunction with
something derived from this program, whose useful purpose is to extend
or adapt or add capabilities to this program, is to be considered a
modified version of this program under the requirement above.  Ports
of this program to other systems not supported in the distribution are
also considered modified versions.  All modified versions should be
reported back to the author.

This program is distributed with no
warranty of any sort.  No contributor accepts responsibility for the
consequences of using this program or for whether it serves any
particular purpose.
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

