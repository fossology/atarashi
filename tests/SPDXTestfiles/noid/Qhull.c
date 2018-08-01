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
** SPDX License to detect: https://spdx.org/licenses/Qhull.html				
*/



/*
Qhull, Copyright (c) 1993-2003

The National Science and Technology
Research Center for Computation and Visualization of Geometric
Structures (The Geometry Center) University of Minnesota

email:
qhull@qhull.org

This software includes Qhull from The Geometry
Center. Qhull is copyrighted as noted above. Qhull is free software
and may be obtained via http from www.qhull.org. It may be freely
copied, modified, and redistributed under the following
conditions:

1. All copyright notices must remain intact in all
files.

2. A copy of this text file must be distributed along with any
copies of Qhull that you redistribute; this includes copies that you
have modified, or copies of programs or other software products that
include Qhull.

3. If you modify Qhull, you must include a notice
giving the name of the person performing the modification, the date of
modification, and the reason for such modification.

4. When
distributing modified versions of Qhull, or other software products
that include Qhull, you must provide notice that the original source
code may be obtained as noted above.

5. There is no warranty or other
guarantee of fitness for Qhull, it is provided solely "as is". Bug
reports or fixes may be sent to qhull_bug@qhull.org; the authors may
or may not act on them as they desire.
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

