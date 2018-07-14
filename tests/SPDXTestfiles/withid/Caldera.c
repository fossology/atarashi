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
** SPDX License to detect: https://spdx.org/licenses/Caldera.html				
*/



/* SPDX-License-Identifier: Caldera */
/*
Caldera International, Inc. hereby grants a fee free license that
includes the rights use, modify and distribute this named source code,
including creating derived binary products created from the source
code. The source code for which Caldera International, Inc. grants
rights are limited to the following UNIX Operating Systems that
operate on the 16-Bit PDP-11 CPU and early versions of the 32-Bit UNIX
Operating System, with specific exclusion of UNIX System III and UNIX
System V and successor operating systems:

     32-bit 32V UNIX
    
16 bit UNIX Versions 1, 2, 3, 4, 5, 6, 7

Caldera International, Inc.
makes no guarantees or commitments that any source code is available
from Caldera
International, Inc.

The following copyright notice
applies to the source code files for which this license is
granted.

Copyright(C) Caldera International Inc. 2001-2002. All
rights reserved.

Redistribution and use in source and binary forms,
with or without modification, are permitted provided that the
following conditions are met:

     Redistributions of source code and
documentation must retain the above copyright notice, this list of
conditions and the following disclaimer. 

     Redistributions in
binary form must reproduce the above copyright notice, this list of
conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

     All advertising
materials mentioning features or use of this software must display the
following acknowledgement:
This product includes software developed or
owned by Caldera International, Inc.

     Neither the name of Caldera
International, Inc. nor the names of other contributors may be used to
endorse or promote products derived from this software without
specific prior written permission.

USE OF THE SOFTWARE PROVIDED FOR
UNDER THIS LICENSE BY CALDERA INTERNATIONAL, INC. AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CALDERA
INTERNATIONAL, INC. BE LIABLE FOR ANY DIRECT, INDIRECT INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

