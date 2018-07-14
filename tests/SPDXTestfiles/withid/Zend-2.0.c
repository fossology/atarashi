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
** SPDX License to detect: https://spdx.org/licenses/Zend-2.0.html				
*/



/* SPDX-License-Identifier: Zend-2.0 */
/*
The Zend Engine License, version 2.00 
Copyright (c) 1999-2002 Zend
Technologies Ltd. All rights reserved. 

Redistribution and use in
source and binary forms, with or without modification, is permitted
provided that the following conditions are met:

     1.
Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer. 

     2.
Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.


     3. The names "Zend" and "Zend Engine" must not be used to
endorse or promote products derived from this software without prior
permission from Zend Technologies Ltd. For written permission, please
contact license@zend.com. 

     4. Zend Technologies Ltd. may publish
revised and/or new versions of the license from time to time. Each
version will be given a distinguishing version number. Once covered
code has been published under a particular version of the license, you
may always continue to use it under the terms of that version. You may
also choose to use such covered code under the terms of any subsequent
version of the license published by Zend Technologies Ltd. No one
other than Zend Technologies Ltd. has the right to modify the terms
applicable to covered code created under this License.

     5.
Redistributions of any form whatsoever must retain the following
acknowledgment: "This product includes the Zend Engine, freely
available at http://www.zend.com"

     6. All advertising materials
mentioning features or use of this software must display the following
acknowledgment: "The Zend Engine is freely available at
http://www.zend.com"

THIS SOFTWARE IS PROVIDED BY ZEND TECHNOLOGIES
LTD. ``AS IS'' AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT
NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ZEND
TECHNOLOGIES LTD. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
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

