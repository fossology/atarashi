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
** SPDX License to detect: https://spdx.org/licenses/Sendmail.html				
*/



/*
SENDMAIL LICENSE 

The following license terms and conditions apply,
unless a redistribution agreement or other license is obtained from
Sendmail, Inc., 6475 Christie Ave, Third Floor, Emeryville, CA 94608,
USA, or by electronic mail at license@sendmail.com. 

License Terms:


Use, Modification and Redistribution (including distribution of any
modified or derived work) in source and binary forms is permitted only
if each of the following conditions is met: 

1. Redistributions
qualify as "freeware" or "Open Source Software" under one of the
following terms: 

     (a) Redistributions are made at no charge
beyond the reasonable cost of materials and delivery. 

     (b)
Redistributions are accompanied by a copy of the Source Code or by an
irrevocable offer to provide a copy of the Source Code for up to three
years at the cost of materials and delivery. Such redistributions must
allow further use, modification, and redistribution of the Source Code
under substantially the same terms as this license. For the purposes
of redistribution "Source Code" means the complete compilable and
linkable source code of sendmail including all modifications. 

2.
Redistributions of Source Code must retain the copyright notices as
they appear in each Source Code file, these license terms, and the
disclaimer/limitation of liability set forth as paragraph 6 below.


3. Redistributions in binary form must reproduce the Copyright
Notice, these license terms, and the disclaimer/limitation of
liability set forth as paragraph 6 below, in the documentation and/or
other materials provided with the distribution. For the purposes of
binary distribution the "Copyright Notice" refers to the following
language: 
"Copyright (c) 1998-2010 Sendmail, Inc. All rights
reserved." 

4. Neither the name of Sendmail, Inc. nor the University
of California nor names of their contributors may be used to endorse
or promote products derived from this software without specific prior
written permission. The name "sendmail" is a trademark of Sendmail,
Inc. 

5. All redistributions must comply with the conditions imposed
by the University of California on certain embedded code, which
copyright Notice and conditions for redistribution are as follows: 

 
   (a) Copyright (c) 1988, 1993 The Regents of the University of
California. All rights reserved. 

     (b) Redistribution and use in
source and binary forms, with or without modification, are permitted
provided that the following conditions are met: 

          (i)
Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer. 139848.1 

     
    (ii) Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution. 

          (iii) Neither the name of the University nor
the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission. 

6. Disclaimer/Limitation of Liability: THIS SOFTWARE IS
PROVIDED BY SENDMAIL, INC. AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL SENDMAIL, INC., THE REGENTS OF THE
UNIVERSITY OF CALIFORNIA OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGES. 

$Revision: 8.16 $, Last updated $Date:
2010/10/25 23:11:19 $, Document 139848.1
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

