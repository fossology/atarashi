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
** SPDX License to detect: https://spdx.org/licenses/TMate.html				
*/



/*
The TMate Open Source License. 

This license applies to all portions
of TMate SVNKit library, which are not externally-maintained libraries
(e.g. Ganymed SSH library).

All the source code and compiled classes
in package org.tigris.subversion.javahl except SvnClient class are
covered by the license in JAVAHL-LICENSE file

Copyright (c) 2004-2012
TMate Software. All rights reserved.

Redistribution and use in source
and binary forms, with or without modification, are permitted provided
that the following conditions are met:

     * Redistributions of
source code must retain the above copyright notice, this list of
conditions and the following disclaimer.  
     
     *
Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution. 

    
     * Redistributions in any form must be accompanied by
information on how to obtain complete source code for the software
that uses SVNKit and any accompanying software that uses the software
that uses SVNKit. The source code must either be included in the
distribution or be available for no more than the cost of distribution
plus a nominal fee, and must be freely redistributable under
reasonable conditions. For an executable file, complete source code
means the source code for all modules it contains. It does not include
source code for modules or files that typically accompany the major
components of the operating system on which the executable file runs.

  
     * Redistribution in any form without redistributing source
code for software that uses SVNKit is possible only when such
redistribution is explictly permitted by TMate Software. Please,
contact TMate Software at support@svnkit.com to get such
permission.

THIS SOFTWARE IS PROVIDED BY TMATE SOFTWARE ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE, OR NON-INFRINGEMENT, ARE DISCLAIMED. 

IN NO EVENT SHALL
TMATE SOFTWARE BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
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

