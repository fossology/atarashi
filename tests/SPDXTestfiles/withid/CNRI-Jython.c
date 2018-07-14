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
** SPDX License to detect: https://spdx.org/licenses/CNRI-Jython.html				
*/



/* SPDX-License-Identifier: CNRI-Jython */
/*

1. This LICENSE AGREEMENT is between the Corporation for National
Research Initiatives, having an office at 1895 Preston White Drive,
Reston, VA 20191 ("CNRI"), and the Individual or Organization
("Licensee") accessing and using JPython version 1.1.x in source or
binary form and its associated documentation as provided herein
("Software"). 
2.  Subject to the terms and conditions of this
License Agreement, CNRI hereby grants Licensee a non-exclusive,
non-transferable, royalty-free, world-wide license to reproduce,
analyze, test, perform and/or display publicly, prepare derivative
works, distribute, and otherwise use the Software alone or in any
derivative version, provided, however, that CNRI's License Agreement
and CNRI's notice of copyright, i.e., “Copyright (c) 1996-1999
Corporation for National Research Initiatives; All Rights Reserved”
are both retained in the Software, alone or in any derivative version
prepared by Licensee. Alternatively, in lieu of CNRI's License
Agreement, Licensee may substitute the following text (omitting the
quotes), provided, however, that such text is displayed prominently in
the Software alone or in any derivative version prepared by Licensee:
“JPython (Version 1.1.x) is made available subject to the terms and
conditions in CNRI's License Agreement. This Agreement may be located
on the Internet using the following unique, persistent identifier
(known as a handle): 1895.22/1006. The License may also be obtained
from a proxy server on the Web using the following URL:
http://hdl.handle.net/1895.22/1006.” 
3.  In the event Licensee
prepares a derivative work that is based on or incorporates the
Software or any part thereof, and wants to make the derivative work
available to the public as provided herein, then Licensee hereby
agrees to indicate in any such work, in a prominently visible way, the
nature of the modifications made to CNRI's Software. 	
4. Licensee
may not use CNRI trademarks or trade name, including JPython or CNRI,
in a trademark sense to endorse or promote products or services of
Licensee, or any third party. Licensee may use the mark JPython in
connection with Licensee's derivative versions that are based on or
incorporate the Software, but only in the form “JPython-based
___________________,” or equivalent. 
5. CNRI is making the
Software available to Licensee on an “AS IS” basis. CNRI MAKES NO
REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE,
BUT NOT LIMITATION, CNRI MAKES NO AND DISCLAIMS ANY REPRESENTATION OR
WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR
THAT THE USE OF THE SOFTWARE WILL NOT INFRINGE ANY THIRD PARTY
RIGHTS. 
6. CNRI SHALL NOT BE LIABLE TO LICENSEE OR OTHER USERS OF
THE SOFTWARE FOR ANY INCIDENTAL, SPECIAL OR CONSEQUENTIAL DAMAGES OR
LOSS AS A RESULT OF USING, MODIFYING OR DISTRIBUTING THE SOFTWARE, OR
ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
SOME STATES DO NOT ALLOW THE LIMITATION OR EXCLUSION OF LIABILITY SO
THE ABOVE DISCLAIMER MAY NOT APPLY TO LICENSEE. 
7. This License
Agreement may be terminated by CNRI (i) immediately upon written
notice from CNRI of any material breach by the Licensee, if the nature
of the breach is such that it cannot be promptly remedied; or (ii)
sixty (60) days following notice from CNRI to Licensee of a material
remediable breach, if Licensee has not remedied such breach within
that sixty-day period. 
8. This License Agreement shall be governed
by and interpreted in all respects by the law of the State of
Virginia, excluding conflict of law provisions. Nothing in this
Agreement shall be deemed to create any relationship of agency,
partnership, or joint venture between CNRI and Licensee. 
9. By
clicking on the "ACCEPT" button where indicated, or by installing,
copying or otherwise using the Software, Licensee agrees to be bound
by the terms and conditions of this License Agreement.   
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

