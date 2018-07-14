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
** SPDX License to detect: https://spdx.org/licenses/Saxpath.html				
*/



/*
Copyright (C) 2000-2002 werken digital.  
All rights reserved.  


Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions 
are met:   

     1. Redistributions of source code must retain the
above copyright  notice, this list of conditions, and the following
disclaimer.   

     2. Redistributions in binary form must reproduce
the above copyright  notice, this list of conditions, and the
disclaimer that follows  these conditions in the documentation and/or
other materials  provided with the distribution.   

     3. The name
"SAXPath" must not be used to endorse or promote products  derived
from this software without prior written permission. For  written
permission, please contact license@saxpath.org.   

     4. Products
derived from this software may not be called "SAXPath", nor  may
"SAXPath" appear in their name, without prior written permission  from
the SAXPath Project Management (pm@saxpath.org).   

In addition, we
request (but do not require) that you include in the  end-user
documentation provided with the redistribution and/or in the  software
itself an acknowledgement equivalent to the following:  
     "This
product includes software developed by the  SAXPath Project
(http://www.saxpath.org/)."  

Alternatively, the acknowledgment may
be graphical using the logos  available at http://www.saxpath.org/  


THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED 
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES  OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE  DISCLAIMED.
IN NO EVENT SHALL THE SAXPath AUTHORS OR THE PROJECT  CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,  SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT  LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF  USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND  ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY,  OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT  OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF  SUCH DAMAGE.
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

