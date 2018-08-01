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
** SPDX License to detect: https://spdx.org/licenses/Adobe-Glyph.html				
*/



/*
Copyright (c) 1997,1998,2002,2007 Adobe Systems Incorporated


Permission is hereby granted, free of charge, to any person
obtaining a copy of this documentation file to use, copy, publish,
distribute, sublicense, and/or sell copies of the documentation, and
to permit others to do the same, provided that: 

     - No
modification, editing or other alteration of this document is allowed;
and 
     - The above copyright notice and this permission notice
shall be included in all copies of the documentation. 

Permission is
hereby granted, free of charge, to any person obtaining a copy of this
documentation file, to create their own derivative works from the
content of this document to use, copy, publish, distribute,
sublicense, and/or sell the derivative works, and to permit others to
do the same, provided that the derived work is not represented as
being a copy or version of this document. 

Adobe shall not be liable
to any party for any loss of revenue or profit or for indirect,
incidental, special, consequential, or other similar damages, whether
based on tort (including without limitation negligence or strict
liability), contract or other legal or equitable grounds even if Adobe
has been advised or had reason to know of the possibility of such
damages.Ê The Adobe materials are provided on an "AS IS" basis.Ê
Adobe specifically disclaims all express, statutory, or implied
warranties relating to the Adobe materials, including but not limited
to those concerning merchantability or fitness for a particular
purpose or non-infringement of any third party rights regarding the
Adobe materials. 
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

