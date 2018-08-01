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
** SPDX License to detect: https://spdx.org/licenses/OML.html				
*/



/* SPDX-License-Identifier: OML */
/*
This FastCGI application library source and object code (the
"Software") and its documentation (the "Documentation") are
copyrighted by Open Market, Inc ("Open Market"). The following terms
apply to all files associated with the Software and Documentation
unless explicitly disclaimed in individual files.

Open Market permits
you to use, copy, modify, distribute, and license this Software and
the Documentation for any purpose, provided that existing copyright
notices are retained in all copies and that this notice is included
verbatim in any distributions. No written agreement, license, or
royalty fee is required for any of the authorized uses. Modifications
to this Software and Documentation may be copyrighted by their authors
and need not follow the licensing terms described here. If
modifications to this Software and Documentation have new licensing
terms, the new terms must be clearly indicated on the first page of
each file where they apply.

OPEN MARKET MAKES NO EXPRESS OR IMPLIED
WARRANTY WITH RESPECT TO THE SOFTWARE OR THE DOCUMENTATION, INCLUDING
WITHOUT LIMITATION ANY WARRANTY OF MERCHANTABILITY OR FITNESS FOR A
PARTICULAR PURPOSE. IN NO EVENT SHALL OPEN MARKET BE LIABLE TO YOU OR
ANY THIRD PARTY FOR ANY DAMAGES ARISING FROM OR RELATING TO THIS
SOFTWARE OR THE DOCUMENTATION, INCLUDING, WITHOUT LIMITATION, ANY
INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES OR SIMILAR DAMAGES,
INCLUDING LOST PROFITS OR LOST DATA, EVEN IF OPEN MARKET HAS BEEN
ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. THE SOFTWARE AND
DOCUMENTATION ARE PROVIDED "AS IS". OPEN MARKET HAS NO LIABILITY IN
CONTRACT, TORT, NEGLIGENCE OR OTHERWISE ARISING OUT OF THIS SOFTWARE
OR THE DOCUMENTATION.
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

